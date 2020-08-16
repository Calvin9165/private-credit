from composite_strategy import composite, initial_investment, cagr_calculator
from hyg_cd_first_chart import hyg_cd

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df_list = [hyg_cd, composite]

start_date = df_list[0].index[0]

# find the most recent date from each dataframe
# this will then be used to have a start date that is equal for all strategies
for df in df_list[1:]:

    if df.index[0] > start_date:

        start_date = df.index[0]


# converting to a string so that we can slice the dataframes
start_date = start_date.strftime('%Y-%m-%d')

hyg_perf = ((hyg_cd['hyg'][start_date:] + 1).cumprod() * initial_investment)
cd_perf = ((hyg_cd['cd'][start_date:] + 1).cumprod() * initial_investment)
composite = composite[start_date:]

all_strats = [hyg_perf, cd_perf, composite]

max_dd = {}
cagr = {}

for strat in all_strats:

    # updating the max_dd dictionary, key is the name of the strategy, value is the max drawdown
    max_dd.update({strat.name: min(strat / strat.cummax() - 1)})

    # updating the cagr dictionary which tells you the cagr for each strategy
    cagr.update({strat.name: cagr_calculator(strat)})

max_dd.update({'composite strategy': min(composite / composite.cummax() - 1)})

# updating the cagr dictionary which tells you the cagr for each strategy
cagr.update({'composite strategy': cagr_calculator(composite)})

# print(max_dd)
# print(cagr)


if __name__ == '__main__':


    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(nrows=10, ncols=4)

    # creating the performance subplot
    ax1 = fig.add_subplot(gs[0:6, :])
    ax1.set_title('Performance of $10,000 Investment')
    ax1.plot(cd_perf, label='private credit', color='r')
    ax1.plot(hyg_perf, label='high yield bonds')
    ax1.plot(composite, label='composite strategy', color='black')
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

    # composite strategy drawdowns
    ax2.plot((composite / composite.cummax()) - 1, color='black')

    # changing the yaxis of drawdowns subplot to percentages
    pct_formatter = ticker.PercentFormatter(1, decimals=0)
    ax2.yaxis.set_major_formatter(pct_formatter)

    # plotting chart
    plt.show()

    fig.savefig('composite-vs-base-chart')


