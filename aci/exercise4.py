from getpass import getpass

import requests
import urllib3
from requests.exceptions import ConnectionError, HTTPError
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warning
urllib3.disable_warnings(InsecureRequestWarning)

# Inputs
apic = input("APIC [sandboxapicdc.cisco.com]: ") or "sandboxapicdc.cisco.com"
base = f"https://{apic}:443"
username = input("Username [admin]: ") or "admin"
password = getpass("Password: ") or "!v3G@!4@Y"

payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}

# POST: Request
response = requests.post(url=f"{base}/api/aaaLogin.json", json=payload, verify=False)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

# ----------------------------------------------------------------------

# Create a new VRF

# Use the token for subsequent requests
cookies = {"APIC-Cookie": token}
vrf = {
    "fvCtx": {
        "attributes": {"name": "example-vrf"},
    }
}

# POST: Request
try:
    response = requests.post(
        url=f"{base}/api/mo/uni/tn-ExampleTenant1.json",
        cookies=cookies,
        json=vrf,
        verify=False,
    )
    response.raise_for_status()
    print(response.json())
except (HTTPError, ConnectionError) as e:
    print(e)
else:
    if response.status_code == 200 and response.json()["imdata"] == []:
        print("VRF added successfully")

print("Done")
