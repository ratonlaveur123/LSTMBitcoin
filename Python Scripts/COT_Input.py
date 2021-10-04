# Names: Matan Winstok and Qianzhe Wang
# Description: This script accepts the COT data for each year, extracts BTC data, filters the dates, computes new COT inputs,
# fills in missing values, and returns a csv file with the selected data. 

import pandas as pd
import numpy as np

# Read excel files from 2018 to 2020 
data_2018 = pd.read_excel('2018.xls')
data_2019 = pd.read_excel('2019.xls')
data_2020 = pd.read_excel('2020.xls')

# Create new datasets that contains only bitcoin data from 2018 to 2020
data_2018_bitcoin = data_2018.loc[data_2018['Market_and_Exchange_Names']=='BITCOIN - CHICAGO MERCANTILE EXCHANGE']
data_2019_bitcoin = data_2019.loc[data_2019['Market_and_Exchange_Names']=='BITCOIN - CHICAGO MERCANTILE EXCHANGE']
data_2020_bitcoin = data_2020.loc[data_2020['Market_and_Exchange_Names']=='BITCOIN - CHICAGO MERCANTILE EXCHANGE']

# cConcatenate the three datasets
data = pd.concat([data_2018_bitcoin,data_2019_bitcoin,data_2020_bitcoin])

# Sort data by date in ascending order
data.sort_values(by=['As_of_Date_In_Form_YYMMDD'],ascending=True,inplace=True)

# Set 'As_of_Date_In_Form_YYMMDD' as index
data.set_index('As_of_Date_In_Form_YYMMDD',inplace=True)

# Select data from 2018-04-10 until 2020-10-13 that matches weekly BTC data 
data = data.loc[:'201013']

# Create COT input variable of percent change of dealer net position
data['Dealer_Net_Position'] = data['Dealer_Positions_Long_All'] - data['Dealer_Positions_Short_All']
data['Pct_Change_Dealer_Net_Position'] = (data['Dealer_Net_Position'] - data['Dealer_Net_Position'].shift(1)) / data['Dealer_Net_Position'].shift(1)

# Create COT input variable of percent change of lev money net position
data['Lev_Money_Net_Position'] = data['Lev_Money_Positions_Long_All'] - data['Lev_Money_Positions_Short_All']
data['Pct_Change_Lev_Money_Net_Position'] = (data['Lev_Money_Net_Position'] - data['Lev_Money_Net_Position'].shift(1)) / data['Lev_Money_Net_Position'].shift(1)

# Replace missing values with 0 due to zero division that occurs in the Pct_Change_Dealer_Net_Position column
data.fillna(0,inplace=True)

# Replace inf/-inf with values of large magnitude to represent infinity
data.replace([np.inf, -np.inf], [100,-100], inplace=True)

# Select useful COT input variables from the dataset
data = data[['Pct_of_OI_Dealer_Long_All',
                 'Pct_of_OI_Dealer_Short_All',
                 'Pct_of_OI_Lev_Money_Long_All',
                 'Pct_of_OI_Lev_Money_Short_All',
                 'Pct_Change_Dealer_Net_Position',
                 'Pct_Change_Lev_Money_Net_Position']]

# Write to csv file
data.to_csv("COT_Input.csv")

