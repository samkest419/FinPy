# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 08:19:39 2018

@author: Richard Hardis
"""

import time
from finpy import *

ticker = 'SPY'
period = 'intraday'
interval = '1min'
t_wait = 60 #interval in seconds

span1 = 3
span2 = 6
span3 = 2

while True:
    spy = pull_data(ticker,period,interval) 
    spy_macd = create_macd(spy.iloc[-10:,:],span1,span2,span3)
    stratout = macdStrat(spy_macd,period,interval)
    signal = stratout.iloc[-1,-1]
    if ((signal == 'Buy') or (signal == 'Sell')):
        emailSignal(['richardphardis@gmail.com','samkest419@gmail.com'],stratout)
    time.sleep(t_wait)
    
    
#['richardphardis@gmail.com','samkest419@gmail.com']