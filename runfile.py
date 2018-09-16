# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
from finpy import *

data = Fin_Data()       #Create a new data object that we will use to pull the data

ticker = 'SPY'
period = 'monthly'
interval = '60min'

spy = data.pull_data(ticker,period,interval)                                      #Pull data
data.save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')  #Save the data to csv format

plotter = Plotter() #Create plotting object
plotter.candlePlot(spy)    #Plot the candleplot

macd = MACD()
spy_macd = macd.create_macd(spy,5,15,3)
plotter.plotMACD(spy)
plotter.plotVertical(spy)

