import pandas as pd

def parse_country_codes(file_path): 
    """
    This function parses the country codes into a pandas DataFrame.

    Parameters:
    ------------
    file_path: str
        Path to the text file containing the country codes
    
    Returns:
    ------------
    pandas.DataFrame
        DataFrame containing the country codes and names    
    """
    # Read the text file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process each line
    countries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split line to separate code and country name
        # Format is: "0003 IRELAND"
        parts = line.split(' ', 1)
        if len(parts) == 2:
            code = parts[0].strip()
            country = parts[1].strip()
            countries.append({'code': int(code), 'country': country})

    # Create the Data Frame
    country_df = pd.DataFrame(countries)

def update_passenger_data_with_countries(passenger_df, country_df):
    """
    Update the passenger DataFrame with country names based on country codes.
    
    Parameters:
    -----------
    passenger_df : pandas.DataFrame
        DataFrame containing passenger records with country_code column
    country_df : pandas.DataFrame
        DataFrame containing country codes and names
        
    Returns:
    --------
    pandas.DataFrame
        Updated passenger DataFrame with country names
    """
    # Create a dictionary mapping codes to country names
    country_dict = dict(zip(country_df['code'], country_df['country']))
    
    # Add a new column with country names
    passenger_df['country_name'] = passenger_df['country_code'].map(country_dict)
    
    return passenger_df

if __name__ == "__main__":
    # Parse country codes
    country_file = "Irish_Country_Codes.txt"
    country_df = parse_country_codes(country_file)
    
    print("Country codes parsed successfully:")
    print(country_df.head())
    
    # Save to CSV
    country_df.to_csv("country_codes.csv", index=False)
    print("\nCountry codes saved to country_codes.csv")
    
    # Example of how to update passenger data
    try:
        # Try to load existing passenger data
        passenger_df = pd.read_csv("famine_records.csv")
        
        # Update with country names
        passenger_df = update_passenger_data_with_countries(passenger_df, country_df)
        
        # Save updated passenger data
        passenger_df.to_csv("famine_records_with_countries.csv", index=False)
        print("\nPassenger data updated with country names and saved to famine_records_with_countries.csv")
    except FileNotFoundError:
        print("\nPassenger data file not found. Run the passenger data parsing script first.")