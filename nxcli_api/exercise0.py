import json

import requests
from requests.auth import HTTPBasicAuth as BasicAuth
from requests.packages import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

url = "https://sbx-nxos-mgmt.cisco.com:443/ins"
username = "admin"
password = "Admin_1234!"

data = {
    "ins_api": {
        "version": "1.0",
        # Possible values:
        # 1- cli_show
        # 2- cli_show_array (For multiple show commands at once)
        # 3- cli_show_ascii
        # 4- cli_conf
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show vlan brief",  # any command
        "output_format": "json",  # or XML
    }
}

# POST: Request
response = requests.post(
    url=url,
    auth=BasicAuth(username, password),
    json=data,
    verify=False,
)

vlan_brief = response.json()

# Export response to a JSON file
with open(file="vlan-brief-output.json", mode="w") as outfile:
    json.dump(obj=vlan_brief, fp=outfile, indent=4)

print("Done")
