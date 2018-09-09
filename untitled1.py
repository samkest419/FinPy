# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 20:37:46 2018

@author: Richard Hardis
"""

import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.stocks import AAPL

df = pd.DataFrame(AAPL)
df['date'] = pd.to_datetime(df['date'])
output_file('dt.html')
p = figure(plot_width=800,plot_height=250, x_axis_type="datetime")

p.line(df['date'],df['close'],color='navy',alpha=0.5)
show(p)