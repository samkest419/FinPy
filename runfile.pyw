# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
import time

from finpy import *
from strategies import macdStrat

ticker = 'SPY'
period = 'intraday'
interval = '1min'

while True:
    spy = pull_data(ticker,period,interval)                                      #Pull data
    
    save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')  #Save the data to csv format
    
    #candlePlot(spy,period)    #Plot the candleplot
    
    spy_macd = create_macd(spy,5,25,3)
    plotMACD(spy_macd,period)
    
    #plotVertical(spy_macd,period)
    
    stratout = macdStrat(spy_macd,period,interval)

    emailSignal('richardphardis@gmail.com',stratout)
    time.sleep(60)  #sleep for one minute