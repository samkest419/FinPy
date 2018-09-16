
import pandas as pd
#pd.core.common.is_list_like = pd.api.types.is_list_like
#import pandas_datareaders_unofficial
#from pandas_datareaders_unofficial import data as web
import matplotlib.pyplot as plt
#import datetime
import numpy as np
#from pandas_datareaders_unofficial import data as pdr
#import fix_yahoo_finance as yf
from math import sqrt
#yf.pdr_override()

def MACD(stock, start, end):
    df = pd.DataFrame(pdr.get_data_yahoo(stock, start=start, end=end)['Close'])
    df = df.reset_index()
    df['30 mavg'] = pd.rolling_mean(df['Close'], 30)
    df['26 ema'] = pd.ewma(df['Close'], span=26)
    df['12 ema'] = pd.ewma(df['Close'], span=12)
    df['MACD'] = (df['12 ema'] - df['26 ema'])
    df['Signal'] = pd.ewma(df['MACD'], span=9)
    df['Crossover'] = df['MACD'] - df['Signal']
    return stock, df['Date'][-1:].to_string(),df['Crossover'][-1:].mean()


directory = 'C:/Users/Richard Hardis/.spyder-py3/'
df = pd.read_csv(directory+'SPY.csv')


# MACD 3,6,2
df['stock_df_3_ema'] = pd.ewma(df['Close'], span=3)
df['stock_df_6_ema'] = pd.ewma(df['Close'], span=6)
df['stock_df_macd_3_6'] = df['stock_df_3_ema'] - df['stock_df_6_ema']
df['stock_df_signal_3_6'] = pd.ewma(df['stock_df_macd_3_6'], span=2)
df['stock_df_crossover_3_6'] = df['stock_df_macd_3_6'] - df['stock_df_signal_3_6'] # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal
                                                                               # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal

# MACD 5,15,3
df['stock_df_5_ema'] = pd.ewma(df['Close'], span=5)
df['stock_df_15_ema'] = pd.ewma(df['Close'], span=15)
df['stock_df_macd_5_15'] = df['stock_df_5_ema'] - df['stock_df_15_ema']
df['stock_df_signal_5_15'] = pd.ewma(df['stock_df_macd_5_15'], span=3)
df['stock_df_crossover_5_15'] = df['stock_df_macd_5_15'] - df['stock_df_signal_5_15']  # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal
                                                                                # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal



# MACD 8, 21, 7
df['stock_df_8_ema'] = pd.ewma(df['Close'], span=8)
df['stock_df_21_ema'] = pd.ewma(df['Close'], span=21)
df['stock_df_macd_8_21'] = df['stock_df_8_ema'] - df['stock_df_21_ema']
df['stock_df_signal_8_21'] = pd.ewma(df['stock_df_macd_8_21'], span=7)
df['stock_df_crossover_8_21'] = df['stock_df_macd_8_21'] - df['stock_df_signal_8_21']  # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal
                                                                                # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal



# Chaikin Money Flow Indicator (CMF)

df['mf_multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
df['mf_volume'] = df['mf_multiplier'] * df['Volume']

# calculate 20 period CMF for last 20 periods, using rolling.sum()
# 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume
df['20 Period CMF'] = df['mf_volume'].rolling(min_periods=1, window=20).sum() / df['Volume'].rolling(min_periods=1, window=20).sum()




# confirm data
print(df.head())

# last 10 periods: df['Close'][-10:]


df['Buy 1'] = df['stock_df_macd_3_6'][-10:] < -0.5 # fast line was less than -0.5 in the last 10 periods

df['Buy 2'] = df['stock_df_crossover_3_6'] > 0 # fast line crossed above slow line

df['Buy 3'] = df['20 Period CMF'] <  -0.5

df['BUY'] = df['Buy 1'] + df['Buy 2']




df['Sell 1'] = df['stock_df_macd_5_15'] > 0 #  MACD oscillator crosses above 0

df['Sell 2'] = df['20 Period CMF'] >  0.5

df['SELL'] = df['Sell 1'] + df['Sell 2']




# DERIVE STRATEGY RETURNS


# stock single day returns
df['stock returns'] = (df['Close'] / df['Close'].shift(1)) - 1
df['stock returns'].fillna(0)
df['stock returns 1'] = df['stock returns'].fillna(0)
df['stock returns 2'] = df['stock returns 1'].replace([np.inf, -np.inf], np.nan)
df['stock returns final'] = df['stock returns 2'].fillna(0)
print('******************************** Stock Total  Daily Returns **************************************************')
print(df['stock returns final'])



df['position'] = np.where(df['BUY'] ,1 ,0)  # implements trading rule in vectorized fashion to go long
df['position'] = np.where(df['SELL'], -1, df['position'])  # implements trading rule in vectorized fashion to sell


df['strategy'] = df['position'].shift(1) * df['stock returns final']


print("STRATEGY RETURNS")
print(df['strategy'])  # this is output of strategy returns




# Calculate annualized mean and standard deviation of returns for strategy

# annualized mean return
df[['strategy']].mean() * 252
print("Annualized Mean Return")
print(df[['strategy']].mean() * 252)


# annualized standard deviation
df[['strategy']].std() * 252 ** 0.5
print("Annualized Standard Deviation")
print(df[['strategy']].std() * 252 ** 0.5)


# sharpe ratio
sharpe = (df['strategy'].mean() * 252) / (df['strategy'].std() * (np.sqrt(252)))
print("Sharpe Ratio")
print(sharpe)





####################################### RESULTING RISK STATISTICS: MAX DRAWDOWN AND VAR ###########################################################################################

# starting capital of $5k

risk = pd.DataFrame(df['strategy'])  # creates a new DataFrame object for risk analysis
risk['equity'] = risk['strategy'].cumsum().apply \
    (np.exp) * 5000  # calculates the equity position values over time given the leverage ratio of 30 in this case
risk['cummax'] = risk['equity'].cummax()

# next we calculate maximum drawdown and longest drawdown period

risk['drawdown'] = risk['cummax'] - risk['equity']  # calculates absolute drawdown over time

print("Maximum Drawdown Value, Initial Capital of $5,000 USD")
print(risk['drawdown'].max())  # identifies maximum drawdown value



########### VALUE AT RISK ##################################################################################################################################

# code below calculates the VaR values in USD for the single day under consideration in our backtest- and for multiple confidence intervals
# for example, at a confidence interval of 99% the VaR is 153.70 USD. Meaning, there is a 1% chance that an equity position of 5,000 USD loses more than
# 153.70 USD during (here, "the") trading day

import scipy.stats as scs  # imports stats sub-package of scipy

percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]  # defines the relevant percentile values (i.e. 100% - confidence interval)

