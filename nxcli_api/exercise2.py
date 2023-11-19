# Imports
import csv
from datetime import date
from getpass import getpass

import requests
import urllib3
from numpy import sort
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

# Inputs
host = input("Host [sbx-nxos-mgmt.cisco.com]: ") or "sbx-nxos-mgmt.cisco.com"
usr = input("Username [admin]: ") or "admin"
pwd = getpass("Password: ") or "Admin_1234!"

data = {
    "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show interface transceiver",
        "output_format": "json",
    }
}

s = requests.Session()  # use session
try:
    print(f"Trying {host}...", end="\r")
    # POST: Request
    r = s.post(url=f"https://{host}:443/ins", auth=(usr, pwd), json=data, verify=False)
    r.raise_for_status()
except requests.HTTPError as e:
    raise SystemExit(e) from e
else:
    print(f"Connected to {host} successfully")
    interfaces = (
        r.json()
        .get("ins_api")
        .get("outputs")
        .get("output")
        .get("body")
        .get("TABLE_interface")
        .get("ROW_interface")
    )

    # Extract unique keys for DictWriter fieldnames
    fieldnames = sorted(set().union(*(interface.keys() for interface in interfaces)))

    # Create CSV file
    with open(
        file=f"{host}-transceivers_{date.today()}.csv", mode="wt", newline=""
    ) as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(interfaces)
    print(f"Created {csvfile.name} file successfully")
