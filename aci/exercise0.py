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


# Request
response = requests.post(url=f"{base}/api/aaaLogin.json", json=payload, verify=False)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

print(token)
