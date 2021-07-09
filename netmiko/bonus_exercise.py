# Export Nexus devices show interface command output to an Excel file
# Using Pandas and Openpyxl as its engine

import uuid  # Unique Universal IDentifier

import openpyxl
import pandas as pd

from netmiko import ConnectHandler

# Devices to SSH into
devices = [
    {
        "device_type": "cisco_nxos",
        "ip": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
        "port": 8181,
        "session_log": "bonus_exercise-device-1.log",
        "fast_cli": False,
        "conn_timeout": 15,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
        "port": 8181,
        "session_log": "bonus_exercise-device-2.log",
        "fast_cli": False,
        "conn_timeout": 15,
    },
]

# Check if the Excel file already exists and re-create it
excel_file_name = "Ex4-2-Nexus-Interfaces.xlsx"
workbook = openpyxl.Workbook(excel_file_name)
workbook.save(excel_file_name)
print(f"Created {excel_file_name} workbook")

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

    # Create a data frame from the ouput list
    df = pd.DataFrame(intfs)

    # Export the df automatically to an Excel file
    with pd.ExcelWriter(excel_file_name, engine="openpyxl", mode="a") as writer:
        df.to_excel(
            writer,  # The Excel file as a variable
            index=False,  # Remove the automatically generated first index column
            sheet_name=f"{str(uuid.uuid4())[0:8]}",  # 8 random characters
            verbose=True,  # show verbose output for errors ONLY
            freeze_panes=(1, 1),  # freeze top row & most left column
        )

# Read the created Excel file
workbook = openpyxl.load_workbook(excel_file_name)
# Grab the automatically created sheet
sheet = workbook["Sheet"]
# Remove the automatically generated sheet
workbook.remove(sheet)
# Close the workbook
workbook.save(excel_file_name)

print("Done")
