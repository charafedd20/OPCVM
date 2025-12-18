"""
Data endpoints - Stock and OPCVM data
Business-focused endpoints with caching and error handling
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.api.models.data import StockData, OPCVMData
from app.api.services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
data_service = DataService()


@router.get("/stocks", response_model=List[StockData])
async def get_stocks(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get available stocks from Casablanca Stock Exchange
    
    - **use_cache**: Use cached data (faster) or fetch fresh data
    - Returns list of stocks with symbol, name, sector, market cap
    """
    try:
        stocks = await data_service.get_available_stocks(use_cache=use_cache)
        if not stocks:
            logger.warning("No stocks returned from service")
        return stocks
    except Exception as e:
        logger.error(f"Error in get_stocks endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching stocks: {str(e)}"
        )


@router.get("/stocks/{symbol}/history")
async def get_stock_history(
    symbol: str,
    start_date: Optional[str] = Query(
        None, 
        description="Start date (YYYY-MM-DD format)",
        regex=r'^\d{4}-\d{2}-\d{2}$'
    ),
    end_date: Optional[str] = Query(
        None,
        description="End date (YYYY-MM-DD format)",
        regex=r'^\d{4}-\d{2}-\d{2}$'
    ),
    days: Optional[int] = Query(
        None,
        description="Number of days back from end_date (alternative to start_date)",
        ge=1,
        le=3650  # Max 10 years
    ),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get historical price data for a stock
    
    - **symbol**: Stock symbol (e.g., "ATW", "IAM", "CSH", "AKD", "SGT")
    - **start_date**: Start date in YYYY-MM-DD format (optional)
    - **end_date**: End date in YYYY-MM-DD format (default: today)
    - **days**: Number of days back from end_date (alternative to start_date, max 3650)
    - **use_cache**: Use cached data or fetch fresh
    
    Returns list of price data with date, open, high, low, close, volume
    """
    try:
        # Handle days parameter
        if days and not start_date:
            from datetime import datetime, timedelta
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
            start_date = (end_dt - timedelta(days=days)).strftime('%Y-%m-%d')
            logger.info(f"Using days parameter: {days} days back from {end_dt.strftime('%Y-%m-%d')}")
        
        # Validate date format if provided
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be in YYYY-MM-DD format"
                )
        
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="end_date must be in YYYY-MM-DD format"
                )
        
        history = await data_service.get_stock_history(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            use_cache=use_cache
        )
        
        if not history:
            logger.warning(f"No history found for symbol {symbol}")
        
        return {
            "symbol": symbol,
            "count": len(history),
            "data": history
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_history endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock history: {str(e)}"
        )


@router.get("/opcvm", response_model=List[OPCVMData])
async def get_opcvm_list(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get available OPCVM from ASFIM
    
    - **use_cache**: Use cached data or fetch fresh
    - Returns list of OPCVM with id, name, category, NAV, performances
    """
    try:
        opcvm_list = await data_service.get_opcvm_list(use_cache=use_cache)
        if not opcvm_list:
            logger.warning("No OPCVM returned from service")
        return opcvm_list
    except Exception as e:
        logger.error(f"Error in get_opcvm_list endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching OPCVM list: {str(e)}"
        )


@router.get("/opcvm/{opcvm_id}/performance")
async def get_opcvm_performance(
    opcvm_id: str,
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get performance data for a specific OPCVM
    
    - **opcvm_id**: OPCVM identifier
    - **use_cache**: Use cached data or fetch fresh
    
    Returns NAV, performances (1y, 3y, 5y), and date
    """
    try:
        if not opcvm_id:
            raise HTTPException(status_code=400, detail="opcvm_id is required")
        
        performance = await data_service.get_opcvm_performance(opcvm_id)
        
        if not performance:
            raise HTTPException(
                status_code=404,
                detail=f"OPCVM {opcvm_id} not found"
            )
        
        return performance
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_opcvm_performance endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching OPCVM performance: {str(e)}"
        )

