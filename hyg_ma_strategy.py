from loading_data import tbill_df, hyg_df
from hyg_cd_fifth_chart import spread_ma_strategy
import pandas as pd

import matplotlib.pyplot as plt

tbill_df['nav % change'] = tbill_df['NAV per Share'].pct_change()
tbill_df['income % gain'] = tbill_df['Ex-Dividends'] / tbill_df['NAV per Share']
tbill_df['total return'] = tbill_df['nav % change'] + tbill_df['income % gain']


spread_ma_strategy['tbill'] = tbill_df['total return']

three_months = 63

try:
    spread_ma_strategy.drop(['hy spread', 'rolling spread', 'strategy'], axis=1, inplace=True)
except KeyError:
    pass

hyg_perf = ((spread_ma_strategy['hyg'] + 1).cumprod() * 1)
tbill_perf = ((spread_ma_strategy['tbill'] + 1).cumprod() * 1)

three_m_df = spread_ma_strategy.copy()

three_m_df['rolling hyg perf'] = hyg_perf.pct_change(three_months)
three_m_df['rolling tbill perf'] = tbill_perf.pct_change(three_months)

# three_m_df['rolling hyg perf'].plot()
# three_m_df['rolling tbill perf'].plot()
# plt.show()

three_m_df = three_m_df[three_months:]

three_m_df['3 month momentum strategy'] = None

for i in range(len(three_m_df)):

    if three_m_df['rolling hyg perf'].iloc[i] > three_m_df['rolling tbill perf'].iloc[i]:

            three_m_df['3 month momentum strategy'].iloc[i] = three_m_df['cd'].iloc[i]

    else:

        three_m_df['3 month momentum strategy'].iloc[i] = (three_m_df['cd'].iloc[i] + three_m_df['hyg'].iloc[i]) / 2

strat_perf = ((three_m_df['3 month momentum strategy'] + 1).cumprod() * 10000)
hyg_perf = ((three_m_df['hyg'] + 1).cumprod() * 10000)
cd_perf = ((three_m_df['cd'] + 1).cumprod() * 10000)

if __name__ =='__main__':
    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(nrows=10, ncols=4)

    # creating the performance subplot
    ax1 = fig.add_subplot(gs[0:6, :])
    ax1.plot(strat_perf)
    ax1.plot(hyg_perf)
    ax1.plot(cd_perf)

    # creating the subplot showing t bill relative to hyg 3 month perf
    ax2 = fig.add_subplot(gs[7:, :])
    ax2.plot(three_m_df['rolling tbill perf'])
    ax2.plot(three_m_df['rolling hyg perf'])



    plt.show()

