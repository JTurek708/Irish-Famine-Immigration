import pandas as pd

# Import the updated csv - has the country names
passenger_df = pd.read_csv("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/famine_records_with_countries.csv")

# Import port codes csv
port_codes = pd.read_csv("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/code/port_codes.csv")

# Make sure port codes are 3 character strings
passenger_df['embarkation_code'] = passenger_df['embarkation_code'].astype(str).str.zfill(3)
port_codes["port_code"] = port_codes["port_code"].astype(str).str.zfill(3)


merged_df = passenger_df.merge(
    port_codes,
    left_on="embarkation_code",
    right_on="port_code",
    how="left"
)
#print(merged_df.head())
merged_df.to_csv("famine_records_update2.csv", index=False)