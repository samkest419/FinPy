# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 06:43:01 2018

@author: Richard Hardis
"""

import pandas as pd
from finpy import *
import time

ticker = 'SPY'
period = 'intraday'
interval = '1min'
filename = 'M1_SPY'
path = 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy'

df = pull_data(ticker,period,interval)
df.to_csv(path+'\\'+filename+'_2.csv', index=False)
df2 = pd.read_csv(path+'\\'+filename+'_2.csv')
#df.to_csv('C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\'+ 'monthly_SPY_new' + '.csv')
#new_df = pd.read_csv('C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\'+ 'monthly_SPY_new' + '.csv')
#new_df = new_df.iloc[:10,:]
#df.drop(['DT','TimeDelta'],inplace=True,axis = 1)
#df = df.iloc[:-10,:]

#Open the old dataset
file_path = path + '\\' + filename + '.csv'
old_df = pd.read_csv(file_path)
#old_df = old_df.iloc[7:15,:]
#old_df= old_df.iloc[:,1:]

#print(new_df.equals(old_df))

combined = pd.concat([df,old_df], join='outer', ignore_index=True)
