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

# Create an Excel file with devices details
with xlsxwriter.Workbook("Ex3-Nexus-Devices.xlsx") as workbook:
    # The Excel sheet within the file
    worksheet = workbook.add_worksheet("Nexus Devices")

    # Customization for the sheet
    worksheet.autofilter("A1:H1")
    worksheet.freeze_panes(1, 1)

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
    for cell, value in header_line.items():
        worksheet.write(cell, value)

    # Initial values for row and col
    row = 1
    col = 0

    # Iterate over devices
    for device in devices:
        # Create a connection instance to each device
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(
                command_string="show version", use_textfsm=True
            )[0]

        # Write each value in the corresponding cell
        # according to the header line
        worksheet.write(row, col + 0, output["hostname"])  # 1
        # Notice device["ip"] not output["ip"]!!
        worksheet.write(row, col + 1, device["ip"])  # 2
        worksheet.write(row, col + 2, output["serial"])  # 3
        worksheet.write(row, col + 3, output["platform"])  # 4
        worksheet.write(row, col + 4, output["os"])  # 5
        worksheet.write(row, col + 5, output["boot_image"])  # 6
        worksheet.write(row, col + 6, output["last_reboot_reason"])  # 7
        worksheet.write(row, col + 7, output["uptime"])  # 8

        # Jump to next row
        row += 1

print("Done")
