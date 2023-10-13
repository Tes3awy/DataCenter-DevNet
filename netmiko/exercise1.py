# Create a connection instance to a Nexus switch
# Context Manager (Implicit) Method
from pprint import pprint

from netmiko import ConnectHandler

# Device to SSH into
device = {
    "device_type": "cisco_nxos",
    "ip": "sbx-nxos-mgmt.cisco.com",
    "username": "admin",
    "password": "Admin_1234!",
    "port": 8181,
    "fast_cli": False,
    "session_log": "nxos-exercise1.log",
}

# Create a connection instance using Context Manager
with ConnectHandler(**device) as conn:
    # Use TEXTFSM to parse the show version command output
    output = conn.send_command(command_string="show version", use_textfsm=True)

pprint(output)
print("Done")
