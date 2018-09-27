# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:40:01 2018

@author: Richard Hardis
"""
import pandas as pd
import numpy as np


#Strategy 1: Pure MACD - no Chaikin MF
def macdStrat(df,period,interval):
    #Returns by, sell, or hold signal.  Only the most basic form here --> crossing from negative to positive or positive to negative
    df = df.copy(deep=True)
    crossover_current = df.iloc[-1,-1]
    crossover_previous = df.iloc[-2,-1]
    macd_status = df.iloc[-10:,-3]
    
    df['PrevCross'] = df.iloc[:,-1].shift(1)
    df.iloc[0,-1] = 0
    df['Buy'] = np.where((df.iloc[:,-2]>0) & (df.iloc[:,-1]<0),'Buy','')
    df['Sell'] = np.where((df.iloc[:,-3]<0) & (df.iloc[:,-2]>0),'Sell','')
    df['Trade'] = df['Buy'] + df['Sell']
    df = df.drop(['Buy','Sell'],axis=1)
    
    #Add in logic for hysterisis and scale factors for the crossovers.
    
    return df