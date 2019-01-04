# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 06:43:01 2018

@author: Richard Hardis
"""

import pandas as pd
from finpy import *
import time

ticker = 'SPY'
period = 'monthly'
interval = '60min'
filename = 'monthly_SPY'

df = pull_data(ticker,period,interval)

#Open the old dataset
file_path = path + '\\' + filename + '.csv'
old_df = pd.read_csv(file_path)

