# Shutdown all Link not connected interfaces
# Must run Exercise 3 first
import pandas as pd

from netmiko import ConnectHandler

# Read Excel file
data = pd.read_excel(io="Ex3-Nexus-Devices.xlsx", sheet_name=0, usecols="B")
# Convert Excel file to DataFrame
df = pd.DataFrame(data)

ips = df.iloc[:, 0].tolist()  # If NOT usecols="B", then replace 0 with 1

devices = [
    {
        "device_type": "cisco_nxos",
        "ip": ip,
        "username": "admin",
        "password": "Admin_1234!",
        "port": 8181,
        "fast_cli": False,
        "session_log": f"{ip}-nxos-exercise8.log",
    }
    for ip in ips
]

# Iterate over devices
for device in devices:
    # Create a connection instance
    with ConnectHandler(**device) as conn:
        # Parse the hostname of the device
        hostname = conn.send_command(command_string="show hostname", use_textfsm=True)[
            0
        ]["hostname"]
        # Parse the interface brief of the  device
        down_intfs = conn.send_command(
            command_string="show interface brief", use_textfsm=True
        )

        cfg = ""
        for down_intf in down_intfs:
            if (
                "Eth" in down_intf["interface"]
                and "Link not connected" in down_intf["reason"]
            ):
                cfg_template = f"""\
                interface {down_intf["interface"]}
                 shutdown
                 exit
                 !
                """
                cfg += cfg_template

        # Export shutdown template to a text file
        cfg_fname = f"Ex6-1-{hostname}-shutdown-intfs.txt"
        with open(file=f"{cfg_fname}", mode="wt") as f:
            f.writelines([cfg, "end", "\n"])

        # Send the new config to each device
        send_cfg = conn.send_config_from_file(config_file=f"{cfg_fname}")

        # Save the new config
        send_cfg += conn.save_config()

print("Done")
