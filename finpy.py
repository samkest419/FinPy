# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 16:41:11 2018

@author: Richard Hardis
"""

from alpha_vantage.timeseries import TimeSeries


class fin_data:               #Class name fin_data
    
    print('New Fin. Data Object Created\n')
    
    def pull_data(self,ticker,pullType,interval='0',key='1RJDU8R6RESLVE09'):
        ts = TimeSeries(key=key, output_format='pandas')
        
        if pullType == 'intraday':
            data1, meta_data1 = ts.get_intraday(symbol=ticker,interval=interval,outputsize='full')
            print('Pulled intraday with interval = ' + interval + '\n')
        elif pullType == 'daily':
            data1, meta_data1 = ts.get_daily_adjusted(symbol=ticker,outputsize='full')
            print('Pulled daily\n')
        elif pullType == 'weekly':
            data1, meta_data1 = ts.get_weekly_adjusted(symbol=ticker,outputsize='full')
            print('Pulled weekly\n')
        elif pullType == 'monthly':
            data1, meta_data1 = ts.get_monthly_adjusted(symbol=ticker,outputsize='full')
            print('Pulled monthly\n')
        else:
            print('Please enter a valid pull type')
            
        data1.columns = ['Open','High','Low','Close','Volume']
        print('Data collected in dataframe data1\n')
        return data1
        
    def save_data(self,df,directory,ticker):
        df.to_csv(directory+ticker+'.csv')
        print('CSV File Saved!\n')
        
        
class plotter:
    
    print('New Plotter Object Created')
    
    def plotMACD(self,df):
        print('Nothing here yet!')
    