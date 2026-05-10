from typing import Literal, List, Dict, Any
from datetime import datetime 
#from .config import config

import yfinance as yf
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

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

def calculate_rsi(close: np.ndarray, daysback: int = 14) -> List[float]:
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
    return rsi.tolist()

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

#closing_price, ten_day_sma, twenty_day_sma

def plot_rsi_with_candles(
        ticker,
        date,
        open, 
        high,
        low,
        closing, 
        ten_day_sma, 
        twenty_day_sma,
        rsi):
    """
    Provide important plots for visual analysis of the stock data
    Includes:
    - Closing price with 10-day and 20-day SMA
    - RSI over time
    Adapted from: 
    https://gist.github.com/rbdundas/ab5c3cc61edf200e27b506e729f47ee9#file-chart_rsi_with_candles-py

    Args:
        ticker: Stock ticker symbol for labeling the plot
        date: Array of dates corresponding to the stock data
        open: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        closing: Array of closing prices    
        ten_day_sma: Array of 10-day simple moving average values
        twenty_day_sma: Array of 20-day simple moving average values
        rsi: Array of Relative Strength Index values

    Returns:
        Displays a plot with candlestick chart and RSI
    """

    
    
    date = pd.to_datetime(date)

    open_prices = np.array(open, dtype=float)
    high_prices = np.array(high, dtype=float)
    low_prices = np.array(low, dtype=float)
    close_prices = np.array(closing, dtype=float)

    ten_day_sma = np.array(
        ten_day_sma,
        dtype=float
    )
    twenty_day_sma = np.array(
        twenty_day_sma,
        dtype=float
    )
    rsi = np.array(
        rsi,
        dtype=float
    )

    min_length = min(
        len(date),
        len(open_prices),
        len(high_prices),
        len(low_prices),
        len(close_prices),
        len(ten_day_sma),
        len(twenty_day_sma),
        len(rsi),
    )

    #Make sure all the arrays have the same length by truncating 
    #them to the minimum length

    date = date[-min_length:]
    open_prices = open_prices[-min_length:]
    high_prices = high_prices[-min_length:]
    low_prices = low_prices[-min_length:]
    close_prices = close_prices[-min_length:]
    ten_day_sma = ten_day_sma[-min_length:]
    twenty_day_sma = twenty_day_sma[-min_length:]
    rsi = rsi[-min_length:]

    up = close_prices >= open_prices
    down = close_prices < open_prices

    fig, ax = plt.subplots(
        2,
        1,
        figsize=(12, 8),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    fig.suptitle(ticker)

    width = 0.5
    wick_width = 0.05

    ax[0].grid(True)
    ax[0].set_ylabel("Price")

    #Build the candle from the 3 different components:
    #1. The body of the candle (the rectangle between open and close)
    #2. The upper wick (the line from the top of the body to the high
    #3. The lower wick (the line from the bottom of the body to the low)

    ax[0].bar(
        date[up], #Select the dates where the price went up
        close_prices[up] - open_prices[up], #Height of the bar
        width,
        bottom=open_prices[up], #Where the bar starts
        color="green",
    )
    ax[0].bar(
        date[up],
        high_prices[up] - close_prices[up], #Upper wick height
        wick_width,
        bottom=close_prices[up],
        color="green",
    )
    ax[0].bar(
        date[up],
        low_prices[up] - open_prices[up], #Lower wick height
        wick_width,
        bottom=open_prices[up],
        color="green",
    )

    ax[0].bar(
        date[down], #Select the dates where the price went down
        close_prices[down] - open_prices[down],
        width,
        bottom=open_prices[down],
        color="red",
    )
    ax[0].bar(
        date[down],
        high_prices[down] - open_prices[down],
        wick_width,
        bottom=open_prices[down],
        color="red",
    )
    ax[0].bar(
        date[down],
        low_prices[down] - close_prices[down],
        wick_width,
        bottom=close_prices[down],
        color="red",
    )

    ax[0].plot(date, ten_day_sma, label="10-day SMA")
    ax[0].plot(date, twenty_day_sma, label="20-day SMA")
    ax[0].legend()

    ax[1].plot(date, rsi)
    ax[1].set_ylim(0, 100)
    ax[1].axhline(y=70, color="red", linestyle="-")
    ax[1].axhline(y=30, color="red", linestyle="-")
    ax[1].grid(True)
    ax[1].set_ylabel("RSI")

    for label in ax[1].get_xticklabels(which="major"):
        label.set(rotation=30, horizontalalignment="right")

    plt.tight_layout()
    plt.show()

def format_datetime_index(index: pd.DatetimeIndex) -> List[str]:
    """
    Format a pandas DatetimeIndex to timezone-aware ISO8601 strings

    Args:
        index: Pandas DatetimeIndex to be formatted

    Returns:
        List of formatted datetime strings in ISO8601 format
    """
    formatted = index.strftime("%Y-%m-%dT%H:%M:%S%z")

    #Insert colon in timezone offset (-0500 -> -05:00)
    return [d[:-2] + ":" + d[-2:] for d in formatted]