import pandas as pd

# Read in port codes text file
with open("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/Irish_Port_Codes.txt", "r") as f:
    lines = f.readlines()

# Parse the lines into a list of (code, name) tuples
port_data = []
for line in lines:
    if line.strip(): # skip empty lines
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            code, name = parts
            port_data.append((code.zfill(3), name))

# Create dataframe
port_df = pd.DataFrame(port_data, columns=["port_code", "port_name"])
print(port_df)

port_df.to_csv("port_codes.csv", index=False)