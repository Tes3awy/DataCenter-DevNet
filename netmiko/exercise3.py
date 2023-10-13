# Export Nexus devices to an Excel file
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
        "session_log": "nxos-exercise3.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.46",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise3-2.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.47",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise3-3.log",
        "verbose": True,
    },
]

# Create an Excel file workbook for devices facts
with xlsxwriter.Workbook("Ex3-Nexus-Devices.xlsx") as wb:
    # The Excel worksheet within the file
    ws = wb.add_worksheet("Nexus Devices Facts")

    # Customization for the sheet
    ws.autofilter("A1:H1")
    ws.freeze_panes(1, 1)

    # Header line
    header_line = {
        "A1": "Hostname",  # 1
        "B1": "MGMT IP Address",  # 2
        "C1": "Serial Number",  # 3
        "D1": "Part Number",  # 4
        "E1": "OS",  # 5
        "F1": "Boot Image",  # 6
        "G1": "Last Reboot Reason",  # 7
        "H1": "Uptime",  # 8
    }

    # Write header line
    for cell, val in header_line.items():
        ws.write(cell, val)

    # Initial values for row and col
    row, col = 1, 0

    # Iterate over devices
    for device in devices:
        # Create a connection instance to each device
        with ConnectHandler(**device) as net_connect:
            facts = net_connect.send_command(
                command_string="show version", use_textfsm=True
            )[0]

        # Write each value in the corresponding cell
        # according to the header line
        ws.write(row, col + 0, facts["hostname"])  # 1
        # Notice device["ip"] not output["ip"]!!
        ws.write(row, col + 1, device["ip"])  # 2
        ws.write(row, col + 2, facts["serial"])  # 3
        ws.write(row, col + 3, facts["platform"])  # 4
        ws.write(row, col + 4, facts["os"])  # 5
        ws.write(row, col + 5, facts["boot_image"])  # 6
        ws.write(row, col + 6, facts["last_reboot_reason"])  # 7
        ws.write(row, col + 7, facts["uptime"])  # 8

        # Jump to next row
        row += 1

print("Done")
