from hyg_cd_first_chart import hyg_cd
from loading_data import spread_df
import matplotlib.pyplot as plt


spread_ma_strategy = hyg_cd.copy()

spread_ma_strategy['hy spread'] = spread_df['Spread']
spread_ma_strategy['rolling spread'] = spread_df['rolling spread']


spread_ma_strategy.fillna(method='ffill', inplace=True)
# spread_ma_strategy['rolling hy spread'] = spread_ma_strategy['hy spread'].rolling(252).mean()

# reason we divide by 63 is because 63 is a quarter in trading days (252/4)
# we need to convert to quarterly data so that when the strategy switches the return of the
# private credit fund is proportional to the amount of time the strategy has been invested
spread_ma_strategy['cd'] = spread_ma_strategy['cd'] / 63
spread_ma_strategy['cd'].replace(to_replace=0, method='bfill', inplace=True)

spread_ma_strategy['12 month rolling spread strategy'] = None

for i in range(len(spread_ma_strategy)):

    if spread_ma_strategy['hy spread'].iloc[i] > spread_ma_strategy['rolling spread'].iloc[i]:

        # if high yield spread is above MA then the strategy return equals 50% private credit
        # 50% high yield
        spread_ma_strategy['12 month rolling spread strategy'].iloc[i] = spread_ma_strategy['hyg'].iloc[i] * 0.5 + \
                                                                         spread_ma_strategy['cd'].iloc[i]*0.5

    else:

        # id the high yield spread is below MA then the strategy return equals 100% private credit
        spread_ma_strategy['12 month rolling spread strategy'].iloc[i] = spread_ma_strategy['cd'].iloc[i]


if __name__ == '__main__':

    strat_perf = ((spread_ma_strategy['12 month rolling spread strategy'] + 1).cumprod() * 10000)
    hyg_perf = ((spread_ma_strategy['hyg'] + 1).cumprod() * 10000)
    cd_perf = ((spread_ma_strategy['cd'] + 1).cumprod() * 10000)

    fig = plt.figure()
    gs = fig.add_gridspec(nrows=10, ncols=4)


    ax1 = fig.add_subplot(gs[:7, :])
    ax1.plot(strat_perf, label='strategy')
    ax1.plot(hyg_perf, label='high yield')
    ax1.plot(cd_perf, label='private credit')
    ax1.legend()

    ax2 = fig.add_subplot(gs[7:, :])
    ax2.plot(spread_ma_strategy['hy spread'])
    ax2.plot(spread_ma_strategy['rolling spread'])

    plt.tight_layout()
    plt.show()
