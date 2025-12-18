"""
Data endpoints - Stock and OPCVM data
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from app.api.models.data import StockData, OPCVMData
from app.api.services.data_service import DataService

router = APIRouter()
data_service = DataService()


@router.get("/stocks", response_model=List[StockData])
async def get_stocks():
    """Get available stocks from Casablanca Stock Exchange"""
    try:
        stocks = await data_service.get_available_stocks()
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks/{symbol}/history")
async def get_stock_history(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get historical data for a stock"""
    try:
        history = await data_service.get_stock_history(symbol, start_date, end_date)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/opcvm", response_model=List[OPCVMData])
async def get_opcvm_list():
    """Get available OPCVM from ASFIM"""
    try:
        opcvm_list = await data_service.get_opcvm_list()
        return opcvm_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/opcvm/{opcvm_id}/performance")
async def get_opcvm_performance(opcvm_id: str):
    """Get performance data for an OPCVM"""
    try:
        performance = await data_service.get_opcvm_performance(opcvm_id)
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

