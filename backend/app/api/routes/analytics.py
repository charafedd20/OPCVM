"""
Analytics endpoints - Data analysis and visualization
Business-focused: Provides insights on scraped data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database.models import StockPrice, StockInfo, OPCVMData, get_db
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/analytics/stocks/summary")
async def get_stocks_summary():
    """
    Get summary statistics for all stocks
    
    Returns:
        - Total number of stocks
        - Sectors distribution
        - Market cap statistics
        - Most traded stocks
    """
    db = next(get_db())
    
    try:
        # Total stocks
        total_stocks = db.query(StockInfo).count()
        
        # Sector distribution
        sector_dist = db.query(
            StockInfo.sector,
            func.count(StockInfo.id).label('count')
        ).group_by(StockInfo.sector).all()
        
        sectors = {sector: count for sector, count in sector_dist if sector}
        
        # Market cap statistics
        market_caps = db.query(StockInfo.market_cap).filter(
            StockInfo.market_cap.isnot(None)
        ).all()
        
        market_cap_values = [mc[0] for mc in market_caps if mc[0] is not None]
        
        market_cap_stats = {
            "total": len(market_cap_values),
            "sum": sum(market_cap_values) if market_cap_values else 0,
            "mean": np.mean(market_cap_values) if market_cap_values else 0,
            "median": np.median(market_cap_values) if market_cap_values else 0,
            "min": min(market_cap_values) if market_cap_values else 0,
            "max": max(market_cap_values) if market_cap_values else 0
        }
        
        # Most traded stocks (by volume)
        most_traded = db.query(
            StockPrice.symbol,
            func.sum(StockPrice.volume).label('total_volume')
        ).group_by(StockPrice.symbol).order_by(
            desc('total_volume')
        ).limit(10).all()
        
        # Get stock names for most traded
        most_traded_with_names = []
        for symbol, volume in most_traded:
            stock_info = db.query(StockInfo).filter(StockInfo.symbol == symbol).first()
            most_traded_with_names.append({
                "symbol": symbol,
                "name": stock_info.name if stock_info else symbol,
                "total_volume": int(volume)
            })
        
        # Get all stocks with full info
        all_stocks = db.query(StockInfo).all()
        stocks_list = [
            {
                "symbol": s.symbol,
                "name": s.name,
                "sector": s.sector,
                "market_cap": s.market_cap
            }
            for s in all_stocks
        ]
        
        return {
            "total_stocks": total_stocks,
            "sectors": sectors,
            "market_cap_statistics": market_cap_stats,
            "most_traded_stocks": most_traded_with_names,
            "stocks": stocks_list,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in get_stocks_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/analytics/stocks/{symbol}/statistics")
async def get_stock_statistics(
    symbol: str,
    days: int = Query(30, description="Number of days for statistics")
):
    """
    Get detailed statistics for a specific stock
    
    Returns:
        - Price statistics (mean, std, min, max)
        - Volume statistics
        - Returns (daily, weekly, monthly)
        - Volatility
        - Price trends
    """
    db = next(get_db())
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get price data
        prices = db.query(StockPrice).filter(
            StockPrice.symbol == symbol,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        if not prices:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for symbol {symbol}"
            )
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([{
            'date': p.date,
            'open': p.open,
            'high': p.high,
            'low': p.low,
            'close': p.close,
            'volume': p.volume
        } for p in prices])
        
        # Calculate returns
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        
        # Price statistics
        price_stats = {
            "open": {
                "mean": float(df['open'].mean()),
                "std": float(df['open'].std()),
                "min": float(df['open'].min()),
                "max": float(df['open'].max())
            },
            "close": {
                "mean": float(df['close'].mean()),
                "std": float(df['close'].std()),
                "min": float(df['close'].min()),
                "max": float(df['close'].max())
            },
            "high": {
                "mean": float(df['high'].mean()),
                "max": float(df['high'].max())
            },
            "low": {
                "mean": float(df['low'].mean()),
                "min": float(df['low'].min())
            }
        }
        
        # Volume statistics
        volume_stats = {
            "mean": float(df['volume'].mean()),
            "std": float(df['volume'].std()),
            "min": int(df['volume'].min()),
            "max": int(df['volume'].max()),
            "total": int(df['volume'].sum())
        }
        
        # Returns statistics
        returns_stats = {
            "mean_daily": float(df['returns'].mean()),
            "std_daily": float(df['returns'].std()),
            "volatility_annualized": float(df['returns'].std() * np.sqrt(252)),
            "total_return": float((df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100),
            "sharpe_ratio": float(df['returns'].mean() / df['returns'].std() * np.sqrt(252)) if df['returns'].std() > 0 else 0
        }
        
        # Price trends
        price_trend = {
            "first_price": float(df['close'].iloc[0]),
            "last_price": float(df['close'].iloc[-1]),
            "change": float(df['close'].iloc[-1] - df['close'].iloc[0]),
            "change_percent": float((df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100)
        }
        
        return {
            "symbol": symbol,
            "period_days": days,
            "data_points": len(prices),
            "price_statistics": price_stats,
            "volume_statistics": volume_stats,
            "returns_statistics": returns_stats,
            "price_trend": price_trend,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/analytics/stocks/{symbol}/chart-data")
async def get_stock_chart_data(
    symbol: str,
    days: int = Query(30, description="Number of days"),
    chart_type: str = Query("line", description="Chart type: line, candlestick, volume")
):
    """
    Get formatted data for charting
    
    Returns:
        Data formatted for visualization libraries (Recharts, Plotly, etc.)
    """
    db = next(get_db())
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        prices = db.query(StockPrice).filter(
            StockPrice.symbol == symbol,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        if not prices:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for symbol {symbol}"
            )
        
        if chart_type == "line":
            data = [{
                "date": p.date.isoformat(),
                "price": float(p.close),
                "volume": int(p.volume)
            } for p in prices]
        
        elif chart_type == "candlestick":
            data = [{
                "date": p.date.isoformat(),
                "open": float(p.open),
                "high": float(p.high),
                "low": float(p.low),
                "close": float(p.close),
                "volume": int(p.volume)
            } for p in prices]
        
        elif chart_type == "volume":
            data = [{
                "date": p.date.isoformat(),
                "volume": int(p.volume),
                "price": float(p.close)
            } for p in prices]
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid chart_type: {chart_type}. Use 'line', 'candlestick', or 'volume'"
            )
        
        return {
            "symbol": symbol,
            "chart_type": chart_type,
            "data_points": len(data),
            "data": data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_chart_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/analytics/opcvm/summary")
async def get_opcvm_summary():
    """
    Get summary statistics for OPCVM
    
    Returns:
        - Total OPCVM count
        - Category distribution
        - Performance statistics
        - Best/worst performers
    """
    db = next(get_db())
    
    try:
        # Total OPCVM
        total_opcvm = db.query(OPCVMData.opcvm_id).distinct().count()
        
        # Category distribution
        category_dist = db.query(
            OPCVMData.category,
            func.count(func.distinct(OPCVMData.opcvm_id)).label('count')
        ).filter(
            OPCVMData.category.isnot(None)
        ).group_by(OPCVMData.category).all()
        
        categories = {cat: count for cat, count in category_dist if cat}
        
        # Performance statistics
        latest_opcvm = db.query(OPCVMData).order_by(
            OPCVMData.date.desc()
        ).all()
        
        # Get unique OPCVM with latest data
        opcvm_dict = {}
        for opcvm in latest_opcvm:
            if opcvm.opcvm_id not in opcvm_dict:
                opcvm_dict[opcvm.opcvm_id] = opcvm
        
        performances_1y = [o.performance_1y for o in opcvm_dict.values() if o.performance_1y is not None]
        performances_3y = [o.performance_3y for o in opcvm_dict.values() if o.performance_3y is not None]
        
        # Best and worst performers
        best_performers = sorted(
            [(o.opcvm_id, o.name, o.performance_1y) 
             for o in opcvm_dict.values() if o.performance_1y is not None],
            key=lambda x: x[2],
            reverse=True
        )[:10]
        
        worst_performers = sorted(
            [(o.opcvm_id, o.name, o.performance_1y) 
             for o in opcvm_dict.values() if o.performance_1y is not None],
            key=lambda x: x[2]
        )[:10]
        
        return {
            "total_opcvm": total_opcvm,
            "categories": categories,
            "performance_statistics": {
                "1y": {
                    "count": len(performances_1y),
                    "mean": float(np.mean(performances_1y)) if performances_1y else None,
                    "median": float(np.median(performances_1y)) if performances_1y else None,
                    "min": float(min(performances_1y)) if performances_1y else None,
                    "max": float(max(performances_1y)) if performances_1y else None
                },
                "3y": {
                    "count": len(performances_3y),
                    "mean": float(np.mean(performances_3y)) if performances_3y else None,
                    "median": float(np.median(performances_3y)) if performances_3y else None
                }
            },
            "best_performers_1y": [
                {"id": id, "name": name, "performance": float(perf)}
                for id, name, perf in best_performers
            ],
            "worst_performers_1y": [
                {"id": id, "name": name, "performance": float(perf)}
                for id, name, perf in worst_performers
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in get_opcvm_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/analytics/market/overview")
async def get_market_overview():
    """
    Get overall market overview
    
    Returns:
        - Market statistics
        - Sector performance
        - Market trends
    """
    db = next(get_db())
    
    try:
        # Stock statistics
        total_stocks = db.query(StockInfo).count()
        stocks_with_data = db.query(StockPrice.symbol).distinct().count()
        
        # Recent trading activity
        last_30_days = datetime.now() - timedelta(days=30)
        recent_volume = db.query(
            func.sum(StockPrice.volume)
        ).filter(
            StockPrice.date >= last_30_days
        ).scalar() or 0
        
        # Sector distribution
        sectors = db.query(
            StockInfo.sector,
            func.count(StockInfo.id).label('count')
        ).filter(
            StockInfo.sector.isnot(None)
        ).group_by(StockInfo.sector).all()
        
        return {
            "market_statistics": {
                "total_listed_stocks": total_stocks,
                "stocks_with_price_data": stocks_with_data,
                "coverage_percentage": float(stocks_with_data / total_stocks * 100) if total_stocks > 0 else 0
            },
            "trading_activity": {
                "last_30_days_volume": int(recent_volume),
                "average_daily_volume": int(recent_volume / 30) if recent_volume > 0 else 0
            },
            "sector_distribution": {
                sector: count for sector, count in sectors
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in get_market_overview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

