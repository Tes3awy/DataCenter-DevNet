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

# Create a multiple Tenants

# Use the token for subsequent requests
cookies = {}
cookies["APIC-Cookie"] = token

tenant_names = ["ExampleTenant1", "ExampleTenant2", "ExampleTenant3"]

tenants = []

for name in tenant_names:
    tenants.append(
        {
            "fvTenant": {
                "attributes": {
                    "name": name,
                    "descr": "Added using requests in Python",
                    "nameAlias": f"{name}Alias",
                },
            }
        }
    )

# POST: Request
try:
    for tenant in tenants:
        response = requests.post(
            url=f"{base_url}/api/mo/uni.json",
            headers=headers,
            cookies=cookies,
            json=tenant,
            verify=verify,
        )

        response.raise_for_status()
        print(
            f'{tenant["fvTenant"]["attributes"]["name"]} tenant was created successfully'
        )
except HTTPError as e:
    print(e)
except ConnectionError as e:
    print(e)
except ConnectTimeout as e:
    print(e)

print("Done")
