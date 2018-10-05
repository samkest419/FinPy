# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 08:19:39 2018

@author: Richard Hardis
"""

import time
from finpy import *
from strategies import *

ticker = 'SPY'
period = 'intraday'
interval = '30min'
t_wait = 60 #interval in seconds

span1 = 3
span2 = 6
span3 = 2
span4 = 5
span5 = 15
span6 = 3

while True:
    spy = pull_data(ticker,period,interval) 
    spy_macd362 = create_macd(spy.iloc[-10:,:],span1,span2,span3)
    stratout362 = macdStrat(spy_macd362,period,interval,-.5)
    spy_macd5153 = create_macd(spy.iloc[-10:,:],span4,span5,span6)
    stratout5153 = macdStrat(spy_macd5153,period,interval,-.5)
    signal = oversold30min(stratout362,stratout5153)
    if ((signal == 'Buy') or (signal == 'Hold')):
        emailSignal(['richardphardis@gmail.com','samkest419@gmail.com'],stratout362)
    time.sleep(t_wait)
    
    
#['richardphardis@gmail.com','samkest419@gmail.com']