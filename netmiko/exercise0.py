# Create a connection instance to a Nexus switch
# Explicit Method
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_nxos",  # Required (cisco_nxos_telnet)
    "ip": "sbx-nxos-mgmt.cisco.com",  # Required
    "username": "admin",  # Required
    "password": "Admin_1234!",  # Required
    "secret": "",  # Optional
    "port": 8181,  # Optional
    "session_log": "nxos-exercise0.log",  # Optional
    "verbose": True,  # Optional
    "global_delay_factor": 2,  # Optional
    "fast_cli": False,  # Optional
    "conn_timeout": 15,  # Optional
}

# Create a connection instance
net_connect = ConnectHandler(**device)
output = net_connect.send_command(command_string="show version")
net_connect.disconnect()  # Disconnect from the session

print(output)

print("Done")
