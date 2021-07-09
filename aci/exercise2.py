from datetime import date, datetime

import requests
import xlsxwriter
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

# POST Request
response = requests.post(
    url=f"{base_url}/api/aaaLogin.json",
    headers=headers,
    json=credentials,
    verify=verify,
)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

# ----------------------------------------------------------------------

# Use the token for subsequent requests
cookies = {}
cookies["APIC-Cookie"] = token

# GET Request
response = requests.get(
    url=f"{base_url}/api/mo/uni.json",
    params={"query-target": "subtree", "target-subtree-class": "fvTenant"},
    headers=headers,
    cookies=cookies,
    data=None,
    verify=verify,
)

tenants = response.json()

# Export Tenants to an Excel file
with xlsxwriter.Workbook(filename=f"ACI-Tenants_{date.today()}.xlsx") as workbook:
    worksheet = workbook.add_worksheet("Tenants")
    # Customizations for the sheet
    worksheet.autofilter("A1:E1")
    worksheet.freeze_panes(1, 1)

    # Header line
    header_line = {
        "A1": "Distingushed Name (DN)",  # 1
        "B1": "Name",  # 2
        "C1": "LCOwn",  # 3
        "D1": "Last Modified",  # 4
        "E1": "UID",  # 5
    }

    # Write Header line
    for cell, value in header_line.items():
        worksheet.write(cell, value)

    # Initial values for row and col
    row = 1
    col = 0

    # Iterate over tenants
    for tenant in tenants["imdata"]:
        worksheet.write(row, col + 0, tenant["fvTenant"]["attributes"]["dn"])  # 1
        worksheet.write(row, col + 1, tenant["fvTenant"]["attributes"]["name"])  # 2
        worksheet.write(row, col + 2, tenant["fvTenant"]["attributes"]["lcOwn"])  # 3
        # Convert ISO time to Human Readable time format
        mod_date = datetime.strptime(
            tenant["fvTenant"]["attributes"]["modTs"][:-6], "%Y-%m-%dT%H:%M:%S.%f"
        ).replace(microsecond=0)
        worksheet.write(row, col + 3, str(mod_date))  # 4
        worksheet.write(row, col + 4, tenant["fvTenant"]["attributes"]["uid"])  # 5

        # Jump to next row
        row += 1

print("Done")
