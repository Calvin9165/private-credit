from loading_data import hyg_df, cd_df

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import sqrt

hyg_df['nav % change'] = hyg_df['NAV per Share'].pct_change()
hyg_df['income % gain'] = hyg_df['Ex-Dividends'] / hyg_df['NAV per Share']
hyg_df['total return'] = hyg_df['nav % change'] + hyg_df['income % gain']

# hyg_perf = ((hyg_df['total return'] + 1).cumprod() * 10000)

cd_df.fillna(0, inplace=True)
cd_df['Total Return'] = cd_df['Total Return'].apply(lambda x: str(x).replace('%', ''))
cd_df['Total Return'] = pd.to_numeric(cd_df['Total Return'])/100

start_date = hyg_df.index[0]
end_date = hyg_df.index[-1]

# creating a new daily date range to combine the direct lending and high yield bond performance
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# creating new dataframe with common index to compare hyg vs. direct lending
hyg_cd = pd.DataFrame({'hyg': hyg_df['total return'],
                       'cd': cd_df['Total Return']},
                      index=date_range)

# drops rows where both hyg and cd are nan, if one of the columns has a value it does not drop
hyg_cd.dropna(how='all', inplace=True)

# fill all nan values with zeros
hyg_cd.fillna('0', inplace=True)

# converting the values from strings to numeric
for col in hyg_cd.columns:
    hyg_cd[col] = pd.to_numeric(hyg_cd[col])

# creating performance values based on initial investment value
hyg_perf = ((hyg_cd['hyg'] + 1).cumprod() * 10000)
cd_perf = ((hyg_cd['cd'] + 1).cumprod() * 10000)

if __name__ == '__main__':

    # creating the figure
    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(nrows=10, ncols=4)

    # creating the performance subplot
    ax1 = fig.add_subplot(gs[0:6, :])
    ax1.set_title('Performance of $10,000 Investment')
    ax1.plot(cd_perf, label='private credit', color='r')
    ax1.plot(hyg_perf, label='high yield bonds')
    ax1.legend()

    # Setting the y ticks to be properly formatted 10000 becomes $10,000
    formatter = ticker.StrMethodFormatter('${x:,.0f}')
    ax1.yaxis.set_major_formatter(formatter)

    # creating the drawdown subplot
    ax2 = fig.add_subplot(gs[7:, :])
    ax2.set_title('Drawdowns')
    ax2.set_xlabel('Date')

    # high yield bond drawdowns
    ax2.plot((hyg_perf / hyg_perf.cummax()) - 1)

    # private credit drawdowns
    ax2.plot((cd_perf / cd_perf.cummax()) - 1, color='r')

    # changing the yaxis of drawdowns subplot to percentages
    pct_formatter = ticker.PercentFormatter(1, decimals=0)
    ax2.yaxis.set_major_formatter(pct_formatter)

    # plotting chart
    plt.show()

    print(hyg_cd['hyg'].std() * sqrt(252))

    print(hyg_perf.pct_change().std() * sqrt(252))

    fig.savefig('pc_first_chart.png')



