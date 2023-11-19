from datetime import date, datetime
from getpass import getpass

import requests
import urllib3
import xlsxwriter
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warning
urllib3.disable_warnings(InsecureRequestWarning)

# Inputs
apic = input("APIC [sandboxapicdc.cisco.com]: ") or "sandboxapicdc.cisco.com"
base = f"https://{apic}:443"
username = input("Username [admin]: ") or "admin"
password = getpass("Password: ") or "!v3G@!4@Y"

payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}

# POST Request
response = requests.post(url=f"{base}/api/aaaLogin.json", json=payload, verify=False)

token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

# ----------------------------------------------------------------------

# Use the token for subsequent requests
cookies = {"APIC-Cookie": token}
# GET Request
response = requests.get(
    url=f"{base}/api/mo/uni.json",
    params={"query-target": "subtree", "target-subtree-class": "fvTenant"},
    cookies=cookies,
    verify=False,
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
        "A1": "Name",  # 2
        "B1": "Distingushed Name (DN)",  # 1
        "C1": "LCOwn",  # 3
        "D1": "Last Modified",  # 4
        "E1": "UID",  # 5
    }

    # Write Header line
    for cell, val in header_line.items():
        worksheet.write(cell, val)

    # Initial value for column
    col = 0

    # Iterate over tenants
    for row, tenant in enumerate(tenants["imdata"], start=1):
        worksheet.write(row, col + 0, tenant["fvTenant"]["attributes"]["name"])  # 1
        worksheet.write(row, col + 1, tenant["fvTenant"]["attributes"]["dn"])  # 2
        worksheet.write(row, col + 2, tenant["fvTenant"]["attributes"]["lcOwn"])  # 3
        # Convert ISO time to Human Readable time format
        mod_date = datetime.strptime(
            tenant["fvTenant"]["attributes"]["modTs"][:-6], "%Y-%m-%dT%H:%M:%S.%f"
        ).replace(microsecond=0)
        worksheet.write(row, col + 3, str(mod_date))  # 4
        worksheet.write(row, col + 4, tenant["fvTenant"]["attributes"]["uid"])  # 5

print("Done")
