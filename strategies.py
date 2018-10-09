# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:40:01 2018

@author: Richard Hardis
"""
#import pandas as pd
import numpy as np


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

def sell8217(df_in):
    df = df_in.copy(deep=True)
    
    df['prevMACD']
    
    return result

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