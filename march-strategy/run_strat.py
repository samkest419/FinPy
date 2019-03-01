# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 20:37:23 2019

@author: Richard Hardis
"""
import numpy as np
import pandas as pd


class securityData:
    def __init__(self):
        self.tickers = ['spy']
        self.macd_window = [1,1,1]
        self.stoch_window = [1,1,1]
        self.criteria = 5
        



def main():
    # 1. Create an instance of the securityData class
    sd = securityData()
    
    # 2. Loop over all of the tickers in sd and calculate the stochastic value for each
    tlist = []
    tvalues = []
    for ticker in sd.tickers:
        tlist.append(ticker)
        tvalues.append(calculate_stochastic(ticker, sd.macd_args, sd.stoch_args))
        
    
    # 3. Combine all results into a single dataframe
    combined_df = pd.DataFrame({'tickers':tlist, 'stoch_values':tvalues})
    
    
    # 4. Filter the dataframe based on our desired cutoff values.
    combined_df = combined_df[combined_df.stoch_values > sd.criteria]
    
    # 5. Send an email containing the list of all of the securities that match the criteria
    
    
    
def calculate_stochastic(ticker, macd_args, stoch_args):
    """
    Calculates the stochastic value of the provided ticker and returns a list with ticker name and value
    
    Args:
        ticker (string): the acronym representing the ticker to look up
        macd_args (list): a list of the three macd values
        stoch_args (list): a list of the three stochastic values
        
    Returns:
        result_list (float): the numeric value of the stochastic
    """
    result_list = None
    ticker_df = get_ticker_data(ticker)
    
    # Run some math on the ticker dataframe
    stoch_val = None

    # Make result list
    result_list = stoch_val 
    
    
    return result_list


def get_ticker_data(ticker):
    ticker_df = None
    
    return ticker_df

def email_blast(results_df, emails):
    
    print('emails away!')

if __name__ == '__main__':
    main()