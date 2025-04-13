import pandas as pd
import re

def parse_famine_irish_records(file_path):
    """
    Parse Famine Irish Passenger Records

    Parameters:
    ___________
    file_path : str
        Path to text file containing FIPAS

    Returns:
    ________
    pandas.DataFrame
        DataFrame containing parsed records
    """

    # Define col specifications
    colspecs = [
        (0, 20),    # Last Name
        (21, 40),   # First Name
        (40, 41),   # Family Relation Code
        (41, 44),   # Age
        (45, 46),   # Sex Code
        (47, 57),   # Occupation Code
        (57, 58),   # Literacy Code
        (58, 61),   # Native Country Code
        (62, 82),   # Town of Last Residence
        (82, 102),  # Destination
        (102, 103), # Transit Code
        (103, 105), # Travel Compartment Code
        (107, 110), # Passenger Port of Embarkation Code
        (111, 119), # CIR-MID Key
        (120, 130)  # Passenger Arrival Date
    ]
    
    # Define column names
    column_names = [
        'last_name', 'first_name', 'family_relation_code', 'age', 'sex',
        'occupation_code', 'literacy', 'country_code', 'last_residence',
        'destination', 'transit_code', 'travel_compartment', 'embarkation_code',
        'cir_mid', 'arrival_date'
    ]

    # Read the file
    df = pd.read_fwf(file_path, colspecs=colspecs, names=column_names,
                 na_values='U', keep_default_na=True)

    # Process special age codes
    def process_age(age):
        if pd.isna(age):
            return age
        age = int(age)
        if age == 900:
            return "Born at Sea"
        elif 901 <= age <= 911:
            return f"{age-900} months"
        elif age == 800:
            return None
        else:
            return age
    
    df['age'] = df['age'].apply(process_age)

    # Convert arrival date to datetime
    # The format is MM DD YYYY (cols 121-130)
    if 'arrival_date' in df.columns:
        df['arrival_date'] = pd.to_datetime(df['arrival_date'], format='%m %d %Y', errors='coerce')

    return df
