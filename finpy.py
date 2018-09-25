# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 16:41:11 2018

@author: Richard Hardis
"""

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
import pandas as pd
import numpy as np
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter
    
    #print('New Fin. Data Object Created\n')
    
def pull_data(ticker,pullType,interval='0',key='1RJDU8R6RESLVE09'):
    ts = TimeSeries(key=key, output_format='pandas')
    
    if pullType == 'intraday':
        data1, meta_data1 = ts.get_intraday(symbol=ticker,interval=interval,outputsize='full')
        data1.columns = ['Open','High','Low','Close','Volume']
        
        if interval == '1min':
            td = 1
        elif interval == '5min':
            td = 5
        elif interval == '15min':
            td = 15
        elif interval == '30min':
            td = 30
        elif interval == '60min':
            td = 60
        else:
            td = 0
        
        data1['TimeDelta'] = td*60*1000*.75
        
        print('Pulled intraday with interval = ' + interval + '\n')
    elif pullType == 'daily':
        data1, meta_data1 = ts.get_daily_adjusted(symbol=ticker,outputsize='full')
        data1=data1.iloc[:,[0,1,2,3,5,6,7]]
        data1.columns = ['Open','High','Low','Close','Volume','Dividend','Split Coef']
        data1['TimeDelta'] = 24*60*60*1000*.75
        print('Pulled daily\n')
    elif pullType == 'weekly':
        data1, meta_data1 = ts.get_weekly_adjusted(symbol=ticker)
        data1=data1.iloc[:,[0,1,2,3,5,6]]
        data1.columns = ['Open','High','Low','Close','Volume','Dividend']
        data1['TimeDelta'] = 7*24*60*60*1000*.75
        print('Pulled weekly\n')
    elif pullType == 'monthly':
        data1, meta_data1 = ts.get_monthly_adjusted(symbol=ticker)
        data1=data1.iloc[:,[0,1,2,3,5,6]]
        data1.columns = ['Open','High','Low','Close','Volume','Dividend']
        data1['TimeDelta'] = 30*24*60*60*1000*.75
        print('Pulled monthly\n')
    else:
        print('Please enter a valid pull type')
        
    print('Data collected in dataframe data1\n')
    
    return data1
        
def save_data(df,directory,ticker):    #Saves data in the dataframe to csv format in specified directory
        df.to_csv(directory+ticker+'.csv')
        print('CSV File Saved!\n')
     
def create_macd(df,span1,span2,span3):
    df['stock_{}_ema'.format(span1)] = pd.ewma(df['Close'], span=span1)
    df['stock_{}_ema'.format(span2)] = pd.ewma(df['Close'], span=span2)
    df['macd_{}_{}'.format(span1,span2)] = df['stock_{}_ema'.format(span1)] - df['stock_{}_ema'.format(span2)]
    df['signal_{}_{}'.format(span1,span2)] = pd.ewma(df['macd_{}_{}'.format(span1,span2)], span=span3)
    df['crossover_{}_{}'.format(span1,span2)] = df['macd_{}_{}'.format(span1,span2)] - df['signal_{}_{}'.format(span1,span2)] # means, if this is > 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] > 0, there is a buy signal
    return_df = df                                                                          # means, if this is < 0, or stock_df['Crossover'] =  stock_df['MACD'] - stock_df['Signal'] < 0, there is a sell signal
    return return_df
        
    
    #print('New Plotter Object Created')
        
def candlePlot(df_in,period):
    df = df_in
    df['DT'] = pd.to_datetime(df.index)
    df['Middle'] = (df['Open']+df['Close'])/2
    df['Height'] = np.abs(df.Open-df.Close)
    
    def inc_dec(c, o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    
    
    #Calculate Hours 12 based on the input time interval        
    hours_12 = df.TimeDelta
    
    output_file("fig1.html")
    
    
    
    if period == 'intraday':
        df = df.reset_index(drop=True)
        p = figure(plot_width=1400, plot_height=700,y_axis_type="log",title=None)
        p.line(df.index,df['Middle'])
        p.segment(df.index, df.High, df.index, df.Low, color="Black")
        p.rect(df.index,df['Middle'],hours_12,df['Height'])
        p.rect(df.index[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
          hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")
        p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
          hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
        
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700,y_axis_type="log",title=None)
        p.line(df['DT'],df['Middle'])
    
        p.segment(df.DT, df.High, df.DT, df.Low, color="Black")
        
        p.rect(df['DT'],df['Middle'],hours_12,df['Height'])
    
        p.rect(df.DT[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
          hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")
    
        p.rect(df.DT[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
          hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
    
    
    show(p)
    #return df

def plotMACD(df_in,period):
    df = df_in
    df['DT'] = pd.to_datetime(df.index)
    
    hours_12 = df.TimeDelta
    
    output_file("fig2.html")

    if period == 'intraday':
        df = df.reset_index(drop=True)
        p = figure(plot_width=1400, plot_height=700,y_axis_type="log",title='Intraday MACD')
        p.line(df.index,df['Close'],line_color="black")    #Closing values
        p.line(df.index,df.iloc[:,-5],line_color="red")  #MACD with first span size
        p.line(df.index,df.iloc[:,-4],line_color="blue")  #MACD with second span size
        p.xaxis.axis_label = "Intraday Intervals"
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700,y_axis_type="log",title=None)
        
        p.line(df['DT'],df['Close'],line_color="black")    #Closing values
        p.line(df['DT'],df.iloc[:,-5],line_color="red")  #MACD with first span size
        p.line(df['DT'],df.iloc[:,-4],line_color="blue")  #MACD with second span size
    
    show(p)
    #return df
    
def plotCombined(df_in):   #Plot candle with MACD on top
    df = df_in
    df['DT'] = pd.to_datetime(df.index)
    df['Middle'] = (df['Open']+df['Close'])/2
    df['Height'] = np.abs(df.Open-df.Close)
    
    def inc_dec(c, o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    
    
    #Calculate Hours 12 based on the input time interval        
    hours_12 = df.TimeDelta
    
    output_file("fig3.html")
    
    p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700,y_axis_type="log",title=None)
    
    #p.xaxis.formatter=DatetimeTickFormatter(
    #hours=["%d %B %Y"],
    #days=["%d %B %Y"],
    #months=["%d %B %Y"],
    #years=["%d %B %Y"],
    #)
    p.segment(df.DT, df.High, df.DT, df.Low, color="Black")
    
    p.rect(df['DT'],df['Middle'],hours_12,df['Height'])

    p.rect(df.DT[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
      hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")

    p.rect(df.DT[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
      hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
      
    p.line(df['DT'],df['Close'],line_color="black")    #Closing values
    p.line(df['DT'],df.iloc[:,-5],line_color="red")  #MACD with first span size
    p.line(df['DT'],df.iloc[:,-4],line_color="blue")  #MACD with second span size
    
    show(p)
       
def plotVertical(df_in):  #Plot MACD on top of Candle Chart
    df = df_in
    #df['Year'] = df.index.str.slice(0,4).astype(int)
    #df['Day'] = df.index.str.slice(5,7).astype(int)
    #df['Month'] = df.index.str.slice(8,10).astype(int)
    df['DT'] = pd.to_datetime(df.index)
    df['Middle'] = (df['Open']+df['Close'])/2
    df['Height'] = np.abs(df.Open-df.Close)
    
    def inc_dec(c, o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    
    
    #Calculate Hours 12 based on the input time interval        
    hours_12 = df.TimeDelta
    
    output_file("fig4.html")
    
    p = figure(x_axis_type="datetime",plot_width=1400, plot_height=340,y_axis_type="log",title=None)
    
    #p.xaxis.formatter=DatetimeTickFormatter(
    #hours=["%d %B %Y"],
    #days=["%d %B %Y"],
    #months=["%d %B %Y"],
    #years=["%d %B %Y"],
    #)
    p.segment(df.DT, df.High, df.DT, df.Low, color="Black")
    
    p.rect(df['DT'],df['Middle'],hours_12,df['Height'])

    p.rect(df.DT[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
      hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")

    p.rect(df.DT[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
      hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
      
    q = figure(x_axis_type="datetime",plot_width=1400, plot_height=340,y_axis_type="log",title=None)
    q.line(df['DT'],df['Close'],line_color="black")    #Closing values
    q.line(df['DT'],df.iloc[:,-5],line_color="red")  #MACD with first span size
    q.line(df['DT'],df.iloc[:,-4],line_color="blue")  #MACD with second span size
    
    show(column(q,p))
           
           
           
           
           
        