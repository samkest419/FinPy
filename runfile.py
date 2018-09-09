# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:03:59 2018

@author: Richard Hardis
"""
from finpy import *

data = Fin_Data()       #Create a new data object that we will use to pull the data

spy = data.pull_data('SPY','monthly','60min')
data.save_data(spy, 'C:\\Users\\Richard Hardis\\Documents\\GitHub\\FinPy\\','SPY')

plotter = Plotter()

#plotter.bPlot(spy)
#sp = spy.iloc[:5,[0,3]]
#plotter.basicPlot(sp)

outspy = plotter.candlePlot(spy)


