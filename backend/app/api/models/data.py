"""
Data models
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StockData(BaseModel):
    """Stock data model"""
    symbol: str
    name: str
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    currency: str = "MAD"


class StockHistory(BaseModel):
    """Stock historical data"""
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: float


class OPCVMData(BaseModel):
    """OPCVM data model"""
    id: str
    name: str
    category: Optional[str] = None
    nav: Optional[float] = None  # Net Asset Value
    performance_1y: Optional[float] = None
    performance_3y: Optional[float] = None
    performance_5y: Optional[float] = None

