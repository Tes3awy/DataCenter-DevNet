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
with xlsxwriter.Workbook(filename="Ex4-Nexus-Interfaces-Brief.xlsx") as wb:
    # Loop over each device
    for device in devices:
        # Connect to each device
        with ConnectHandler(**device) as conn:
            # Parse hostname of each device
            hostname = conn.send_command(
                command_string="show hostname", use_textfsm=True
            )[0]["hostname"]
            # Parse show interface brief of each device
            intfs = conn.send_command(
                command_string="show interface brief", use_textfsm=True
            )

        # Export interfaces to a JSON file for readability (Comment out if you don't need it)
        with open(file=f"{hostname}-intfs-brief.json", mode="wt") as f:
            json.dump(obj=intfs, fp=f, indent=4, sort_keys=True)

        # Create worksheets with the hostname of each device
        ws = wb.add_worksheet(f"{hostname} Interface Brief")
        # Auto Filter for header line
        ws.autofilter("A1:L1")
        # Freeze top row and very left column only
        ws.freeze_panes(1, 1)

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
        for intf in intfs:
            ws.write(row, col + 0, intf["interface"])  # Interface Name
            ws.write(row, col + 1, intf["ip"])  # IP
            ws.write(row, col + 2, intf["type"])  # Type
            ws.write(row, col + 3, intf["mode"])  # Mode
            ws.write(row, col + 4, intf["vlan"])  # VLAN
            ws.write(row, col + 5, intf["portch"])  # Port-Channel
            ws.write(row, col + 6, intf["speed"])  # Speed
            ws.write(row, col + 7, intf["status"])  # Status
            ws.write(row, col + 8, intf["mtu"])  # MTU
            ws.write(row, col + 9, intf["vrf"])  # VRF
            ws.write(row, col + 10, intf["reason"])  # Reason
            ws.write(row, col + 11, intf["description"])  # Description

            # Jump to next row
            row += 1

print("Done")
