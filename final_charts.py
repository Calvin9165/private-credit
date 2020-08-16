from composite_strategy import max_dd, cagr


import pandas as pd
import matplotlib.pyplot as plt

# print(max_dd)
# print(cagr)

# # converting the drawdown dictionary in pandas DataFrame
dd_df = pd.DataFrame.from_dict(max_dd, orient='index', columns=['Max Drawdown'])
#
# # converting the cagr dictionary in pandas DataFrame
cagr_df = pd.DataFrame.from_dict(cagr, orient='index', columns=['CAGR'])
#
# fig = plt.figure()
#
#
# # ax1 = fig.add_subplot(121)
# cagr_df.plot.bar()
# dd_df.plot.bar()
#
#
# plt.show()

print(dd_df)
print(cagr_df)