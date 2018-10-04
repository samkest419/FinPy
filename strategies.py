# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:40:01 2018

@author: Richard Hardis
"""
#import pandas as pd
import numpy as np


#Strategy 1: Pure MACD - no Chaikin MF
def macdStrat(df,period,interval):
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
    
    df['buy'] = np.where((df['crossover']>0) & (df['prevCross']<0) & (df['buy2']<-.5),'Buy','')
    #df['Sell'] = np.where((df['crossover']<0) & (df['PrevCross']>0),'Sell','')
    df['sell'] = np.where((df['macd']>0) & (df['prevMACD']<0),'Sell','')
    df['hold'] = np.where((df['buy'] == '') & (df['sell'] == ''),'Hold','')
    df['trade'] = df['buy'] + df['sell'] + df['hold']
    df = df.drop(['buy','sell','hold'],axis=1)
    
    
    #Add in logic for hysterisis and scale factors for the crossovers.
    
    return df