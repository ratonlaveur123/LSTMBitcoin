# Names: Matan Winstok and Qianzhe Wang
# Description: This script converts the daily BTC data to a weekly basis. It uses Pandas to aggregate each column to a weekly
# basis. 


# Import libraries
import pandas as pd

# Import the data
df = pd.read_csv('btc_dataset.csv', parse_dates=['Date'], index_col=['Date'])

# Make the hash_rate column numeric (necessary for aggregation)
df['hash_rate'] = df['hash_rate'].astype('float')

# Only select a subset of the data that lines up with the COT data dates
# Note: it should start 1 week earlier than the COT data so that when we aggregate by week the 
# first weekly BTC date aligns with the COT value for that week. COT data starts Tuesday April 10, 2018 
# so we will use data starting from Tuesday April 3, 2018
df = df.loc['2018-04-03' : ]

# Now we want to aggregate the daily data to weekly data:
output_df = df.resample('W-TUE').agg({'Closing Price (USD)':'last', 'active_addresses':'sum', 'hash_rate': 'mean', 
											  'btc_left':'last', 'total_addresses':'last', 'difficulty':'last', 
                                              'total_fees': 'sum', 'fed_assets': 'last', 'GLD':'last', 'IYE':'last', 
                                              'SLV':'last', 'SPY':'last', 'TLT':'last', 
                                              'UUP':'last', 'NYFed_inflation':'last', 'Google_popularity':'last'} )

# Note: COT data is collected at the end of day each Tuesday at which point data collection starts for the next week's COT report
# For the data above, we start collecting from Wednesday April 4 -> Tuesday April 10 which is the first week of collection. 
# Then it restarts data collection from April 11-17, etc. 

# Can ignore the value at 2018-04-03:
output_df = output_df.loc['2018-04-10' : ]

# Save to csv 
output_df.to_csv('Weekly_BTC.csv')