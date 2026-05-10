from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field

class HistoricalData(BaseModel):
    """Historical data from yfinance API"""
    date: List[str] = Field(..., description="Date of the stock in timezone-aware ISO8601 format")
    open: List[float] = Field(..., description="Opening price of the stock")
    high: List[float] = Field(..., description="Highest price of the stock")
    low: List[float] = Field(..., description="Lowest price of the stock")
    close: List[float] = Field(..., description="Closing price of the stock")
    volume: List[int] = Field(..., description="Trading volume")
    dividends: List[float] = Field(..., description="Dividends per share")
    stock_splits: List[float]  = Field(..., description="Stock splits")

class TechnicalIndicators(BaseModel):
    """Technical indicators for stock analysis"""
    ten_day_simple_moving_average: List[float] = Field(..., description="10-day simple moving average")
    twenty_day_simple_moving_average: List[float] = Field(..., description="20-day simple moving average")
    relative_strength_index: List[float] = Field(..., description="Relative strength index")
