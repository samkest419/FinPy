# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 10:07:14 2018

@author: Richard Hardis
"""

import pandas as pd
from finpy import *
import time

ticker = 'SPY'
periods = ['monthly','weekly','daily','intraday','intraday','intraday','intraday','intraday']
intervals = ['month','week','day','60min','30min','15min','5min','1min']
filenames = ['monthly_SPY','weekly_SPY','daily_SPY','M60_SPY','M30_SPY','M15_SPY','M5_SPY','M1_SPY']

path = 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy'

def old_method():
    for period, interval, filename  in zip(periods, intervals, filenames):
        print('{} {} {}\n\n\n'.format(period, interval, filename))
        try:
            #Collect the latest data
            df = pull_data(ticker,period,interval)
            df.to_csv(path+'\\'+filename+'_new.csv')
            new_df = pd.read_csv(path+'\\'+filename+'_new.csv')
            
            #Open the old dataset
            file_path = path + '\\' + filename + '.csv'
            old_df = pd.read_csv(file_path)
            #old_df.to_csv(path + '\\' + filename + '_Old.csv')
            
            #Merge the two datasets
            df_merged = new_df.merge(old_df,how = 'outer')
            #df_merged.set_index('DT', inplace=True,drop=False)
                    
            #Save the combined dataset
            df_merged.to_csv(file_path)
            
            #Print when finished
            print('saved {}.\n'.format(file_path))
        except:
            print('Unable to Load Data for {}, {}, {}.\n'.format(period,interval,filename))
        time.sleep(10)
        
def new_method():
    #Pull the new data
    
    
    #Load the old data
    
    
    #
    


    