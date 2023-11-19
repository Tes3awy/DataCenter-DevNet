from getpass import getpass

import requests
import urllib3
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError
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

# Create a multiple Tenants

# Use the token for subsequent requests
cookies = {"APIC-Cookie": token}

tenant_names = ["ExampleTenant1", "ExampleTenant2", "ExampleTenant3"]

tenants = [
    {
        "fvTenant": {
            "attributes": {
                "name": name,
                "descr": "Added using requests in Python",
                "nameAlias": f"{name}-Alias",
            },
        }
    }
    for name in tenant_names
]
# POST: Request
for tenant in tenants:
    try:
        response = requests.post(
            url=f"{base}/api/mo/uni.json", cookies=cookies, json=tenant, verify=False
        )
        response.raise_for_status()
    except (HTTPError, ConnectionError, ConnectTimeout) as e:
        print(e)
    else:
        print(
            f'{tenant["fvTenant"]["attributes"]["name"]} tenant was created successfully'
        )

print("Done")
