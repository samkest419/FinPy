# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:40:01 2018

@author: Richard Hardis
"""
import pandas as pd


#Strategy 1: Pure MACD - no Chaikin MF
def macdStrat(df,period,interval):
    #Returns by, sell, or hold signal
    df = df.copy(deep=True)
    crossover_current = df.iloc[-1,-1]
    crossover_previous = df.iloc[-2,-1]
    macd_status = df.iloc[-10:,-3]

    df['Buy1'] = df.iloc[-10:,-3] < -.5
    df['Buy2'] = df.iloc[:,-1]
    df['BUY'] = df.iloc[:,-3] + df.iloc[:,-1]     
    
    return df