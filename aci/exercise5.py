import requests
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError
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

# Create a new BD

# Use the token for subsequent requests
cookies = {}
cookies["APIC-Cookie"] = token

bd_name = "example1-domain"

bd = {
    "fvBD": {
        "attributes": {
            "name": bd_name,
            "dn": f"uni/tn-ExampleTenant1/BD-{bd_name}",
        },
        "children": [
            {
                "fvRsCtx": {
                    "attributes": {
                        "tnFvCtxName": "example-vrf",
                    }
                }
            },
            {
                "fvSubnet": {
                    "attributes": {
                        "ip": "10.10.100.1/24",
                    }
                }
            },
        ],
    }
}

# POST: Request
try:
    response = requests.post(
        url=f"{base_url}/api/mo/uni.json",
        headers=headers,
        cookies=cookies,
        json=bd,
        verify=verify,
    )

    response.raise_for_status()
except HTTPError as e:
    print(e)
except ConnectionError as e:
    print(e)
except ConnectTimeout as e:
    print(e)
else:
    if response.json()["imdata"] == []:
        print(f"{bd_name} BD was added successfully")
