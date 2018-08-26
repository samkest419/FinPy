# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
from finpy import *

data = fin_data()       #Create a new data object that we will use to pull the data

spy = data.pull_data('SPY','intraday','30min')
data.save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')