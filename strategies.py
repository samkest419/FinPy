# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:40:01 2018

@author: Richard Hardis
"""
#import pandas as pd
import numpy as np
import pandas as pd
from scipy import fftpack
import matplotlib.pyplot as plt


#Strategy 1: Pure MACD - no Chaikin MF
def macdStrat(df,period,interval,low_bound):
    #Returns by, sell, or hold signal.  Only the most basic form here --> crossing from negative to positive or positive to negative
    df = df.copy(deep=True)
    
    df['buy2'] = 0
    for i in np.arange(len(df.iloc[:,-1])-9):
        df.iloc[i+9,-1] = np.min(df['macd'][i:(i+9)])
        #print(np.min(df['stock_fast_ema'][i:(i+10)]))
    
    df['prevCross'] = df['crossover'].shift(1)
    df.iloc[0,-1] = 0
    
    df['prevMACD'] = df['macd'].shift(1)
    df.iloc[0,-1] = 0
    
    df['buy'] = np.where((df['crossover']>0) & (df['prevCross']<0) & (df['buy2']<low_bound),'Buy','')
    #df['Sell'] = np.where((df['crossover']<0) & (df['PrevCross']>0),'Sell','')
    df['sell'] = np.where((df['macd']>0) & (df['prevMACD']<0),'Sell','')
    df['hold'] = np.where((df['buy'] == '') & (df['sell'] == ''),'Hold','')
    df['macd_trade'] = df['buy'] + df['sell'] + df['hold']
    df = df.drop(['buy','sell','hold'],axis=1)

    return df

def oversold30min(df362,df5153,df8217):
    df362 = df362.copy(deep=True)
    df5153 = df5153.copy(deep=True)
    df8217 = df8217.copy(deep=True)
    
    #Hold the last non-hold signal over the past ten periods
    list362 = list(df362.iloc[-10:,-1])
    subsetBuyHold = [signal for signal in list362 if signal != 'Hold']
    if (len(subsetBuyHold) > 0):
        result362 = subsetBuyHold[-1]
    else:
        result362 = 'Hold'
        
    result5153 = df5153.iloc[-1,-1]
    
    #if True:
    result8217 = df8217.iloc[-1,1]
    
    if (((result362 == 'Buy') and (result5153 == 'Buy')) and not (result8217 == 'Sell')):
        result = 'Buy'
    elif (((result362 != 'Buy') and (result5153 != 'Buy')) and (result8217 == 'Sell')):
        result = 'Sell'
    else:
        result = 'Hold'
    
    return(result)

def rollingLastSignal(list_in):
    subsetBuyHold = [signal for signal in list_in if signal != 'Hold']
    if (len(subsetBuyHold) > 0):
        result = subsetBuyHold[-1]
    else:
        result = 'Hold'
    return result

def backTest30Min(base_df, period, interval, low_bound,window362):
    #example: output_df = backTest30Min(spy,'intraday','30min',-0.5,10)
    df362 = macdStrat(create_macd(base_df,3,6,2),period,interval, low_bound)
    df5153 = macdStrat(create_macd(base_df,5,15,3),period,interval, low_bound)
    df8217 = macdStrat(create_macd(base_df,8,21,7),period,interval, low_bound)
    
    #combine into one big dataframe
    combinedDf = base_df
    combinedDf['signals_1'] = df362['macd_trade']   #iloc -5
    combinedDf['signals_2'] = df5153['macd_trade']  #iloc -4
    combinedDf['signals_3'] = df8217['macd_trade']  #iloc -3
    combinedDf = combinedDf.reset_index(drop=True)
    
    indices362 = np.arange(window362-1,len(combinedDf))
    combinedDf['signals_1_window'] = 0              #iloc -2
    combinedDf['trade_signal'] = 'Hold'             #iloc -1
    
    for i in indices362:
        windowList = combinedDf.iloc[(i-9):(i+1),-5]    #Must be selecting the signals_1 column
        combinedDf.iloc[i,-2] = rollingLastSignal(windowList)
        
        if ((combinedDf.iloc[i,-2] == 'Buy') and (combinedDf.iloc[i,-4] == 'Buy') and not (combinedDf.iloc[i,-3] == 'Sell')):
            combinedDf.iloc[i,-1] = 'Buy'
        elif ((combinedDf.iloc[i,-2] != 'Buy') and (combinedDf.iloc[i,-4] != 'Buy') and (combinedDf.iloc[i,-3] == 'Sell')):
            combinedDf.iloc[i,-1] = 'Sell'  
    
    return(combinedDf)
    
def create_macd(df,span1,span2,span3):
    df = df.copy(deep=True)
    df['stock_fast_ema'] = pd.ewma(df['Close'], span=span1)
    df['stock_slow_ema'] = pd.ewma(df['Close'], span=span2)
    df['macd'] = df['stock_fast_ema'] - df['stock_slow_ema']
    df['signal'] = pd.ewma(df['macd'], span=span3)
    df['crossover'] = df['macd'] - df['signal'] # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal                                                                     # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal
    return df

def create_cmf(df,window):
    df = df.copy(deep=True)
    df['mf_multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['mf_volume'] = df['mf_multiplier'] * df['Volume']
    
    df['Period CMF'] = df['mf_volume'].rolling(min_periods=1, window=window).sum() / df['Volume'].rolling(min_periods=1, window=window).sum()
    return df

def create_cmfmacd(df_fast,df_slow,span3):
    df_fast = df_fast.copy(deep=True)    
    df_slow = df_slow.copy(deep=True)  

    df_cmf = df_fast.copy(deep=True)
    df_cmf = df_cmf[['Close','Volume','Period CMF']]
    df_cmf.rename(columns={'Period CMF': 'Fast MF'}, inplace=True)
    df_cmf['Slow MF'] = df_slow['Period CMF']
    df_cmf['CMF MACD'] = df_cmf['Fast MF'] - df_cmf['Slow MF']
    df_cmf['CMF Signal'] = pd.ewma(df_cmf['CMF MACD'], span = span3)
    df_cmf['CMF Crossover'] = df_cmf['CMF MACD'] - df_cmf['CMF Signal']
    
    #df_cmf['mf_fast'] = df_fast['Period CMF']
    #df['mf_slow_ema'] = pd.ewma(df['Period CMF'], span=span2)
    #df['cmf_macd'] = df['mf_fast_ema'] - df['mf_slow_ema']
    #df['cmf_signal'] = pd.ewma(df['cmf_macd'], span=span3)
    #df['cmf_crossover'] = df['cmf_macd'] - df['cmf_signal'] # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal                                                                     # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal
    return df_cmf
    

def chaikinMFStrat(df,period,interval,window):
    df = df.copy(deep=True)
    # Chaikin Money Flow Indicator (CMF)  
    
    df['Buy 1'] = df['macd'][-10:] < -0.5 # fast line was less than -0.5 in the last 10 period. THis used to be 3-6
    df['Buy 2'] = df['crossover'] > 0 # fast line crossed above slow line
    df['Buy 3'] = df['Period CMF'] <  -0.5
    df['BUY'] = df['Buy 1'] + df['Buy 2']
    
    
    
    
    df['Sell 1'] = df['macd'] > 0 #  MACD oscillator crosses above 0.  This used to be 5-15
    
    df['Sell 2'] = df['Period CMF'] >  0.5
    
    df['SELL'] = df['Sell 1'] + df['Sell 2']
    
    return df

def ichimoku(df, conversion_span, base_span, leading_b_span):
    #input a dataframe with price data
    df = df.copy(deep=True)
    
    #Calculate tenkan-sen 
    df['Conversion_Line'] = (df.High.rolling(min_periods=1, window=conversion_span).max() + df.Low.rolling(min_periods=1, window=conversion_span).min())/2
    df['Base_Line'] = (df.High.rolling(min_periods=1, window=base_span).max() + df.Low.rolling(min_periods=1, window=base_span).min())/2
    df['Leading_A'] = (df.Conversion_Line + df.Base_Line)/2
    df['Leading_B'] = (df.High.rolling(min_periods=1, window=leading_b_span).max() + df.Low.rolling(min_periods=1, window=leading_b_span).min())/2
    df['Lagging'] = df.Close
    df['Leading_Diff'] = df.Leading_A - df.Leading_B
    df['Leading_Diff_Shifted'] = df.Leading_Diff.shift(-1)
    df['crossover'] = list(map(crossover_val, df.Leading_Diff, df.Leading_Diff_Shifted))
    
    return df

def crossover_val(var1, var2):
    if var1 > 0 and var2 < 0:
        value = 1
    elif var1 < 0  and var2 > 0:
        value = -1
    else:
        value = 0
    
    return value

def freq_analysis(df, rate, window_min, window_max):
    signal = df.Close
    transformed_signal = fftpack.fft(signal)
    freqs = fftpack.fftfreq(len(signal)) * rate
    
    plt.plot(freqs, np.log10((transformed_signal)))
    plt.xlim(window_min, window_max)
    
    return frequency, amplitude

