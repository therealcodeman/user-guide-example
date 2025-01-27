import json
import os
from jsonschema import validate, ValidationError

# JSON Schema
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "id": {"type": "integer"},
        "description": {"type": "string"},
        "totalBytes": {"type": "integer"},
        "isVariableSize": {"type": "boolean"},
        "contents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "bytes": {"type": "integer"},
                    "description": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "bytes": {"type": "integer"},
                                "description": {"type": "string"}
                            },
                            "required": ["name", "type", "bytes"]
                        }
                    }
                },
                "required": ["name", "type", "bytes"]
            }
        }
    },
    "required": ["title", "id", "description", "contents"]
}

def create_dynamic_table(header, rows):
    """Generate a dynamic RST table with column widths adjusted to content."""
    # Calculate the width of each column based on the longest element in the header and rows
    column_widths = [max(len(str(item)) for item in col) for col in zip(*([header] + rows))]

    # Create the table header with dynamic column widths
    table = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+\n"
    table += "|" + "|".join([f" {header[i]:<{column_widths[i]}} " for i in range(len(header))]) + "|\n"
    table += "+" + "+".join(["=" * (width + 2) for width in column_widths]) + "+\n"

    # Create each data row with dynamic column widths
    for row in rows:
        table += "|" + "|".join([f" {str(row[i]):<{column_widths[i]}} " for i in range(len(row))]) + "|\n"
        table += "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+\n"

    return table

def json_to_rst(json_data, output_file):
    """Convert JSON data into reStructuredText format with dynamic tables for header and contents."""
    # Header Information as a Table
    header = ["ID", "Total Bytes", "Variable Size", "Description"]
    header_rows = [
        (str(json_data["id"]), str(json_data.get("totalBytes", "N/A")),
         str(json_data.get("isVariableSize", "N/A")), json_data["description"])
    ]
    
    # Write the message header table
    rst_content = f"{json_data['title']}\n{'=' * len(json_data['title'])}\n\n"
    message_header = "Message Information"
    rst_content += f"{message_header}\n" + "-"*len(message_header) + "\n\n"
    rst_content += create_dynamic_table(header, header_rows) + "\n"

    # Contents as a Single Table
    message_contents = "Message Contents"
    rst_content += f"{message_contents}\n" + "-"*len(message_contents) + "\n\n"
    
    # Table header with Description last
    table_header = ["Name", "Type", "Bytes", "Fields", "Description"]
    table_rows = []

    # Add each content as a row in the table
    for content in json_data["contents"]:
        fields = ", ".join([field["name"] for field in content.get("fields", [])]) if "fields" in content else ""
        row = [
            content["name"],
            content["type"],
            str(content["bytes"]),
            fields,
            content.get("description", "No description")
        ]
        table_rows.append(row)

    # Add the table to the RST content
    rst_content += create_dynamic_table(table_header, table_rows)

    # Write to the output file
    with open(output_file, "w") as f:
        f.write(rst_content)

    print(f"RST file generated: {output_file}")


def update_index_rst(index_path, entries, title):
    """Update an index.rst file with new entries."""
    index_content = f"{title}\n{'=' * len(title)}\n\n.. toctree::\n   :maxdepth: 2\n\n"
    for entry in sorted(entries):
        # Ensure the entry is relative to 'messages' directory, no additional 'messages/' prefix
        entry_name = entry.split('/')[-1]  # Extract filename without path prefix
        index_content += f"   {entry_name}\n"

    with open(index_path, "w") as f:
        f.write(index_content)

    print(f"Updated index file: {index_path}")


def process_directory(input_dir, output_dir, root_index_path, messages_index_path):
    """Process all JSON files in the input directory and output RST files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.rst"
            output_path = os.path.join(output_dir, output_filename)

            try:
                with open(input_path, "r") as file:
                    json_data = json.load(file)
                    validate(instance=json_data, schema=schema)  # Validate JSON
                    json_to_rst(json_data, output_path)
                    generated_files.append(f"messages/{os.path.splitext(filename)[0]}")
            except ValidationError as e:
                print(f"Validation error in {filename}: {e.message}")
            except json.JSONDecodeError as e:
                print(f"Error decoding {filename}: {e}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Update the messages index.rst
    update_index_rst(messages_index_path, generated_files, "Telemetry Messages")

    # Update the root index.rst to include the messages index
    update_index_rst(
        "messages/index",
        ["messages/index"],
        "Project Documentation"
    )

if __name__ == "__main__":
    # Directories
    input_directory = "messages"  # Root-level directory containing JSON files
    output_directory = "docs/source/messages"  # Directory for RST output
    root_index = "docs/source/index.rst"  # Root index file
    messages_index = "docs/source/messages/index.rst"  # Messages index file

    if not os.path.exists(input_directory):
        print(f"Error: Input directory '{input_directory}' does not exist.")
    else:
        process_directory(input_directory, output_directory, root_index, messages_index)
