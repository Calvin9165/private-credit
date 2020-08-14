from hyg_cd_first_chart import hyg_cd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

hyg_cd['50/50 strategy'] = (hyg_cd['hyg'] + hyg_cd['cd']) / 2

hyg_perf = ((hyg_cd['hyg'] + 1).cumprod() * 10000)
cd_perf = ((hyg_cd['cd'] + 1).cumprod() * 10000)
half_half = ((hyg_cd['50/50 strategy'] + 1).cumprod() * 10000)


if __name__ == '__main__':

    fig = plt.figure(figsize=(7, 7))
    gs = fig.add_gridspec(nrows=10, ncols=4)

    # plotting the investment value of the three portfolios
    ax1 = fig.add_subplot(gs[0:6, :])
    ax1.set_title('Performance of $10,000 Investment')
    ax1.plot(hyg_perf, color='lightgrey')
    ax1.plot(cd_perf, color='lightgrey')
    ax1.plot(half_half, color='red', label='50/50 Portfolio')
    formatter = ticker.StrMethodFormatter('${x:,.0f}')
    ax1.yaxis.set_major_formatter(formatter)
    ax1.legend()

    # plotting the drawdowns for all the portfolios
    ax2 = fig.add_subplot(gs[7:, :])
    ax2.set_title('Drawdowns')
    ax2.set_xlabel('Date')
    ax2.plot((hyg_perf / hyg_perf.cummax()) - 1, color='lightgrey')
    ax2.plot((cd_perf / cd_perf.cummax()) - 1, color='lightgrey')
    ax2.plot((half_half / half_half.cummax()) - 1, color='red')

    pct_formatter = ticker.PercentFormatter(1, decimals=0)
    ax2.yaxis.set_major_formatter(pct_formatter)

    plt.show()

    fig.savefig('pc_third_chart.png')