VaR = scs.scoreatpercentile(risk['equity'] - 5000
                            ,percs)  # does the sorting, ranking, and identifies the respective (loss) values; uses interpolation if necessary
VaR.round(2)  # prints the absolute (loss) values


def print_var():
    print('%16s %16s' % ('Confidence Level', 'Value-at-Risk'))
    print(33 * '-')
    for pair in zip(percs, VaR):
        print('%16.2f %16.3f' % (100 - pair[0], -pair
            [1]))  # prints the confidence intervals and the positive VaR values (according to convention)


print("************************VaR (Value at Risk) Analysis***********************************************")
print("Output of the Confidence Intervals and Positive VaR Values")
print(print_var())






print("CURRENT SIGNAL")
print(df['position'])
print ("********************** THE CURRENT POSITIONING, OR SIGNAL, FOR THIS STOCK BASED ON GIVEN PAREMETERS IS LAST SIGNAL ON POSITION FRAME: 1 FOR LONG, 0 FOR NEUTRAL, AND -1 FOR SELL SHOWN ABOVE ON LAST LINE")




# PLOT STRATEGY CHART VS STOCK ACTUAL RETURNS
# In order to gain better comprehensive picture of how strategy compares to stock's performance over time, use cumsum and np.exp
df[['stock returns final', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
plt.show()






# *****************************************************************************************************************************************************************************************************
# PLOT MACD CHARTS ************************************************************************************************************************************************************************************
# *****************************************************************************************************************************************************************************************************

# PLOT MACD 3, 6, 2
plt.plot(df['stock_df_macd_3_6'], label= 'MACD 3,6,2 Oscillator', ls='-')
plt.plot(df['stock_df_signal_3_6'], label='MACD 3,6,2 Signal Line',ls='-' )
plt.plot(df['stock_df_crossover_3_6'], label='MACD 3,6,2 Crossover',ls='--')
#plt.plot(df['Close'],  label='SPY Price',ls='-' )
plt.title("MACD 3,6,2")
plt.legend(loc = 'upper left')
plt.show()


#PLOT MACD 5, 15, 3
plt.plot(df['stock_df_macd_5_15'], label= 'MACD 5,15,3 Oscillator', ls='-')
plt.plot(df['stock_df_signal_5_15'], label='MACD 5,15,3 Signal Line',ls='-' )
plt.plot(df['stock_df_crossover_5_15'], label='MACD 5,15,3 Crossover',ls='--')
#plt.plot(df['Close'],  label='SPY Price',ls='-' )
plt.title("MACD 5,15,3")
plt.legend(loc = 'upper left')
plt.show()



#PLOT MACD 8,21,7
plt.plot(df['stock_df_macd_8_21'], label= 'MACD 8,21,7 Oscillator', ls='-')
plt.plot(df['stock_df_signal_8_21'], label='MACD 8,21,7 Signal Line',ls='-' )
plt.plot(df['stock_df_crossover_8_21'], label='MACD 8,21,7 Crossover',ls='--')
#plt.plot(df['Close'],  label='SPY Price',ls='-' )
plt.title("MACD 8,21,7")
plt.legend(loc = 'upper left')
plt.show()



# PLOT STOCK PRICE & 20 DAY SMA

df['SMA'] = df['Close'].rolling(20).mean()  # calculate n series SMA

plt.plot(df['Close'], label='SPY Price', ls='-')
plt.plot(df['SMA'], label='20 Period on 30 Min Candles SMA', ls='-', color='black')
plt.title("SPY Price with 20 Day SMA")
plt.legend(loc = 'upper left')
plt.show()

df.to_csv(directory+'MACD_output.csv')