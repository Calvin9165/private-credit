import pandas as pd
import matplotlib.pyplot as plt

# High Yield Spread Data
# source: https://fred.stlouisfed.org/series/BAMLH0A0HYM2
spread_path = 'HY Spread Data.csv'
spread_df = pd.read_csv(spread_path)

# setting date column to datetime object and to the index of dataframe
spread_df['DATE'] = pd.to_datetime(spread_df['DATE'], dayfirst=False)
spread_df.set_index('DATE', inplace=True)

# df['Spread'] = pd.to_numeric(df['Spread'])

# Removing the periods, ".", and converting them to nonetypes
spread_df.loc[spread_df['Spread'] == '.'] = None

# switching the spread value from string to float
spread_df['Spread'] = pd.to_numeric(spread_df['Spread'])

# if value is None type, then fill forward with most recent value
spread_df.fillna(method='ffill', inplace=True)

# 200 day moving average on spread data
spread_df['rolling spread'] = spread_df['Spread'].rolling(200).mean()

# Cliffwater Direct Lending Data
# source: http://www.cliffwaterdirectlendingindex.com/
cd_path = 'CliffWater Direct Lending Index.csv'
cd_df = pd.read_csv(cd_path)

# Changing the column title "Unnamed: 0" to "Date"
cd_df.rename({'Unnamed: 0': 'Date'}, axis=1, inplace=True)
cd_df['Date'] = pd.to_datetime(cd_df['Date'])
cd_df.set_index('Date', inplace=True)

# High Yield Bond ETF (HYG) Data
# source: https://www.ishares.com/us/products/239565/ishares-iboxx-high-yield-corporate-bond-etf#/
hyg_path = 'HYG Data.csv'
hyg_df = pd.read_csv('HYG Data.csv')

hyg_df['Date'] = pd.to_datetime(hyg_df['Date'])
hyg_df.set_index('Date', inplace=True)

# Treasury Bond ETF (SHV) Data
# source https://www.ishares.com/us/products/239466/ishares-short-treasury-bond-etf#/
tbill_path = 'SHV Data.csv'
tbill_df = pd.read_csv(tbill_path)
tbill_df['Date'] = pd.to_datetime(tbill_df['Date'])
tbill_df.set_index('Date', inplace=True)

# remove the index level and shares outstanding column
tbill_df.drop(['Index Level', 'Shares Outstanding'], axis=1, inplace=True)

# set the deafult value of '--' where no dividend is paid to 0 instead
tbill_df.loc[tbill_df['Ex-Dividends'] == '--', 'Ex-Dividends'] = 0

# setting the values in the dataframe to numbers instead of strings
for column in tbill_df.columns:

    tbill_df[column] = pd.to_numeric(tbill_df[column])

# # really good line of code and could be used to replace the signal column for some of the previous
# # moving average strategies
# tbill_df.loc[tbill_df['Ex-Dividends'] < tbill_df['NAV per Share'], 'test'] = 'heyo'


if __name__ == '__main__':

    pass

