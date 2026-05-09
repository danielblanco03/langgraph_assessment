from typing import Literal, List, Dict, Any
from datetime import datetime 
#from .config import config

import yfinance as yf
import numpy as np
import pandas as pd
from pandas import DataFrame

def fetch_historical_data(ticker: str, t_interval: str='60d') -> DataFrame:
    """
    Fetch historical stock data for the given ticker and time
    interval using the yfinance library

    Args:
        ticker: Stock ticker to be analyzed
        t_interval: Time interval for historical data

    Returns:
        DataFrame containing historical stock data
    """
    try:
        dat = yf.Ticker(ticker)
        #Get historical market data
        historical_data = dat.history(period=t_interval)
        return historical_data
    except (ValueError, TypeError):
        return "unknown"
    
def calculate_simple_moving_average(
        data: np.ndarray, 
        window_size: int=10
    ) -> List[float]:
    """
    Calculate the Simple Moving Average (SMA) for a given 
    data array and window size

    Args:
        data: NumPy array of stock prices
        window_size: Window size for the moving average

    Returns:
        List of Simple Moving Average values
    """
    if window_size <= 0:
        raise ValueError("window_size must be > 0")
    if window_size > len(data):
        raise ValueError("window_size cannot be larger than data length")

    i = 0
    #Initialize an empty list to store the SMA values
    sma_values = []

    #Loop through the data and calculate the SMA for each window
    for i in range(len(data) - window_size + 1):

        #Calculate the average of the current window and append it to the 
        #sma_values list
        window_average = np.mean(data[i:i+window_size])
        sma_values.append(window_average)

    return sma_values

def calculate_rsi(close: pd.Series, daysback: int = 14) -> List[float]:
    """
    Calculate the Relative Strength Index (RSI) for a given array of closing prices
    and a specified number of days back.

    The RSI is a momentum indicator that measures the speed and magnitude of recent price
    changes to evaluate overbought or oversold conditions in the price of a stock.

    Basic Formula:
    RSI = 100 - (100 / (1+(avg. of upward price change / avg. of downward price change)))

    Args:
        close: Pandas Series of closing prices
        daysback: Number of days to look back for calculating the RSI (default is 14)

    Returns:
        DataFrame containing the RSI values indexed by date
    """
    if daysback <= 0:
        raise ValueError("daysback must be greater than 0")

    if len(close) <= daysback:
        raise ValueError("close must contain more values than daysback")

    #Find difference between consecutive closing prices in the array
    retrace = close.diff()
    up = []
    down = []

    for i in range(len(retrace)):
        #Determine whether the price change is an upward movement (positive) 
        #or a downward movement (negative)
        if retrace.iloc[i] < 0:
            up.append(0)
            down.append(retrace.iloc[i])
        else:
            up.append(retrace.iloc[i])
            down.append(0)

    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    
    #compute smoothed averages off gains and losses using an exponential moving average
    #Recent values are given more weight than older values, which allows the RSI to respond more quickly to recent price changes
    #Use adjust=False to use recursive formula: EWM_t = alpha * value_t + (1 - alpha) * EWMA_{t-1}
    #So at each time step: avg_gain_today = (1/daysback)*gain_today + (1 - 1/daysback)*avg_gain_yesterday
    #avg_loss_today = (1/daysback)*loss_today + (1 - 1/daysback)*avg_loss_yesterday  

    up_ewm = up_series.ewm(alpha = 1 / daysback, adjust=False).mean() #alpha controls the degree of weighting decay
    down_ewm = down_series.ewm(alpha = 1 / daysback, adjust=False).mean()

    #Divide the average gain by the average loss to get the relative strength (RS)
    rs = up_ewm / down_ewm
    rsi = 100 - (100 / (1 + rs))
    return rsi.dropna().tolist()

def generate_recommendation(
    ten_day_sma: List[float],
    twenty_day_sma: List[float],
    rsi: List[float],
):
    """
    Provide BUY/HOLD/SELL recommendation based on SMA crossover and RSI.
    Logic:
    - If 10-day SMA > 20-day SMA and 50 < RSI < 70: BUY ("Golden Cross" logic)
    - If 10-day SMA < 20-day SMA and 50 > RSI > 30: SELL ("Death Cross" logic)
    - Otherwise: HOLD

    Args:
        ten_day_sma: 10-day simple moving average values
        twenty_day_sma: 20-day simple moving average values
        rsi: Relative Strength Index values

    Returns:
        "BUY", "HOLD", or "SELL"
    """

    if not ten_day_sma or not twenty_day_sma or not rsi:
        raise ValueError("Indicator lists cannot be empty")

    latest_10_sma = ten_day_sma[-1]
    latest_20_sma = twenty_day_sma[-1]
    latest_rsi = rsi[-1]

    if latest_10_sma > latest_20_sma and 50 < latest_rsi < 70:
        return "BUY"

    if latest_10_sma < latest_20_sma and 50 > latest_rsi > 30:
        return "SELL"

    return "HOLD"

def plot_data():
    pass

