import json

from urllib3.exceptions import InsecureRequestWarning

import requests
from requests.auth import HTTPBasicAuth as BasicAuth
from requests.packages import urllib3

urllib3.disable_warnings(InsecureRequestWarning)

url = "https://sbx-nxos-mgmt.cisco.com:443/ins"
username = "admin"
password = "Admin_1234!"

data = {
    "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show version",
        "output_format": "json",
    }
}

# POST: Request
response = requests.post(
    url=url,
    auth=BasicAuth(username, password),
    json=data,
    verify=False,
)

facts = response.json()

# Export facts to a JSON file
with open(file="facts.json", mode="w") as outfile:
    json.dump(obj=facts, fp=outfile, indent=4)

# --------------------------------------------------

# Store cookies in a variable to be used in subsequent requests
cookies = response.cookies.get_dict()

data = {
    "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show interface brief",
        "output_format": "json",
    }
}

# POST request
response = requests.post(
    url=url,
    cookies=cookies,  # Using cookies not auth
    json=data,
    verify=False,
)

intfs_brief = response.json()

# Export interface brief output to a JSON file
with open(file="intfs-brief-output.json", mode="w") as outfile:
    json.dump(obj=intfs_brief, fp=outfile, indent=4)

print("Done")
