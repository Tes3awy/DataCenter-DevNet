import json

import requests
from requests.packages import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warning
urllib3.disable_warnings(InsecureRequestWarning)

# Inputs
base_url = "https://sandboxapicdc.cisco.com:443"
username = "admin"
password = "ciscopsdt"
verify = False

# Optional (As long as using .json in the URL)
headers = {"Content-Type": "application/json"}

credentials = {
    "aaaUser": {
        "attributes": {
            "name": username,
            "pwd": password,
        }
    }
}

# POST: Request
response = requests.post(
    url=f"{base_url}/api/aaaLogin.json",
    headers=headers,
    json=credentials,
    verify=verify,
)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

# ----------------------------------------------------------------------

cookies = {}
cookies["APIC-Cookie"] = token

# GET: Request
response = requests.get(
    url=f"{base_url}/api/mo/uni.json",
    params={"query-target": "subtree", "target-subtree-class": "fvTenant"},
    headers=headers,
    cookies=cookies,
    data=None,
    verify=verify,
)

tenants = response.json()

# Export response to a JSON file
with open(file="tenants.json", mode="w") as outfile:
    json.dump(obj=tenants, fp=outfile, indent=4, sort_keys=True)

print("Done")
