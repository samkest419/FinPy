# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""

from finpy import *
from strategies import macdStrat

ticker = 'SPY'
period = 'monthly'
interval = '60min'


spy = pull_data(ticker,period,interval)                                      #Pull data

save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')  #Save the data to csv format

candlePlot(spy,period)    #Plot the candleplot

spy_macd = create_macd(spy,5,25,3)
plotMACD(spy_macd,period)

a = plotVertical(spy_macd,period)

stratout = macdStrat(spy_macd,period,interval)

signal = True

if signal == 'buy':
    print('Buy SPY now!')
elif signal == 'sell':
    print('Sell SPY now!')
else:
    print('Hold SPY')