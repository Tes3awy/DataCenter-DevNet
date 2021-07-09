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
        "session_log": "nxos-exercise4.log",
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.46",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-1.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.47",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-2.log",
        "verbose": True,
    },
]

# Create an Excel file
with xlsxwriter.Workbook(filename="Ex4-Nexus-Interfaces-Brief.xlsx") as workbook:
    # Loop over each device
    for device in devices:
        # Connect to each device
        with ConnectHandler(**device) as net_connect:
            # Parse hostname of each device
            hostname = net_connect.send_command(
                command_string="show hostname", use_textfsm=True
            )[0]["hostname"]
            # Parse show interface brief of each device
            intfs = net_connect.send_command(
                command_string="show interface brief", use_textfsm=True
            )
        # Export interfaces to a JSON file for readability (Comment out if you don't need it)
        with open(file=f"{hostname}-intfs-brief.json", mode="w") as outfile:
            json.dump(obj=intfs, fp=outfile, indent=4, sort_keys=True)
        # Create worksheets with the hostname of each device
        worksheet = workbook.add_worksheet(f"{hostname} Interface Brief")
        # Auto Filter for header line
        worksheet.autofilter("A1:L1")
        # Freeze top row and very left column only
        worksheet.freeze_panes(1, 1)

        # Header line
        header_line = {
            "A1": "Interface Name",  # 1
            "B1": "IP Address",  # 2
            "C1": "Interface Type",  # 3
            "D1": "Mode",  # 4
            "E1": "VLAN",  # 5
            "F1": "Port-Channel",  # 6
            "G1": "Speed",  # 7
            "H1": "Status",  # 8
            "I1": "MTU",  # 9
            "J1": "VRF",  # 10
            "K1": "Reason",  # 11
            "L1": "Description",  # 12
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
        for intf in intfs:
            worksheet.write(row, col + 0, intf["interface"])  # Interface Name
            worksheet.write(row, col + 1, intf["ip"])  # IP
            worksheet.write(row, col + 2, intf["type"])  # Type
            worksheet.write(row, col + 3, intf["mode"])  # Mode
            worksheet.write(row, col + 4, intf["vlan"])  # VLAN
            worksheet.write(row, col + 5, intf["portch"])  # Port-Channel
            worksheet.write(row, col + 6, intf["speed"])  # Speed
            worksheet.write(row, col + 7, intf["status"])  # Status
            worksheet.write(row, col + 8, intf["mtu"])  # MTU
            worksheet.write(row, col + 9, intf["vrf"])  # VRF
            worksheet.write(row, col + 10, intf["reason"])  # Reason
            worksheet.write(row, col + 11, intf["description"])  # Description

            # Jump to next row
            row += 1

print("Done")
