from hyg_cd_first_chart import hyg_df, cd_df
import pandas as pd
import matplotlib.pyplot as plt


format_col = ['Income Return', 'Realized Gain/Loss', 'Unrealized Gain/Loss']

# converting the strings with % back to floats so that we can perform operations on them
for col in format_col:
    cd_df[col] = cd_df[col].apply(lambda x: str(x).replace('%', ''))
    cd_df[col] = pd.to_numeric(cd_df[col]) / 100

# adjust starting date so that it lines up with the starting date of HYG inception
cd_df = cd_df['2006-12-31':]



# Breaking down the performance of CLDI

# performance of the income generated from loans
cd_income_perf = (cd_df['Income Return'] + 1).cumprod()

# principal recovery on loans
cd_principal_perf = (cd_df['Realized Gain/Loss'] + 1) * (cd_df['Unrealized Gain/Loss'] + 1).cumprod()

# total return of loans. income + principal recovery
cd_total_return = ((cd_df['Income Return'] + cd_df['Realized Gain/Loss'] + cd_df['Unrealized Gain/Loss']
                 + 1).cumprod())



# Breaking down performance of HYG

print(hyg_df.index[0])

hyg_income_perf = (hyg_df['income % gain'] + 1).cumprod()

hyg_principal_perf = (hyg_df['nav % change'] + 1).cumprod()

hyg_total_return = (hyg_df['total return'] + 1).cumprod()

fig = plt.figure(figsize=(9, 6))

ax1 = fig.add_subplot(1, 2, 1)
ax1.set_title('High Yield Return Breakdown')
ax1.plot(hyg_total_return, label='Total Return')
ax1.plot(hyg_principal_perf, label='NAV Growth')
ax1.plot(hyg_income_perf, label='Income')
ax1.legend()


ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title('Private Credit Return Breakdown')
ax2.plot(cd_total_return, label='Total Return')
ax2.plot(cd_principal_perf, label='NAV Growth')
ax2.plot(cd_income_perf, label='Income')
ax2.legend()

plt.show()

fig.savefig('pc_second_chart.png')

