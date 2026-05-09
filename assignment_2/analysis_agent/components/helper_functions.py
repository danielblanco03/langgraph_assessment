from datetime import datetime 
from .config import config

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
   

def plot_data():
    pass

def fetch_historical_data2(ticker: str) -> dict:
    """
    Classify temperature into human-readable categories.
    
    Args:
        temp_celsius: Temperature in Celsius
        
    Returns:
        Temperature classification string
    """
    try:
        temp = float(temp_celsius)

        if temp < config.TEMP_COLD:
            return "cold"
        elif temp < config.TEMP_COOL:
            return "cool"
        elif temp < config.TEMP_COMFORTABLE:
            return "comfortable"
        elif temp < config.TEMP_WARM:
            return "warm"
        else:
            return "hot"
        
    except (ValueError, TypeError):
        return "unknown"

def get_weather_description(weather_code: int) -> str:
    """
    Get human-readable weather description from WMO code.
    
    Args:
        weather_code: WMO weather code
        
    Returns:
        Weather description string
    """
    try:
        code = int(weather_code)
        return config.WEATHER_CODE_DESCRIPTIONS.get(
            code,
            f"Weather code {code}"
        )
    except (TypeError, ValueError):
        return "Unknown weather condition"
    
def get_greeting(is_day: int) -> str:
    """
    Get appropriate greeting based on time of day.
    
    Args:
        is_day: 1 if day, 0 if night
        
    Returns:
        Greeting string
    """
    if is_day == 1:
        return "Good morning"
    else:
        return "Good evening"

def parse_utc_offset(utc_offset_str: str) -> timedelta:
    """
    Parse UTC offset string to timedelta object.
    
    Args:
        utc_offset_str: UTC offset in format '+05:30' or '-08:00'
        
    Returns:
        timedelta object representing the offset
    """
    try:
        if not utc_offset_str:
            return (timedelta(0))
        
        offset_str = utc_offset_str.strip()
        
        # Remove '+' if present and split by ':'
        sign = -1 if offset_str.startswith('-') else 1
        offset_str = offset_str.replace('+', '').replace('-', '')
        
        if ':' in offset_str:
            hours, minutes = map(int, offset_str.split(':'))
        else:
            # Handle cases like '+0530' without colon
            if len(offset_str) == 4:
                hours = int(offset_str[:2])
                minutes = int(offset_str[2:])
            else:
                hours = int(offset_str)
                minutes = 0

        # Protect against invalid offsets
        if hours > 14 or minutes > 59:
            return timedelta(0)
        
        return timedelta(hours=sign * hours, minutes=sign * minutes)
    except (ValueError, IndexError, AttributeError):
        # Default to UTC if parsing fails
        return timedelta(0)

def format_local_time(utc_time_str: str, utc_offset_str: str) -> str:
    """
    Convert UTC time to local time with timezone info.
    
    Args:
        utc_time_str: UTC time in ISO8601 format
        utc_offset_str: UTC offset string

    Example: format_local_time("2026-04-29T12:00:00Z", "+02:00")
        
    Returns:
        Formatted local time string
    """
    try:
        if not utc_time_str:
            return "Time unavailable"
                
        # Parse UTC time
        utc_time = datetime.fromisoformat(
            utc_time_str.replace('Z', '+00:00')
            )
        
        # If datetime has no timezone, assume UTC
        if utc_time.tzinfo is None:
            utc_time = utc_time.replace(tzinfo=timezone.utc)

        
        # Calculate local time
        offset = parse_utc_offset(utc_offset_str)
        local_time = utc_time + offset
        
        # Format times
        utc_formatted = utc_time.strftime("%H:%M UTC")
        local_formatted = local_time.strftime("%H:%M")

        offset_label = utc_offset_str if utc_offset_str else "+00:00"
        
        return f"{utc_formatted} | {local_formatted} (UTC{offset_label})"
    
    except Exception:
        return "Time unavailable"
    
def seconds_to_utc_offset(offset_seconds: int) -> str:
    """
    Convert UTC offset in seconds obtained in location API to string format ±HH:MM 
    as expected

    Args: offset_seconds: UTC offset in seconds (e.g., 19800 for +05:30)
    """
    try:
        total_seconds = int(offset_seconds)

        sign = "+" if total_seconds >= 0 else "-"
        total_seconds = abs(total_seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return f"{sign}{hours:02d}:{minutes:02d}"

    except (TypeError, ValueError):
        return "+00:00"