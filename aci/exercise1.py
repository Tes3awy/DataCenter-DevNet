import json

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warning
urllib3.disable_warnings(InsecureRequestWarning)

# Inputs
base = "https://sandboxapicdc.cisco.com:443"
username = "admin"
password = "!v3G@!4@Y"

payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}

# POST: Request
response = requests.post(url=f"{base}/api/aaaLogin.json", json=payload, verify=False)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

# ----------------------------------------------------------------------

cookies = {"APIC-Cookie": token}
# GET: Request
response = requests.get(
    url=f"{base}/api/mo/uni.json",
    params={"query-target": "subtree", "target-subtree-class": "fvTenant"},
    cookies=cookies,
    verify=False,
)

tenants = response.json()

# Export response to a JSON file
with open(file="tenants.json", mode="wt") as outfile:
    json.dump(obj=tenants, fp=outfile, indent=4, sort_keys=True)
print(f"Created {outfile.name}")

print("Done")
