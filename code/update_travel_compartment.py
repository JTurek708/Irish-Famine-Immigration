import pandas as pd

famine_records = pd.read_csv("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/famine_records_update3.csv",
    low_memory=False)
print(famine_records['travel_compartment'].dtype)

# Normalize to two-char strings
famine_records['travel_compartment'] = (
    famine_records['travel_compartment'].astype(str).str.zfill(2)
)

# Define mapping
compartment_map = {
    '09': 'Cabin',
    '13': 'Steerage',
    '15': 'Stowaway',
    'U': 'Unkown'
}

# Overwrite old travel_compartment code column
famine_records['travel_compartment'] = famine_records['travel_compartment'].map(compartment_map).fillna('Unkown')

# Write to CSV
famine_records.to_csv("famine_records_update4.csv")