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
from bokeh.models import DatetimeTickFormatter, LinearAxis, Range1d, ColumnDataSource, HoverTool

import pandas as pd
import numpy as np
from datetime import datetime as dt
import smtplib
    
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
    data1['DT'] = data1.index
    print(type(data1.DT[0]))
    #data1['DT'] = pd.to_datetime(data1.index)
    #data1['DT'] = data1.DT.strftime('%Y/%d/%m/%H/%M')
    return data1
        
def save_data(df,directory,ticker):    #Saves data in the dataframe to csv format in specified directory
        df.to_csv(directory+ticker+'.csv')
        print('CSV File Saved!\n')

def candlePlot(df_in,period):
    df = df_in.copy(deep=True)
    
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
    
def plotCombined(df_in,period):   #Plot candle with MACD on top
    df = df_in.copy(deep=True)
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
        p.line(df.index,df['Close'],line_color="black")    #Closing values
        p.line(df.index,df.iloc[:,-5],line_color="red")  #MACD with first span size
        p.line(df.index,df.iloc[:,-4],line_color="blue")  #MACD with second span size
        p.xaxis.axis_label = "Intraday Intervals"
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700,y_axis_type="log",title=None)
        
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
       
def plotVertical(df_in,period):  #Plot MACD on top of Candle Chart
    df = df_in.copy(deep=True)
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
    
    if period == 'intraday':
        df = df.reset_index(drop=True)
        p = figure(plot_width=1400, plot_height=340,y_axis_type="log",title=None)
        
        p.segment(df.index, df.High, df.index, df.Low, color="Black")
        
        p.rect(df.index,df['Middle'],hours_12,df['Height'])
    
        p.rect(df.index[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
          hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")
    
        p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
          hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
          
        q = figure(plot_width=1400, plot_height=340,y_axis_type="log",title=None)
        q.line(df.index,df['Close'],line_color="black")    #Closing values
        q.line(df.index,df.iloc[:,-8],line_color="red")  #MACD with first span size
        q.line(df.index,df.iloc[:,-7],line_color="blue")  #MACD with second span size
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=340,y_axis_type="log",title=None)
        
        p.segment(df.DT, df.High, df.DT, df.Low, color="Black")
        
        p.rect(df['DT'],df['Middle'],hours_12,df['Height'])
    
        p.rect(df.DT[df.Status=='Increase'],df.Middle[df.Status=="Increase"],
          hours_12, df.Height[df.Status=="Increase"],fill_color="#CCFFFF",line_color="black")
    
        p.rect(df.DT[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
          hours_12, df.Height[df.Status=="Decrease"],fill_color="#FF3333",line_color="black")
          
        q = figure(x_axis_type="datetime",plot_width=1400, plot_height=340,y_axis_type="log",title=None)
        q.line(df['DT'],df['Close'],line_color="black")    #Closing values
        q.line(df['DT'],df.iloc[:,-8],line_color="red")  #MACD with first span size
        q.line(df['DT'],df.iloc[:,-7],line_color="blue")  #MACD with second span size
    
    show(column(q,p))
           

def plotCMFMACD(df_in,period):
    df = df_in.copy(deep=True)
    
    output_file("fig5.html")
    if period == 'intraday':
        df = df.reset_index(drop=True)
        p = figure(plot_width=1400, plot_height=700,title='Intraday CMF MACD')
        #p.line(df.index,df['Fast MF'],line_color="black",legend="CMF Fast")    #Closing values
        #p.line(df.index,df['mf_fast_ema'],line_color="red",legend="CMF Slow")  #Stock MA with first span size
        p.line(df.index,df['CMF MACD'],line_color="black",legend="MACD")  #Stock MA with second span size
        p.line(df.index,df['CMF Signal'],line_color="blue",legend="Signal")  #Stock MA with second span size
        p.xaxis.axis_label = "Intraday Intervals"
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700,title=None)
        
        p.line(df['DT'],df['Period CMF'],line_color="black")    #Closing values
        p.line(df['DT'],df['mf_fast_ema'],line_color="red")  #Stock MA with first span size
        p.line(df['DT'],df['mf_slow_ema'],line_color="blue")  #Stock MA with second span size
        
    show(p)

def plotMultiY(xvals, *args):
    output_file("OverlaidMutliY.html")
    
    source = ColumnDataSource(data={
            'Interval':xvals,
            'Close':args[0],
            'MACD':args[1],
            })
    
    offset = 0.05 * (np.max(args[0])-np.min(args[0]))
    p = figure(plot_width=1400, plot_height=700, y_range = (np.min(args[0])-offset,np.max(args[0])+offset), sizing_mode="scale_width")
    plot1 = p.line(x='Interval',y='Close',color="black",line_width=2,source=source)
    p.add_tools(HoverTool(
        renderers=[plot1],
        tooltips=[('Close', '@Close')],
        formatters={'Close':'printf'},
        mode='vline'
        ))
    
    i=2
    arg=args[1]    
    colors = ["blue","red","green","orange","yellow"]
    offset = 0.05 * (np.max(arg)-np.min(arg))
    p.extra_y_ranges = {'Y{}'.format(i): Range1d(start=np.min(arg)-offset, end=np.max(arg)+offset)}
    plot2 = p.line(x='Interval', y='MACD', y_range_name='Y{}'.format(i),line_width=0.5,color=colors[0],alpha=0.5, source=source)
    p.add_layout(LinearAxis(y_range_name='Y{}'.format(i)), 'right')
    p.add_tools(HoverTool(
        renderers=[plot2],
        tooltips=[('MACD', '@MACD')],
        formatters={'MACD':'printf'},
        mode='vline'
        ))
    
    tools = 'crosshair'
    
    #if len(args) > 1:    
    #    for i, arg in enumerate(args[1:]):
    #        p.extra_y_ranges = {'Y{}'.format(i): Range1d(start=np.min(arg), end=np.max(arg))}
    #        p.line(xvals, arg, y_range_name='Y{}'.format(i),line_width=1,color=colors[i],alpha=0.5)
    #        p.add_layout(LinearAxis(y_range_name='Y{}'.format(i)), 'right')
    show(p)

def plotMACD(df_in,period):
    df = df_in.copy(deep=True)    
    output_file("MACD.html")
    
    arg = df.Close
    offset = 0.05 * (np.max(arg)-np.min(arg))
    
    if period == 'intraday':
        df = df.reset_index(drop=True)
        df['DT'] = df.index
        p = figure(plot_width=1400, plot_height=700, y_range = (np.min(arg)-offset,np.max(arg)+offset),title='Intraday MACD', sizing_mode="scale_width")
        #
        p.xaxis.axis_label = "Intraday Intervals"
    else:
        p = figure(x_axis_type="datetime",plot_width=1400, plot_height=700, y_range = (np.min(arg)-offset,np.max(arg)+offset),title=None, sizing_mode="scale_width")
        #,y_axis_type="log"
    source = ColumnDataSource(data=df)
    
    plot1 = p.line(x='DT',y='Close',line_color="blue", legend="Close Price", source=source)    #Closing values
    p.add_tools(HoverTool(
        renderers=[plot1],
        tooltips=[('Close', '@Close'),('Time','@DT')],
        formatters={'Close':'printf'},
        mode='vline'
        ))

    arg = df.macd
    offset = 0.05 * (np.max(arg) - np.min(arg))
    p.extra_y_ranges = {'Y2': Range1d(start=np.min(arg)-offset, end=offset*20*5)}  
    plot2 = p.line(x='DT', y ='crossover', y_range_name='Y2', line_color="red", legend="MACD Cross Value", source=source)
    p.add_layout(LinearAxis(y_range_name='Y2'), 'right')
    p.line(x='DT',y='macd',line_color="black", y_range_name='Y2', alpha=0.25, source=source)
    p.line(x='DT',y='signal',line_color="black", y_range_name='Y2', line_dash='dashed', alpha=0.25, source=source)
    p.line(x='DT', y=0, line_color="black",y_range_name='Y2', source=source)
    p.add_tools(HoverTool(
        renderers=[plot2],
        tooltips=[('Crossover', '@crossover'),('Time','@DT')],
        formatters={'Crossover':'printf'},
        mode='vline'
        ))

    show(p)
    return df, p
           
def emailSignal(to_address,df): 
    curr_time = str(dt.now())
    latest_signal = df.iloc[-1,-1]
    message = str(df.iloc[-1,:])
    conn = smtplib.SMTP('smtp.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login('Rich.Sam.Signals@gmail.com','n3wp34f$!')
    conn.sendmail('Rich.Sam.Signals@gmail.com',to_address,'Subject: SPY Signal {}\n\n{} SPY\n\n{}'.format(curr_time,latest_signal,message))
           
def is_new(df):
    #Compare the latest state of the dataframe to the current time.  If the dataframe time is over a minute before the dataframe time then signal not new data.
    last_call = dt.strptime(df.index[-1], '%Y-%m-%d')
    print(last_call)
    now = dt.now()
    print('Delta:\n')
    print(now-last_call)
    state = 'T'
    return state 

def macdHistogram(df_in):
    df = df_in.copy(deep=True)
    output_file("MACDHistogram.html")
    hist, edges = np.histogram(df['macd'], density=True, bins=30)
    p = figure(title='MACD Histogram', sizing_mode='scale_both', background_fill_color = "#E8DDCB")
    p.quad(top = hist , bottom = 0, left = edges[:-1], right = edges[1:], fill_color = "#036564", line_color = "#033649")
    
    minMACD = np.min(df.macd)
    maxMACD = np.max(df.macd)
    mu = np.mean(df.macd)
    sigma = np.std(df.macd)
    x = np.linspace(minMACD,maxMACD,1000)
    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))       
    p.line(x, pdf, line_color="#D95B43", line_width=2, alpha=0.7, legend="PDF")
    
    p.ray(x=[-1*sigma, sigma], y=[0,0], length=50, angle=90, angle_units="deg", color="blue", line_width=1)
    p.ray(x=[-2*sigma, 2*sigma], y=[0,0], length=50, angle=90, angle_units="deg", color="red", line_width=1)
    p.ray(x=[-3*sigma, 3*sigma], y=[0,0], length=50, angle=90, angle_units="deg", color="green", line_width=1)
    p.ray(x=0,y=0,length=50,angle=90,angle_units="deg",color="black",line_width=2)     
    show(p)


def ichimoku_plot(close, conversion, base, lead_a, lead_b, lagging, conversion_span, base_span, leading_b_span):
    periods = np.arange(0,len(lead_b))
    output_file("IchimokuPlot.html")
    p = figure(title='Ichi Plot. Conversion Span = {}, Base Span = {}, Leading B Span = {}'.format(conversion_span, base_span, leading_b_span),
                plot_width=1400, plot_height=700, sizing_mode="scale_width")
    small=0.2
    large=3
#    p.line(periods, conversion, color='blue', line_width=small)
#    p.line(periods, lagging, color='green', line_width=small)
#    p.line(periods, base, color='red', line_width=small)
#    p.line(periods, lead_a, color='green', line_width=large)
#    p.line(periods, lead_b, color='red', line_width=large)
    p.multi_line([periods,periods,periods,periods,periods,periods], [conversion,base,lagging,lead_a,lead_b,close],
                 color=['blue','red','green','green','red','black'], line_width=[small,small,small,large,large,large/2])
#    legend = Legend(items=[
#            LegendItem(label='')])
    show(p)
           
    