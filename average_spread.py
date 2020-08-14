from one_year_hy_spread import spread_ma_strategy
import matplotlib.pyplot as plt

# see the reasoning behind this in the percentile spread module
try:
    spread_ma_strategy.drop(['rolling spread', 'strategy'], axis=1, inplace=True)
except KeyError:
    pass


average_spread = spread_ma_strategy

average_spread['average spread strategy'] = None


for i in range(len(average_spread)):

    if average_spread['hy spread'].iloc[i] > average_spread['hy spread'].mean():

        average_spread['average spread strategy'].iloc[i] = average_spread['hyg'].iloc[i] * 0.5 + \
                                                           average_spread['cd'].iloc[i] * 0.5

    else:

        average_spread['average spread strategy'].iloc[i] = average_spread['cd'].iloc[i]


if __name__ == '__main__':

    strat_perf = ((average_spread['average spread strategy'] + 1).cumprod() * 10000)
    hyg_perf = ((average_spread['hyg'] + 1).cumprod() * 10000)
    cd_perf = ((average_spread['cd'] + 1).cumprod() * 10000)

    fig = plt.figure()
    gs = fig.add_gridspec(nrows=10, ncols=4)


    ax1 = fig.add_subplot(gs[:7, :])
    ax1.plot(strat_perf, label='strategy')
    ax1.plot(hyg_perf, label='high yield')
    ax1.plot(cd_perf, label='private credit')
    ax1.legend()

    ax2 = fig.add_subplot(gs[7:, :])
    ax2.plot(average_spread['hy spread'])

    # avg_spread = spread_ma_strategy

    ax2.axhline(average_spread['hy spread'].mean(), color='red', ls='--', lw=0.5)

    # ax2.plot(spread_ma_strategy['hy spread'].mean(), ls='--', color='red')
    # ax2.plot(spread_ma_strategy['rolling spread'])

    plt.tight_layout()
    plt.show()
