# Export Nexus device show interface brief command output to
# an Excel file
import json

import xlsxwriter

from netmiko import ConnectHandler

# Devices to SSH into
devices = [
    {
        "device_type": "cisco_nxos",
        "ip": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
        "port": 8181,
        "fast_cli": False,
        "session_log": "nxos-exercise4-2-1.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.46",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-2-2.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.47",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-2-3.log",
        "verbose": True,
    },
]

# Create an Excel file
with xlsxwriter.Workbook(filename="Ex4-2-Nexus-Inventory.xlsx") as wb:
    # Loop over each device
    for device in devices:
        # Connect to each device
        with ConnectHandler(**device) as conn:
            # Parse hostname of each device
            hostname = conn.send_command(
                command_string="show hostname", use_textfsm=True
            )[0]["hostname"]
            # Parse show inventory of each device
            inventory = conn.send_command(
                command_string="show inventory", use_textfsm=True
            )

        # Export interfaces to a JSON file for readability (Comment out if you don't need it)
        with open(file=f"{hostname}-inventory.json", mode="wt") as f:
            json.dump(obj=inventory, fp=f, indent=4, sort_keys=True)
        # Create worksheets with the hostname of each device
        ws = wb.add_worksheet(f"{hostname} Inventory")
        # Auto Filter for header line
        ws.autofilter("A1:E1")
        # Freeze top row and very left column only
        ws.freeze_panes(1, 1)

        # Header line
        header_line = {
            "A1": "Module Name",  # 1
            "B1": "Serial Number",  # 2
            "C1": "Product Identifier (PID)",  # 3
            "D1": "Version Identifier (VID)",  # 4
            "E1": "Description",  # 5
        }

        # Format header line text
        header_line_frmt = wb.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#0058a0",
                "font_color": "#FFFFFF",
            }
        )

        # Write header line
        for cell, val in header_line.items():
            ws.write(cell, val, header_line_frmt)

        # Initial Values for row and col
        row, col = 1, 0

        # Place data according to header line
        for module in inventory:
            ws.write(row, col + 0, module["name"])  # Module Name
            ws.write(row, col + 1, module["sn"])  # Serial Number
            ws.write(row, col + 2, module["pid"])  # PID
            ws.write(row, col + 3, module["vid"])  # VID
            ws.write(row, col + 4, module["descr"])  # Description

            # Jump to next row
            row += 1

print("Done")
