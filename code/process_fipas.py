from parse_fipas_file import parse_famine_irish_records
import pandas as pd
import re

if __name__ == "__main__":
    # Replace with the actual path to your FIPAS file
    file_path = "path/to/your/FIPAS.txt"

df = parse_famine_irish_records('/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/Famine_Irish_Passengers.txt')



print(f"Records processed: {len(df)}")

# Save to CSV
output_path = "/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/famine_records.csv"
df.to_csv(output_path, index=False)
print(f"\nData saved to {output_path}")