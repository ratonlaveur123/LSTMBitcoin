# Description: This script merges the weekly BTC data and the COT input data based on dates as the index. 

import pandas as pd

# Read both csv files into Pandas dataframes
a = pd.read_csv('Weekly_BTC.csv')
b = pd.read_csv('COT_Input.csv')

# Merge the two dataframes
merged = a.merge(b,how='outer',left_index=True,right_index=True)

# Drop this column as it is not necessary
merged.drop('As_of_Date_In_Form_YYMMDD',axis=1,inplace=True)

# Set the index
merged.set_index('Date',inplace=True)

# Save to csv file
merged.to_csv('merged.csv')

