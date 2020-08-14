from hyg_ma_strategy import three_m_df
from hyg_cd_third_chart import hyg_cd
from hyg_cd_fifth_chart import spread_ma_strategy
from average_spread import average_spread
from percentile_spread import pctile_spread

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import timedelta
from math import sqrt

initial_investment = 10000

df_list = [hyg_cd, three_m_df, spread_ma_strategy, average_spread, pctile_spread]

start_date = df_list[0].index[0]

# find the most recent date from each dataframe
# this will then be used to have a start date that is equal for all strategies
for df in df_list[1:]:

    if df.index[0] > start_date:

        start_date = df.index[0]


# converting to a string so that we can slice the dataframes
start_date = start_date.strftime('%Y-%m-%d')


three_month_perf = ((three_m_df[start_date:]['3 month momentum strategy'] + 1).cumprod() *
                    initial_investment)

fifty_fifty_perf = ((hyg_cd[start_date:]['50/50 strategy'] + 1).cumprod() * initial_investment)

hy_spread_perf = ((spread_ma_strategy[start_date:]['12 month rolling spread strategy'] + 1).cumprod() * initial_investment)

average_spread_perf = ((average_spread[start_date:]['average spread strategy'] + 1).cumprod() *
                       initial_investment)

pctile_perf = ((pctile_spread[start_date:]['75 pctile strategy'] + 1).cumprod() * initial_investment)


all_strats = [three_month_perf, fifty_fifty_perf, hy_spread_perf, average_spread_perf, pctile_perf]

composite = sum(all_strats) / len(all_strats)


def cagr_calculator(strategy_series):

    start_val = strategy_series.iloc[0]
    end_val = strategy_series.iloc[-1]

    # period is equal to number of years the strategy has been invested for as a float
    period = (strategy_series.index[-1] - strategy_series.index[0]) / timedelta(days=365)

    return ((end_val / start_val) ** (1 / period)) - 1


# dictionary to hold drawdown values
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

if __name__ == '__main__':

    fig = plt.figure()
    gs = fig.add_gridspec(nrows=10, ncols=4)

    ax1 = fig.add_subplot(gs[:7, :])
    ax1.set_title('Performance of $10,000 Investment')

    ax1.plot(three_month_perf, label='3 month momentum strategy', alpha=0.25)
    ax1.plot(fifty_fifty_perf, label='50/50 strategy', alpha=0.25)
    ax1.plot(hy_spread_perf, label='12 month rolling spread strategy', alpha=0.25)
    ax1.plot(average_spread_perf, label='average spread strategy', alpha=0.25)
    ax1.plot(pctile_perf, label='75th pctile strategy', alpha=0.25)
    ax1.plot(composite, label='composite strategy', color='black')

    formatter = ticker.StrMethodFormatter('${x:,.0f}')
    ax1.yaxis.set_major_formatter(formatter)
    ax1.legend()

    ax2 = fig.add_subplot(gs[8:, :])
    ax2.set_title('Drawdowns')
    pct_formatter = ticker.PercentFormatter(1, decimals=0)
    ax2.yaxis.set_major_formatter(pct_formatter)

    # dictionary to hold drawdown values
    max_dd = {}
    cagr = {}

    for strat in all_strats:

        ax2.plot(strat / strat.cummax() - 1, alpha=0.25)

    ax2.plot(composite / composite.cummax() - 1, color='black', lw=0.5)


    plt.show()







