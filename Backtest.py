# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 10:35:39 2018

@author: Richard Hardis
"""

import pandas as pd
import numpy as np

from strategies import *
from finpy import *


def applyStrat(df_in, strategy):
    """
    Arguments:
        df_in: dataframe of open, high, low, close, volume
        strategy: strategy object with info on how to apply the strategy to a single instance
        
    Outputs:
        df: dataframe with buy and sell signals 
    """
    
    df = df_in.copy(deep=True)
    return df

def try30Min(initial_investment):
    ticker = 'SPY'
    period = 'intraday'
    interval = '30min'

    spy = pull_data(ticker,period,interval) 
    btest = backTest30Min(spy, period, interval, -.5, 10)
    ops_only = btest[btest['trade_signal'] != 'Hold']
    ops_only = ops_only.reset_index(drop=True)
    
    checker = ops_only.copy(deep=True)
    checker['Value'] = 0
    
    current_value = initial_investment
    current_cash = initial_investment
    current_shares = 0
    
    for i in np.arange(0, len(ops_only)):
        print('Index {}'.format(i))
        if (ops_only.iloc[i,-1] == 'Buy'):
            print('Current Cash = {}.  Current Shares = {}'.format(current_cash,current_shares))
            close_price = ops_only.iloc[i,3]
            shares_bought = current_cash/close_price
            current_shares = current_shares + shares_bought #cash/current closing price
            current_cash = 0
            checker.iloc[i,-1] = current_cash + current_shares * ops_only.iloc[i,3]
            print('Bought {} shares at ${}/share.'.format(shares_bought,close_price))
            print('Current Cash = {}.  Current Shares = {}\n\n\n'.format(current_cash,current_shares))
            
        elif (ops_only.iloc[i,-1] == 'Sell'):
            print('Current Cash = {}.  Current Shares = {}'.format(current_cash,current_shares))
            close_price = ops_only.iloc[i,3]
            shares_sold = current_shares
            current_cash = current_cash + current_shares * close_price
            current_shares = 0
            checker.iloc[i,-1] = current_cash + current_shares * ops_only.iloc[i,3]
            print('Sold {} shares at ${}/share'.format(shares_sold,close_price))
            print('Current Cash = {}.  Current Shares = {}\n\n\n'.format(current_cash,current_shares))
        
            
    total_value = current_cash + current_shares * ops_only.iloc[-1,3]
    
    checker = checker.iloc[:,[3,-2,-1]]
    
    return total_value, checker

initial = 1000
tot_val, df = try30Min(initial)
perc_profit = ((tot_val - initial)/initial) * 100