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
with xlsxwriter.Workbook(filename="Ex4-2-Nexus-Inventory.xlsx") as workbook:
    # Loop over each device
    for device in devices:
        # Connect to each device
        with ConnectHandler(**device) as net_connect:
            # Parse hostname of each device
            hostname = net_connect.send_command(
                command_string="show hostname", use_textfsm=True
            )[0]["hostname"]
            # Parse show inventory of each device
            inventory = net_connect.send_command(
                command_string="show inventory", use_textfsm=True
            )

        # Export interfaces to a JSON file for readability (Comment out if you don't need it)
        with open(file=f"{hostname}-inventory.json", mode="w") as outfile:
            json.dump(obj=inventory, fp=outfile, indent=4, sort_keys=True)
        # Create worksheets with the hostname of each device
        worksheet = workbook.add_worksheet(f"{hostname} Inventory")
        # Auto Filter for header line
        worksheet.autofilter("A1:E1")
        # Freeze top row and very left column only
        worksheet.freeze_panes(1, 1)

        # Header line
        header_line = {
            "A1": "Module Name",  # 1
            "B1": "Serial Number",  # 2
            "C1": "Product Identifier (PID)",  # 3
            "D1": "Version Identifier (VID)",  # 4
            "E1": "Description",  # 5
        }

        # Format header line text
        header_line_frmt = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#0058a0",
                "font_color": "#FFFFFF",
            }
        )

        # Write header line
        for key, value in header_line.items():
            worksheet.write(key, value, header_line_frmt)

        # Initial Values for row and col
        row = 1
        col = 0

        # Place data according to header line
        for item in inventory:
            worksheet.write(row, col + 0, item["name"])  # Module Name
            worksheet.write(row, col + 1, item["sn"])  # Serial Number
            worksheet.write(row, col + 2, item["pid"])  # PID
            worksheet.write(row, col + 3, item["vid"])  # VID
            worksheet.write(row, col + 4, item["descr"])  # Description

            # Jump to next row
            row += 1

print("Done")
