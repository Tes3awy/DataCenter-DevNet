![Cisco DevNet](https://img.shields.io/badge/Cisco-DevNet-blue)
[![Tested on Python 3.9.6](https://img.shields.io/badge/Python%203.6+-white.svg?logo=python)](https://www.python.org/downloads)
![Language](https://img.shields.io/github/languages/top/Tes3awy/DataCenter-DevNet)
[![Visual Studio Code](https://img.shields.io/badge/1.58.0-blue.svg?logo=visual-studio-code)](https://code.visualstudio.com/)
[![Issues Open](https://img.shields.io/github/issues/Tes3awy/DataCenter-DevNet)](https://github.com/Tes3awy/DataCenter-DevNet/issues)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/Tes3awy/DataCenter-DevNet)](https://github.com/Tes3awy/DataCenter-DevNet/commits/main)
![Last Commit](https://img.shields.io/github/last-commit/Tes3awy/DataCenter-DevNet)
[![Code Size](https://img.shields.io/github/languages/code-size/Tes3awy/DataCenter-DevNet?color=green)](https://github.com/Tes3awy/DataCenter-DevNet)
[![License](https://img.shields.io/github/license/Tes3awy/DataCenter-DevNet)](https://github.com/Tes3awy/DataCenter-DevNet/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Cisco DevNet for Data Center Engineers

## Table of Contents

1. [Getting Started](#getting-started)
2. [Documentation Links](#documentation-links)

---

### Getting Started

1. `Clone` this repo or `Download ZIP` by clicking on `Code` up above.
   _(Alternativley, you can click on Releases on the right hand side and download the latest release)_

2. Once downloaded, extract the ZIP file and `cd` into `aci`, `nxcli_api` or `netmiko` folder.

3. Open `requirements.txt` file and if any of the libraries is not installed on your PC, run the following command in the PowerShell terminal within VSCode:

```powershell
path_to\folder> pip install -r requirements.txt --user ↵
```

4. Explore each `exercise*.py` file. _**(where **\*** is the number of the exercise)**_

5. Run any Python exercise by typing the following command in PowerShell terminal in VSCode:

```powershell
path_to\folder> python exercise*.py ↵
```

---

### Documentation Links

Examples in `aci`, `netmiko`, and `nxcli_api` folders use some Python libraries. These libraries are:

1. Netmiko **v3.4.0** (Multi-vendor library to simplify Paramiko SSH connections to network devices) [Documentation Link](https://github.com/ktbyers/netmiko/blob/develop/README.md).
2. NTC Templates **v2.1.0** (TextFSM templates for parsing show commands of network devices) [Documentation Link](https://github.com/networktocode/ntc-templates).
3. XlsxWriter **v1.4.4** (XlsxWriter is a Python module for creating Excel XLSX files) [Documentation Link](https://xlsxwriter.readthedocs.io/).
4. Pandas **v1.3.0** (Data Analysis Library) [Documentation Link](https://pandas.pydata.org/docs/).
5. Openpyxl **v3.0.7** (A Python library to read/write Excel 2010 xlsx/xlsm files) [Documentation Link](https://openpyxl.readthedocs.io/en/stable/).
6. Requests **v2.25.1** (HTTP Requests) [Documentation Link](https://docs.python-requests.org/en/master/).
