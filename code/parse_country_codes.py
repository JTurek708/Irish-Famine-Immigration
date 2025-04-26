import pandas as pd

def parse_country_codes(file_path):
    """
    Parse the Irish Country Codes file into a pandas DataFrame.
    
    Parameters:
    -----------
    file_path : str
        Path to the text file containing country codes
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the country codes and names
    """
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Process each line
        countries = []
        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            
            # Split the line to separate code and country name
            # Format is: "003 IRELAND"
            parts = line.split(' ', 1)  # Split at first space
            if len(parts) == 2:
                code = parts[0].strip()
                country = parts[1].strip()
                countries.append({'code': int(code), 'country': country})
        
        # Create DataFrame
        country_df = pd.DataFrame(countries)
        
        return country_df
    
    except Exception as e:
        print(f"Error parsing country codes: {e}")
        # Print the file content for debugging
        print("\nFile content:")
        try:
            with open(file_path, 'r') as f:
                print(f.read())
        except:
            print("Could not read file")
        return pd.DataFrame()  # Return empty DataFrame instead of None

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
    country_file = "/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/Irish_Country_Codes.txt"
    
    # Check if file exists
    import os
    if not os.path.isfile(country_file):
        print(f"Error: File '{country_file}' not found.")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure the file exists and the path is correct.")
        exit(1)
    
    country_df = parse_country_codes(country_file)
    
    if country_df.empty:
        print("Failed to parse country codes. Exiting.")
        exit(1)
    
    print("Country codes parsed successfully:")
    print(country_df.head())
    
    # Save to CSV
    country_df.to_csv("country_codes.csv", index=False)
    print("\nCountry codes saved to country_codes.csv")
    
    # Example of how to update passenger data
    try:
        # Try to load existing passenger data
        passenger_df = pd.read_csv("/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/famine_records.csv")
        
        # Update with country names
        passenger_df = update_passenger_data_with_countries(passenger_df, country_df)
        
        # Save updated passenger data
        passenger_df.to_csv("famine_records_with_countries.csv", index=False)
        print("\nPassenger data updated with country names and saved to famine_records_with_countries.csv")
    except FileNotFoundError:
        print("\nPassenger data file not found. Run the passenger data parsing script first.")