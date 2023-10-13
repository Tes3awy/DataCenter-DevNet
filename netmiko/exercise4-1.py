# Export Nexus device show interface command output to an Excel file
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
        "session_log": "nxos-exercise4-1-1.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.46",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-1-2.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.47",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise4-1-3.log",
        "verbose": True,
    },
]

# Create an Excel file
with xlsxwriter.Workbook(filename="Ex4-1-Nexus-Interfaces.xlsx") as wb:
    # Loop over each device
    for device in devices:
        # Connect to each device
        with ConnectHandler(**device) as net_connect:
            # Parse hostname of each device
            hostname = net_connect.send_command(
                command_string="show hostname", use_textfsm=True
            )[0]["hostname"]
            # Parse show interface of each device
            intfs = net_connect.send_command(
                command_string="show interface", use_textfsm=True
            )
        # Export interfaces to a JSON file for readability (Comment out if you don't need it)
        with open(file=f"{hostname}-intfs.json", mode="wt") as f:
            json.dump(obj=intfs, fp=f, indent=4, sort_keys=True)
        # Create worksheets with the hostname of each device
        ws = wb.add_worksheet(f"{hostname} Interfaces")
        # Auto Filter for header line
        ws.autofilter("A1:T1")
        # Freeze top row and very left column only
        ws.freeze_panes(1, 1)

        # Header line
        header_line = {
            "A1": "Interface Name",  # 1
            "B1": "IP Address",  # 2
            "C1": "Interface Type",  # 3
            "D1": "MAC Address",  # 4
            "E1": "Encapsulation",  # 5
            "F1": "BIA",  # 6
            "G1": "Last Link Flapped",  # 7
            "H1": "Link Status",  # 8
            "I1": "Admin State",  # 9
            "J1": "Input Packets",  # 10
            "K1": "Input Errors",  # 11
            "L1": "Output Packets",  # 12
            "M1": "Output Errors",  # 13
            "N1": "Speed",  # 14
            "O1": "Mode",  # 15
            "P1": "Duplex",  # 16
            "Q1": "Delay",  # 17
            "R1": "Bandwidth",  # 18
            "S1": "MTU",  # 19
            "T1": "Description",  # 20
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
            ws.write(row, col + 0, intf["interface"])  # 1
            ws.write(row, col + 1, intf["ip_address"])  # 2
            ws.write(row, col + 2, intf["hardware_type"])  # 3
            ws.write(row, col + 3, intf["address"])  # 4
            ws.write(row, col + 4, intf["encapsulation"])  # 5
            ws.write(row, col + 5, intf["bia"])  # 6
            ws.write(row, col + 6, intf["last_link_flapped"])  # 7
            ws.write(row, col + 7, intf["link_status"])  # 8
            ws.write(row, col + 8, intf["admin_state"])  # 9
            ws.write(row, col + 9, intf["input_packets"])  # 10
            ws.write(row, col + 10, intf["input_errors"])  # 11
            ws.write(row, col + 11, intf["output_packets"])  # 12
            ws.write(row, col + 12, intf["output_errors"])  # 13
            ws.write(row, col + 13, intf["speed"])  # 14
            ws.write(row, col + 14, intf["mode"])  # 15
            ws.write(row, col + 15, intf["duplex"])  # 16
            ws.write(row, col + 16, intf["delay"])  # 17
            ws.write(row, col + 17, intf["bandwidth"])  # 18
            ws.write(row, col + 18, intf["mtu"])  # 19
            ws.write(row, col + 19, intf["description"])  # 20

            # Jump to next row
            row += 1

print("Done")
