from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field

class HistoricalData(BaseModel):
    """Historical data from yfinance API"""
    stock: str = Field(..., description="Stock symbol")
    date: str = Field(..., description="Date of the stock in timezone-aware ISO8601 format")
    open: float = Field(..., description="Opening price of the stock")
    high: float = Field(..., description="Highest price of the stock")
    low: float = Field(..., description="Lowest price of the stock")
    close: float = Field(..., description="Closing price of the stock")
    volume: int = Field(..., description="Trading volume")
    dividends: float = Field(..., description="Dividends per share")
    stock_splits: float = Field(..., description="Stock splits")

class TechnicalIndicators(BaseModel):
    """Technical indicators for stock analysis"""
    ten_day_simple_moving_average: List[float] = Field(..., description="10-day simple moving average")
    twenty_day_simple_moving_average: List[float] = Field(..., description="20-day simple moving average")
    relative_stength_index: float = Field(..., description="Relative strength index")

class RecomendationIndicator(BaseModel):
    """Complete weather response from Open-Meteo API"""
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    timezone: str = Field(..., description="Timezone")
    utc_offset_seconds: int = Field(..., description="UTC offset in seconds")
    current_weather_units: CurrentWeatherUnits = Field(..., description="Units for weather data")
    current_weather: CurrentWeather = Field(..., description="Current weather conditions")

class AnalysisReport(BaseModel):
    pass