# Exercise Explanations

These Python demos depend upon some libraries (`netmiko`, `pandas`, and `XlsxWriter`). If these libs are not installed on your PC, just type:

```powershell
path\netmiko> pip install -r requirements.txt --user
```

In terminal.

---

## Exercise 0

> Shows how to initiate an SSH connection instance to a Nexus device and print its show version command output.

## Exercise 1

> Same as exercise 0, but with an improved method (Context Manager) of initiating the SSH connection and with TEXTFSM.

## Exercise 2

> Shows how to export the running configuration of a single Nexus device.

## Exercise 2-1

> Same as exercise 2, but for multiple devices.

## Exercise 3

> Shows how to save `show version` command output of a Nexus inventory to an Excel file using XlsxWriter library.

## Exercise 4

> Shows how to save `show interface brief` command output of multiple Nexus devices to an Excel file using XlsxWriter library creating separate worksheet for each Nexus device.

## Exercise 4-1

> Same as exercise 4, but for `show interface` command.

## Exercise 4-2

> Same as exercise 4, but for `show inventory` command.

## Exercise 5

> Shows how to create a configuration text file for Ethernet interfaces only.

## Exercise 6

> Shows how to backup and export the running configuration of multiple Nexus devices to text files using Pandas.

## Exercise 7

> Shows how to add repetative configuration to all Nexus switches at once, save the new configuration, and export the latter to text files.

## Exercise 8

> Shows how to shutdown all interfaces (Down + Link not connected).

## Bonus Exercise

> Shows how to export `show interface` command output to an Excel file using Pandas and Openpyxl (Same as exercise 4). (Just an illustration of using different libraries and that you are not bounded to only one right solution)
