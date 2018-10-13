# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 10:35:39 2018

@author: Richard Hardis
"""

import pandas as pd
import numpy as np



def applyStrat(df_in, strategy):
    """
    Arguments:
        df_in: dataframe of open, high, low, close, volume
        strategy: strategy object with info on how to apply the strategy to a single instance
        
    Outputs:
        df: dataframe with buy and sell signals 
    """
    
    df = df_in.copy(deep=True)
    return df