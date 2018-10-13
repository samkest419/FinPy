# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
import time
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from finpy import *
from strategies import macdStrat, chaikinMFStrat, oversold30min

ticker = 'SPY'
period = 'intraday'
interval = '1min'


spy = pull_data(ticker,period,interval)                                      #Pull data

save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\',
          'M1_SPY')  #Save the data to csv format

#candlePlot(spy,period)    #Plot the candleplot

spy_macd362 = create_macd(spy,3,6,2)
#plotMACD(spy_macd362,period)
spy_macd5153 = create_macd(spy,5,15,3)
#plotMACD(spy_macd5153,period)
spy_macd8217 = create_macd(spy,8,21,7)
#rdf = plotMACD(spy_macd8217.iloc[-60:,:],period)

#plotVertical(spy_macd,period)

stratout362 = macdStrat(spy_macd362,period,interval,-.5)
stratout5153 = macdStrat(spy_macd5153,period,interval,-.5)
stratout8217 = macdStrat(spy_macd8217,period,interval,-.5)

#emailSignal('richardphardis@gmail.com',stratout)

#buys = stratout[stratout['macd_trade']=='Buy']

#is_new(stratout)
#condition = oversold30min(stratout362,stratout5153,stratout8217)
cmfFast = create_cmf(spy,8)
cmfSlow = create_cmf(spy,21)
cmfMACD = create_cmfmacd(cmfFast,cmfSlow,7)
#plotCMFMACD(cmfMACD,period)
#plotCMFMACD(cmf362,period)
#plotCMFMACD(cmf5153,period)
#plotCMFMACD(cmf8217,period)

x = np.arange(0,len(cmfMACD.index))
y1 = cmfMACD['Close']
y2 = cmfMACD['CMF MACD']
y3 = cmfMACD['CMF Signal']

#plotMultiY(x,y1,y2) #Only accepts three arguments right now