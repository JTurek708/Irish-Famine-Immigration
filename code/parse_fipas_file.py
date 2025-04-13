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
    