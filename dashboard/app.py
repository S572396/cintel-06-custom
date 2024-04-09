import pandas as pd

infile = r"C:\Users\19564\Documents\cintel-06-custom\cintel-06-custom\dashboard\Electric_Vehicle_Population_Data_20240406 (2).csv"

try:
    df = pd.read_csv(infile)
    print(df.head())
    # return df  # Commenting out return as it might cause issues in this context
except Exception as e:
    print(f"Error reading file: {e}")
    # return None  # Commenting out return as it might cause issues in this context










