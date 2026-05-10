import requests
import numpy as np
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
        ticker = state.get("ticker")

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

def generate_technical_indicators(state: AnalysisAgentState) -> AnalysisAgentState:
    """
    Generate technical indicators from historical stock data.

    Args:
        state: Current agent state with historical_data populated

    Returns:
        Updated state with technical_data populated
    """
    historical_data = state.get("historical_data")

    if not historical_data:
        raise ValueError("Historical data not available for technical indicator generation")

    try:
        close_prices = np.array(historical_data["close"], dtype=float)

        if len(close_prices) < 20:
            raise ValueError("At least 20 closing prices are required")

        ten_day_sma = calculate_simple_moving_average(
            close_prices,
            window_size=10,
        )

        twenty_day_sma = calculate_simple_moving_average(
            close_prices,
            window_size=20,
        )

        rsi = calculate_rsi(
            close_prices,
            daysback=14,
        )

        technical_data = {
            "ten_day_simple_moving_average": ten_day_sma,
            "twenty_day_simple_moving_average": twenty_day_sma,
            "relative_strength_index": rsi,
        }

        state["technical_data"] = technical_data

    except Exception as e:
        raise RuntimeError(f"Error generating technical indicators: {e}") from e
    
    return state

def generate_recommendation_node(state: AnalysisAgentState) -> AnalysisAgentState:
    """
    Generate trading signal recommendation based on technical indicators.

    Args:
        state: Current agent state with historical_data andtechnical_data populated

    Returns:
        Updated state with recommendation_info populated
    """
    if not state.get("historical_data") or not state.get("technical_data"):
        raise ValueError(
            "Historical data or technical data not available for recommendation generation"
        )
    try: 
        stock = state["ticker"]
        historical_data = state["historical_data"]
        technical_data = state["technical_data"]

        ten_day_sma = technical_data["ten_day_simple_moving_average"]
        twenty_day_sma = technical_data["twenty_day_simple_moving_average"]
        rsi = technical_data["relative_strength_index"]

        if not ten_day_sma or not twenty_day_sma or not rsi:
            raise ValueError("Technical indicator lists cannot be empty")

        recommendation = generate_recommendation(
            ten_day_sma,
            twenty_day_sma,
            rsi
        )
        # Build comprehensive recommendation string
        recommendation_parts = [
            f"Stock: {stock}",
            "",
            f"The current recommendation for {stock} is: {recommendation}",
            "",
            f"Current technical indicator values:",
            f"• 10-day SMA: {ten_day_sma[-1]:.2f}",
            f"• 20-day SMA: {twenty_day_sma[-1]:.2f}",
            f"• RSI: {rsi[-1]:.2f}"
        ]

        state["recommendation_info"] = "\n".join(recommendation_parts)

    except KeyError as e:
        raise KeyError(f"Missing data field for recommendation generation: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error generating recommendation: {e}") from e
    
    return state

