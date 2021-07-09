# Export Nexus configuration of multiple devices to a text file
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
        "session_log": "nxos-exercise2-1.log",
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.46",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise2-2.log",
        "verbose": True,
    },
    {
        "device_type": "cisco_nxos",
        "ip": "192.168.90.47",
        "username": "admin",
        "password": "P@ssw0rd",
        "fast_cli": False,
        "session_log": "nxos-exercise2-3.log",
        "verbose": True,
    },
]

for device in devices:
    # Create a connection instance
    with ConnectHandler(**device) as net_connect:
        # Parse hostname of the device
        hostname = net_connect.send_command(
            command_string="show version", use_textfsm=True
        )[0]["hostname"]
        # Parse running configuration of the device
        run_cfg = net_connect.send_command(command_string="show running-config")

    # Save running config to a text file with the hostname of the device
    with open(file=f"{hostname}_run-cfg-ex2-1.txt", mode="w") as outfile:
        outfile.write(run_cfg.lstrip())

print("Done")
