# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
from finpy import *

ticker = 'SPY'
period = 'intraday'
interval = '60min'

spy = pull_data(ticker,period,interval)                                      #Pull data
save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')  #Save the data to csv format

candlePlot(spy,period)    #Plot the candleplot

spy_macd = create_macd(spy,5,15,3)
plotMACD(spy,period)
plotVertical(spy)

