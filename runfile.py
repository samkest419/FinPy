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
from strategies import *
from optimizations import *
#from Backtest import applyStrat
ticker = 'SPY'
period = 'daily'
interval = '60min'


#spy = pull_data(ticker,period,interval)                                      #Pull data
#base_span = 26
#leading_b_span = 52
#conversion_span = 9
#ichi = ichimoku(spy, conversion_span, base_span, leading_b_span)
#ichimoku_plot(ichi.Close, ichi.Conversion_Line, ichi.Base_Line, ichi.Leading_A, ichi.Leading_B, ichi.Lagging, conversion_span, base_span, leading_b_span)

initial = [-10,10]
bounds = [(-10,10), (-10,10)]
PSO(func1, initial, bounds, num_particles = 15, maxiter = 300)
#spy.drop(['DT','TimeDelta'],inplace=True,axis = 1)
#spy.to_csv('C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\'+ 'M1_SPY' + '.csv',index=False)
#save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\',
#          'M1_SPY')  #Save the data to csv format

#candlePlot(spy,period)    #Plot the candleplot

#spy_macd362 = create_macd(spy,3,6,2)
##plotMACD(spy_macd362,period)
#spy_macd5153 = create_macd(spy,5,15,3)
##plotMACD(spy_macd5153,period)
#spy_macd8217 = create_macd(spy,8,21,7)
##rdf, figure = plotMACD(spy_macd8217.iloc[-60:,:],period)
#
##plotVertical(spy_macd,period)
#
#stratout362 = macdStrat(spy_macd362,period,interval,-.5)
#stratout5153 = macdStrat(spy_macd5153,period,interval,-.5)
#stratout8217 = macdStrat(spy_macd8217,period,interval,-.5)
#
##emailSignal('richardphardis@gmail.com',stratout)
#
##buys = stratout[stratout['macd_trade']=='Buy']
#
##is_new(stratout)
##condition = oversold30min(stratout362,stratout5153,stratout8217)
#cmfFast = create_cmf(spy,8)
#cmfSlow = create_cmf(spy,21)
#cmfMACD = create_cmfmacd(cmfFast,cmfSlow,7)
##plotCMFMACD(cmfMACD,period)
##plotCMFMACD(cmf362,period)
##plotCMFMACD(cmf5153,period)
##plotCMFMACD(cmf8217,period)
#
#x = np.arange(0,len(cmfMACD.index))
#y1 = cmfMACD['Close']
#y2 = cmfMACD['CMF MACD']
#y3 = cmfMACD['CMF Signal']
#
##plotMultiY(x,y1,y2) #Only accepts three arguments right now
#btest = backTest30Min(spy, period, interval, -.5, 10)
#ops_only = btest[btest['trade_signal'] != 'Hold']
#
#macdHistogram(spy_macd362)