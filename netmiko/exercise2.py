# Export Nexus configuration to a text file
from netmiko import ConnectHandler

# Device to SSH into
device = {
    "device_type": "cisco_nxos",
    "ip": "sbx-nxos-mgmt.cisco.com",
    "username": "admin",
    "password": "Admin_1234!",
    "port": 8181,
    "fast_cli": False,
    "session_log": "nxos-exercise2.log",
}

# Create a connection instance
with ConnectHandler(**device) as net_connect:
    # Parse hostname of the device
    hostname = net_connect.send_command(
        command_string="show version", use_textfsm=True
    )[0]["hostname"]
    # Parse running configuration of the device
    run_cfg = net_connect.send_command(command_string="show running-config")

# Save running config to a text file with the hostname of the device
with open(file=f"{hostname}_run-cfg-ex2.txt", mode="wt") as f:
    f.write(run_cfg.lstrip())

print("Done")
