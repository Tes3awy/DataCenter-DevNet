# Add same configuration to all Nexus switches
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
        "session_log": "nxos-exercise7.log",
    }
]

# Loop through devices
for device in devices:
    # Create a connection instance
    with ConnectHandler(**device) as conn:
        # Parse hostname of the device
        hostname = conn.send_command(command_string="show hostname", use_textfsm=True)[
            0
        ]["hostname"]
        # Send config from text file (or Use ex5-config.txt)
        output = conn.send_config_from_file(config_file="ex7-config.txt")
        # And save configuration
        output += conn.save_config()

        # Parse the new running configuration
        run_cfg = conn.send_command(command_string="show running-config")

    # Export the new running-config of each device to a text file
    with open(file=f"{hostname}-run_cfg-ex7.txt", mode="wt") as f:
        f.write(run_cfg.lstrip())

print("Done")
