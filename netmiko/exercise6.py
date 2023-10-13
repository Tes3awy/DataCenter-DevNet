# Backup configuration from reading the Excel file using Pandas
import pandas as pd

from netmiko import ConnectHandler

# Read the Excel file # or remove usecols="B"
data = pd.read_excel(io="Ex3-Nexus-Devices.xlsx", sheet_name=0, usecols="B")
# Convert Excel file to a data frame
df = pd.DataFrame(data)
# Convert column B to a list
ip_addrs = df.iloc[:, 0].tolist()  # If NOT usecols="B", then replace 0 with 1

devices = [
    {
        "device_type": "cisco_nxos",
        "ip": ip,
        "username": "admin",
        "password": "Admin_1234!",
        "port": 8181,
        "fast_cli": False,
        "session_log": f"{ip}.log",
    }
    for ip in ip_addrs
]

# Iterate over devices
for device in devices:
    # Create a connection instance
    with ConnectHandler(**device) as conn:
        # Parse the hostname of the device
        hostname = conn.send_command(command_string="show hostname", use_textfsm=True)[
            0
        ]["hostname"]
        # Parse the running-config of the device
        run_cfg = conn.send_command(command_string="show running-config")

    # Export the running configuration of each device to a text file
    with open(file=f"{hostname}-run_cfg-ex6.txt", mode="wt") as f:
        f.write(run_cfg.lstrip())

print("Done")
