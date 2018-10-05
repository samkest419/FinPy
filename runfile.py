# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
import time

from finpy import *
from strategies import macdStrat, chaikinMFStrat

ticker = 'SPY'
period = 'daily'
interval = '1min'


spy = pull_data(ticker,period,interval)                                      #Pull data

save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')  #Save the data to csv format

#candlePlot(spy,period)    #Plot the candleplot

spy_macd = create_macd(spy,3,6,2)
#plotMACD(spy_macd,period)

#plotVertical(spy_macd,period)

stratout = macdStrat(spy_macd.iloc[:,:],period,interval)

#emailSignal('richardphardis@gmail.com',stratout)

buys = stratout[stratout['macd_trade']=='Buy']

is_new(stratout)

chaikin = chaikinMFStrat(spy_macd,period,interval,window=20)