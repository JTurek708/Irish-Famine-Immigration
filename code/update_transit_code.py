import pandas as pd

famine_records = pd.read_csv("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/famine_records_update2.csv")

# Define mapping
transit_map = {
    'S': 'Staying in US',
    'I': 'In Transit, final destination not US',
    'T': 'Temporary Visit',
    'R': 'Return Trip to US (not a citizen)',
    'C': 'Citizen of US',
    'U': 'Unknown'
}

# Overwrite old transit code column
famine_records['transit_code'] = famine_records['transit_code'].map(transit_map).fillna('Unkown')

# Write to CSV
famine_records.to_csv("famine_records_update3.csv")
