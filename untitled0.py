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

span1 = 5
span2 = 25
span3 = 3

while True:
    spy = pull_data(ticker,period,interval) 
    spy_macd = create_macd(spy,span1,span2,span3)
    stratout = macdStrat(spy_macd,period,interval)
    emailSignal('richardphardis@gmail.com',stratout)
    time.sleep(t_wait)