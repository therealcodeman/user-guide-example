# User Guide Example

### **1. Install Sphinx**
Make sure you have Python installed, then install Sphinx using `pip`:

```bash
pip install sphinx
```

---

### **2. Initialize a Sphinx Project**
Run the following command to create a new Sphinx documentation project:

```bash
sphinx-quickstart
```

This interactive tool will ask for basic information about your project. You can customize the following:
- Project name
- Author
- Version
- Whether to enable extensions like `autodoc` (yes, if you want to document Python code automatically).

This generates a basic project structure.

---

### **3. Integrate Doxygen**
Doxygen can generate XML output, which Sphinx can parse using the `breathe` extension.

#### **a. Install Doxygen**
Install Doxygen from your package manager or its official site:
- On Linux:
  ```bash
  sudo apt install doxygen
  ```
- On macOS:
  ```bash
  brew install doxygen
  ```
- On Windows: Download and install from [doxygen.org](https://doxygen.nl).

#### **b. Generate Doxygen Configuration**
Run `doxygen -g` to generate a `Doxyfile` configuration file. Modify the following in the `Doxyfile`:
```plaintext
GENERATE_XML = YES
XML_OUTPUT = doxygen_xml
```
This tells Doxygen to generate XML output in a directory called `doxygen_xml`.

#### **c. Run Doxygen**
Generate the XML files by running:
```bash
doxygen
```

---

### **4. Install and Configure Breathe**
Install the `breathe` extension for Sphinx:

```bash
pip install breathe
```

Add `breathe` to the `extensions` list in your `conf.py`:

```python
extensions = [
    'breathe',
]

breathe_projects = {
    "MyProject": "path/to/doxygen_xml"
}
breathe_default_project = "MyProject"
```

Replace `path/to/doxygen_xml` with the path to the XML output directory created by Doxygen.

---

### **5. Link Doxygen Content in RST**
To display Doxygen documentation in your Sphinx project, use `.. doxygen...` directives provided by `breathe`. For example:

```rst
Doxygen Documentation
======================

.. doxygenindex::
   :project: MyProject
```

This will include the main Doxygen index.

---

### **6. Build Your Documentation**
Build your Sphinx documentation with:
```bash
sphinx-build -b html source/ build/
```

Open the `index.html` file in the `build` directory to view your documentation.

---

### **7. Bonus: Automate the Process**
You can create a script to automate running Doxygen and Sphinx together:

```bash
#!/bin/bash
# Generate Doxygen XML
doxygen

# Build Sphinx documentation
sphinx-build -b html source/ build/
```

Make the script executable and run it whenever you need to update your documentation.

---

### **8. Optional: Enable Theme and Extensions**
Use a modern Sphinx theme like `furo` or `sphinx_rtd_theme` for better visuals:
```bash
pip install furo
```

In `conf.py`:
```python
html_theme = "furo"
```