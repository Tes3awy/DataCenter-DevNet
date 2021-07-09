# Shutdown all Link not connected interfaces
# Must run Exercise 3 first
import pandas as pd

from netmiko import ConnectHandler

# Read Excel file
data = pd.read_excel(io="Ex3-Nexus-Devices.xlsx", sheet_name=0, usecols="B")
# Convert Excel file to DataFrame
df = pd.DataFrame(data)

ips = df.iloc[:, 0].tolist()  # If NOT usecols="B", then replace 0 with 1

# Append IP to the dictionary template from the Excel file
devices = []
for ip in ips:
    devices.append(
        {
            "device_type": "cisco_nxos",
            "ip": ip,
            "username": "admin",
            "password": "Admin_1234!",
            "port": 8181,
            "fast_cli": False,
            "session_log": f"{ip}-nxos-exercise8.log",
        }
    )

# Iterate over devices
for device in devices:
    # Create a connection instance
    with ConnectHandler(**device) as net_connect:
        # Parse the hostname of the device
        hostname = net_connect.send_command(
            command_string="show hostname", use_textfsm=True
        )[0]["hostname"]
        # Parse the interface brief of the  device
        down_intfs = net_connect.send_command(
            command_string="show interface brief",
            use_textfsm=True,
        )

        cfg = ""
        for down_intf in down_intfs:
            if (
                "Eth" in down_intf["interface"]
                and "Link not connected" in down_intf["reason"]
            ):
                template = f'interface {down_intf["interface"]}\n shutdown\nexit\n!\n'
                cfg += template

        # Export shutdown template to a text file
        cfg_fname = f"Ex6-1-{hostname}-shutdown-intfs.txt"
        with open(file=f"{cfg_fname}", mode="w") as outfile:
            outfile.write(cfg.lstrip())

        # Send the new config to each device
        send_cfg = net_connect.send_config_from_file(config_file=f"{cfg_fname}")

        # Save the new config
        send_cfg += net_connect.save_config()

print("Done")
