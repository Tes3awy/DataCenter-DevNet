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
with xlsxwriter.Workbook(filename="Ex4-1-Nexus-Interfaces.xlsx") as workbook:
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
        with open(file=f"{hostname}-intfs.json", mode="w") as outfile:
            json.dump(obj=intfs, fp=outfile, indent=4, sort_keys=True)
        # Create worksheets with the hostname of each device
        worksheet = workbook.add_worksheet(f"{hostname} Interfaces")
        # Auto Filter for header line
        worksheet.autofilter("A1:T1")
        # Freeze top row and very left column only
        worksheet.freeze_panes(1, 1)

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
        for cell, value in header_line.items():
            worksheet.write(cell, value, header_line_frmt)

        # Initial Values for row and col
        row = 1
        col = 0

        # Place data according to header line
        for intf in intfs:
            worksheet.write(row, col + 0, intf["interface"])  # 1
            worksheet.write(row, col + 1, intf["ip_address"])  # 2
            worksheet.write(row, col + 2, intf["hardware_type"])  # 3
            worksheet.write(row, col + 3, intf["address"])  # 4
            worksheet.write(row, col + 4, intf["encapsulation"])  # 5
            worksheet.write(row, col + 5, intf["bia"])  # 6
            worksheet.write(row, col + 6, intf["last_link_flapped"])  # 7
            worksheet.write(row, col + 7, intf["link_status"])  # 8
            worksheet.write(row, col + 8, intf["admin_state"])  # 9
            worksheet.write(row, col + 9, intf["input_packets"])  # 10
            worksheet.write(row, col + 10, intf["input_errors"])  # 11
            worksheet.write(row, col + 11, intf["output_packets"])  # 12
            worksheet.write(row, col + 12, intf["output_errors"])  # 13
            worksheet.write(row, col + 13, intf["speed"])  # 14
            worksheet.write(row, col + 14, intf["mode"])  # 15
            worksheet.write(row, col + 15, intf["duplex"])  # 16
            worksheet.write(row, col + 16, intf["delay"])  # 17
            worksheet.write(row, col + 17, intf["bandwidth"])  # 18
            worksheet.write(row, col + 18, intf["mtu"])  # 19
            worksheet.write(row, col + 19, intf["description"])  # 20

            # Jump to next row
            row += 1

print("Done")
