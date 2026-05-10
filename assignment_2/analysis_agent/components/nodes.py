import requests
from typing import Dict, List, Any
from .state import AnalysisAgentState
from .config import config
from .helper_functions import (
    fetch_historical_data, 
    calculate_simple_moving_average, 
    calculate_rsi,
    generate_recommendation,
    format_datetime_index
)

def fetch_stock_data(state: AnalysisAgentState) -> AnalysisAgentState:
    """
    Fetch historical stock data data for a given ticker using yfinance

    Args:
        state: Current agent state

    Returns:
        Updated state with historical_data populated
    """
    try:
        ticker = state.get["ticker"]

        if not ticker:
            raise ValueError('Ticker is missing from agent state')
        
        raw_historical_data = fetch_historical_data(ticker, t_interval="60d")

        if raw_historical_data is None or raw_historical_data.empty:
            raise ValueError(f"No historical data found for ticker: {ticker}")

        #Validate required fields
        required_fields = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

        for field in required_fields:
            if field not in raw_historical_data.columns:
                raise ValueError(f"Missing required field in historical data: {field}")

        #Save historical data in the expected format
        #JSON safe and Pydantic-friendly format

        historical_data = {
            #make date go: index --> Series --> formatted --> list
            "date": format_datetime_index(raw_historical_data.index),
            "open": raw_historical_data["Open"].astype(float).tolist(),
            "high": raw_historical_data["High"].astype(float).tolist(),
            "low": raw_historical_data["Low"].astype(float).tolist(),
            "close": raw_historical_data["Close"].astype(float).tolist(),
            "volume": raw_historical_data["Volume"].astype(int).tolist(),
            "dividends": raw_historical_data["Dividends"].astype(float).tolist(),
            "stock_splits": raw_historical_data["Stock Splits"].astype(float).tolist(),
        }

        state["historical_data"] = historical_data

    except Exception as e:
        raise Exception(f"Unexpected error fetching historical data: {str(e)}")
    
    return state



def fetch_weather_data(state: WeatherAgentState) -> WeatherAgentState:
    """
    Fetch current weather data using Open-Meteo API based on location coordinates.
    
    Args:
        state: Current agent state with location_data populated
        
    Returns:
        Updated state with weather_data populated
    """
    if not state.get("location_data"):
        raise Exception("Location data not available for weather fetch")
    
    location = state["location_data"]
    
    try:
        # Construct weather API URL with parameters
        params = {
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            "current_weather": True
        }

        response = requests.get(
            config.WEATHER_API_BASE_URL,
            params=params,
            timeout=config.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Validate required fields
        if 'current_weather' not in weather_data:
            raise ValueError("Missing current_weather data in response")
        
        
        current_weather = weather_data['current_weather']

        required_weather_fields = [
            'time', 
            'temperature', 
            'windspeed', 
            'winddirection', 
            'is_day', 
            'weathercode'
            ]
        
        for field in required_weather_fields:
            if field not in current_weather:
                raise ValueError(f"Missing required weather field: {field}")
        
        state["weather_data"] = weather_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid weather data received: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching weather: {str(e)}")
    
    return state

def generate_weather_info(state: WeatherAgentState) -> WeatherAgentState:
    """
    Generate formatted weather information string combining location and weather data.
    
    Args:
        state: Current agent state with location_data and weather_data populated
        
    Returns:
        Updated state with weather_info populated
    """
    if not state.get("location_data") or not state.get("weather_data"):
        raise Exception("Location or weather data not available for info generation")
    
    try:
        # Extract data
        location = state["location_data"]
        weather = state["weather_data"]["current_weather"]
        units = state["weather_data"].get("current_weather_units", {})

        name = state["name"]
        city = location["city"]
        region = location["region"]
        country = location["country_name"]
        utc_offset = location["utc_offset"]
        
        temperature = weather["temperature"]
        temp_unit = units.get("temperature", "°C")
        windspeed = weather["windspeed"]
        wind_unit = units.get("windspeed", "km/h")
        is_day = weather["is_day"]
        weather_code = weather["weathercode"]
        utc_time = weather["time"]
        
        # Generate components
        greeting = get_greeting(is_day)
        temp_classification = classify_temperature(temperature)
        weather_description = get_weather_description(weather_code)
        time_info = format_local_time(utc_time, utc_offset)
        
        # Build comprehensive weather info string
        weather_info_parts = [
            f"Time: {time_info}",
            "",
            f"{greeting}, {name}!",
            "",
            f"Your current location: {city}, {region}, {country}",
            "",
            f"Current weather conditions:",
            f"• {weather_description}",
            f"• Temperature: {temperature}{temp_unit} ({temp_classification})",
            f"• Wind: {windspeed}{wind_unit}"
        ]
        
        state["weather_info"] = "\n".join(weather_info_parts)
        
    except KeyError as e:
        raise Exception(f"Missing data field for weather info generation: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating weather info: {str(e)}")
    
    return state