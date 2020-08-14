from one_year_hy_spread import spread_ma_strategy
import matplotlib.pyplot as plt

# we include this because on the final import we've imported the average spread module which also
# has the same code as below, meaning that if we import average spread first there won't be
# a "rolling spread" or "strategy" column and therefore we'll get a KeyError
try:
    spread_ma_strategy.drop(['rolling spread', 'strategy'], axis=1, inplace=True)

except KeyError:
    pass


pctile_spread = spread_ma_strategy

pctile_spread['75 pctile strategy'] = None



for i in range(len(pctile_spread)):

    if pctile_spread['hy spread'].iloc[i] > pctile_spread['hy spread'].quantile(.75):

        pctile_spread['75 pctile strategy'].iloc[i] = pctile_spread['hyg'].iloc[i] * 0.5 + \
                                                           pctile_spread['cd'].iloc[i] * 0.5

    else:

        pctile_spread['75 pctile strategy'].iloc[i] = pctile_spread['cd'].iloc[i]



if __name__ == '__main__':

    strat_perf = ((pctile_spread['75 pctile strategy'] + 1).cumprod() * 10000)
    hyg_perf = ((pctile_spread['hyg'] + 1).cumprod() * 10000)
    cd_perf = ((pctile_spread['cd'] + 1).cumprod() * 10000)

    fig = plt.figure()
    gs = fig.add_gridspec(nrows=10, ncols=4)


    ax1 = fig.add_subplot(gs[:7, :])
    ax1.plot(strat_perf, label='strategy')
    ax1.plot(hyg_perf, label='high yield')
    ax1.plot(cd_perf, label='private credit')
    ax1.legend()

    ax2 = fig.add_subplot(gs[7:, :])
    ax2.plot(pctile_spread['hy spread'])

    ax2.axhline(pctile_spread['hy spread'].quantile(.75), color='red', ls='--', lw=0.5)

    # plt.tight_layout()
    # plt.show()
