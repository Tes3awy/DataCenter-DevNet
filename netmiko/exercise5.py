# Create interfaces configuration from an Excel file
import pandas as pd

# Read the Excel file
data = pd.read_excel(io="Ex4-Nexus-Interfaces-Brief.xlsx", sheet_name=0, usecols="A")
# Convert Excel file to a data frame
df = pd.DataFrame(data)
# Convert column A to a list
intfs = df.iloc[:, 0].tolist()

intfs = [intf for intf in intfs if "Eth" in intf]
# Export a configuration file for the Ethernet interfaces
with open(file="ex5-config.txt", mode="wt") as f:
    for intf in intfs:
        # Configuration template
        f.writelines(
            [
                f"interface {intf}\n",
                " beacon\n",
                " shutdown\n",
                " exit\n",
                "!\n",
            ]
        )
    f.write("end\n")


print("Done")
