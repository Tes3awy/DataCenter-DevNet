# Create interfaces configuration from an Excel file
import pandas as pd

# Read the Excel file
data = pd.read_excel(io="Ex4-Nexus-Interfaces-Brief.xlsx", sheet_name=0, usecols="A")
# Convert Excel file to a data frame
df = pd.DataFrame(data)
# Convert column A to a list
interfaces = df.iloc[:, 0].tolist()

# Define an empty list to hold all Ethernet interfaces
intfs = []

# Filter out any interface other than Ethernet interface
for interface in interfaces:
    if "Eth" in interface:
        intfs.append(interface)

# Export a configuration file for the Ethernet interfaces
with open(file="ex5-config.txt", mode="w") as outfile:
    for intf in intfs:
        # Configuration template
        cfg = f"interface {intf}\n beacon \n shutdown\nexit\n!\n"
        outfile.write(cfg.lstrip())


print("Done")
