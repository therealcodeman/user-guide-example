SpacecraftStatus
================

Message Information
-------------------

+----+-------------+---------------+-----------------------------------------------+
| ID | Total Bytes | Variable Size | Description                                   |
+====+=============+===============+===============================================+
| 1  | 12          | False         | Provides health and status of the spacecraft. |
+----+-------------+---------------+-----------------------------------------------+

Message Contents
----------------

+----------------+------+-------+--------+-------------------------------------+
| Name           | Type | Bytes | Fields | Description                         |
+================+======+=======+========+=====================================+
| Pcie_Status    | enum | 4     |        | Provides pcie link status           |
+----------------+------+-------+--------+-------------------------------------+
| Heater1_Status | enum | 4     |        | Provides status of the heater       |
+----------------+------+-------+--------+-------------------------------------+
| Heater2_Status | enum | 4     |        | Altitude in meters above sea level. |
+----------------+------+-------+--------+-------------------------------------+
