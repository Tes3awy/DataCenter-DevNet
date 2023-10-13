# Create a connection instance to a Nexus switch
# Explicit Method
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_nxos",  # Required
    "ip": "sbx-nxos-mgmt.cisco.com",  # Required
    "username": "admin",  # Required
    "password": "Admin_1234!",  # Required
    "secret": "",  # Optional
    "port": 8181,  # Optional
    "session_log": "nxos-exercise0.log",  # Optional
    "verbose": True,  # Optional
    "fast_cli": False,  # Optional
    "conn_timeout": 15,  # Optional
}

# Create a connection instance
conn = ConnectHandler(**device)
output = conn.send_command(command_string="show version")
conn.disconnect()  # Disconnect from the session (Clear line VTY)

print(output)

print("Done")
