"""
Data service - Business logic for market data
Handles caching, data validation, and business rules
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import StockPrice, StockInfo, OPCVMData, MarketIndex, get_db
from app.utils.scrapers import CasablancaBourseScraper, ASFIMScraper, AMMCScraper
from app.api.models.data import StockData, OPCVMData as OPCVMDataModel
import logging

logger = logging.getLogger(__name__)


class DataService:
    """
    Service for fetching and caching market data
    
    Business logic:
    - Caches data to reduce API calls and improve performance
    - Validates data before returning
    - Handles errors gracefully
    - Provides fresh data when cache is stale
    """
    
    def __init__(self):
        self.bourse_scraper = CasablancaBourseScraper()
        self.asfim_scraper = ASFIMScraper()
        self.ammc_scraper = AMMCScraper()
        self.cache_ttl_hours = 24  # Cache data for 24 hours
    
    def _is_cache_valid(self, last_updated: datetime) -> bool:
        """Check if cached data is still valid"""
        if not last_updated:
            return False
        age = datetime.utcnow() - last_updated
        return age < timedelta(hours=self.cache_ttl_hours)
    
    async def get_available_stocks(self, use_cache: bool = True) -> List[StockData]:
        """
        Get list of available stocks from Casablanca Stock Exchange
        
        Args:
            use_cache: Whether to use cached data if available
        
        Returns:
            List of StockData objects
        """
        db = next(get_db())
        
        try:
            # Check cache first
            if use_cache:
                cached_stocks = db.query(StockInfo).all()
                if cached_stocks and self._is_cache_valid(
                    max(s.last_updated for s in cached_stocks) if cached_stocks else None
                ):
                    logger.info("Returning cached stocks data")
                    return [
                        StockData(
                            symbol=s.symbol,
                            name=s.name,
                            sector=s.sector,
                            market_cap=s.market_cap,
                            currency=s.currency
                        )
                        for s in cached_stocks
                    ]
            
            # Fetch fresh data
            logger.info("Fetching fresh stocks data from Casablanca Bourse")
            stocks_data = await self.bourse_scraper.get_available_stocks()
            
            # Update cache
            for stock_dict in stocks_data:
                stock_info = db.query(StockInfo).filter(
                    StockInfo.symbol == stock_dict.get('symbol')
                ).first()
                
                if stock_info:
                    # Update existing
                    stock_info.name = stock_dict.get('name', stock_info.name)
                    stock_info.sector = stock_dict.get('sector')
                    stock_info.market_cap = stock_dict.get('market_cap')
                    stock_info.last_updated = datetime.utcnow()
                else:
                    # Create new
                    stock_info = StockInfo(
                        symbol=stock_dict.get('symbol'),
                        name=stock_dict.get('name'),
                        sector=stock_dict.get('sector'),
                        market_cap=stock_dict.get('market_cap'),
                        currency=stock_dict.get('currency', 'MAD')
                    )
                    db.add(stock_info)
            
            db.commit()
            
            # Return as StockData objects
            return [
                StockData(
                    symbol=s.get('symbol'),
                    name=s.get('name'),
                    sector=s.get('sector'),
                    market_cap=s.get('market_cap'),
                    currency=s.get('currency', 'MAD')
                )
                for s in stocks_data
            ]
            
        except Exception as e:
            logger.error(f"Error fetching stocks: {str(e)}")
            db.rollback()
            # Return cached data as fallback
            cached_stocks = db.query(StockInfo).all()
            return [
                StockData(
                    symbol=s.symbol,
                    name=s.name,
                    sector=s.sector,
                    market_cap=s.market_cap,
                    currency=s.currency
                )
                for s in cached_stocks
            ]
        finally:
            db.close()
    
    async def get_stock_history(
        self, 
        symbol: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        Get historical data for a stock
        
        Args:
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            use_cache: Whether to use cached data
        
        Returns:
            List of price dictionaries
        """
        db = next(get_db())
        
        try:
            # Parse dates
            start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
            
            if not start_dt:
                start_dt = end_dt - timedelta(days=365)  # Default: 1 year
            
            # Check cache
            if use_cache:
                cached_prices = db.query(StockPrice).filter(
                    StockPrice.symbol == symbol,
                    StockPrice.date >= start_dt,
                    StockPrice.date <= end_dt
                ).order_by(StockPrice.date).all()
                
                if cached_prices:
                    logger.info(f"Returning {len(cached_prices)} cached prices for {symbol}")
                    return [
                        {
                            'date': p.date.isoformat(),
                            'open': p.open,
                            'high': p.high,
                            'low': p.low,
                            'close': p.close,
                            'volume': p.volume,
                            'adjusted_close': p.adjusted_close
                        }
                        for p in cached_prices
                    ]
            
            # Fetch fresh data
            logger.info(f"Fetching fresh price data for {symbol}")
            prices = await self.bourse_scraper.get_stock_history(symbol, start_dt, end_dt)
            
            # Update cache
            for price_dict in prices:
                price_date = datetime.fromisoformat(price_dict['date']) if isinstance(price_dict['date'], str) else price_dict['date']
                
                existing = db.query(StockPrice).filter(
                    StockPrice.symbol == symbol,
                    StockPrice.date == price_date
                ).first()
                
                if not existing:
                    stock_price = StockPrice(
                        symbol=symbol,
                        date=price_date,
                        open=price_dict.get('open'),
                        high=price_dict.get('high'),
                        low=price_dict.get('low'),
                        close=price_dict.get('close'),
                        volume=price_dict.get('volume', 0),
                        adjusted_close=price_dict.get('adjusted_close')
                    )
                    db.add(stock_price)
            
            db.commit()
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching stock history for {symbol}: {str(e)}")
            db.rollback()
            return []
        finally:
            db.close()
    
    async def get_opcvm_list(self, use_cache: bool = True) -> List[OPCVMDataModel]:
        """Get list of available OPCVM from ASFIM"""
        db = next(get_db())
        
        try:
            # Check cache
            if use_cache:
                cached_opcvm = db.query(OPCVMData).distinct(OPCVMData.opcvm_id).all()
                if cached_opcvm:
                    logger.info("Returning cached OPCVM list")
                    return [
                        OPCVMDataModel(
                            id=o.opcvm_id,
                            name=o.name,
                            category=o.category,
                            nav=o.nav,
                            performance_1y=o.performance_1y,
                            performance_3y=o.performance_3y,
                            performance_5y=o.performance_5y
                        )
                        for o in cached_opcvm
                    ]
            
            # Fetch fresh data
            opcvm_data = await self.asfim_scraper.get_opcvm_list()
            
            # Update cache (simplified - would need more logic for full update)
            return [
                OPCVMDataModel(
                    id=o.get('id'),
                    name=o.get('name'),
                    category=o.get('category'),
                    nav=None,
                    performance_1y=None,
                    performance_3y=None,
                    performance_5y=None
                )
                for o in opcvm_data
            ]
            
        except Exception as e:
            logger.error(f"Error fetching OPCVM list: {str(e)}")
            return []
        finally:
            db.close()
    
    async def get_opcvm_performance(self, opcvm_id: str) -> Dict:
        """Get performance data for an OPCVM"""
        db = next(get_db())
        
        try:
            # Check cache
            latest = db.query(OPCVMData).filter(
                OPCVMData.opcvm_id == opcvm_id
            ).order_by(OPCVMData.date.desc()).first()
            
            if latest and self._is_cache_valid(latest.created_at):
                return {
                    'opcvm_id': latest.opcvm_id,
                    'nav': latest.nav,
                    'performance_1y': latest.performance_1y,
                    'performance_3y': latest.performance_3y,
                    'performance_5y': latest.performance_5y,
                    'date': latest.date.isoformat()
                }
            
            # Fetch fresh data
            performance = await self.asfim_scraper.get_opcvm_performance(opcvm_id)
            
            # Update cache
            if performance:
                opcvm_data = OPCVMData(
                    opcvm_id=performance.get('opcvm_id'),
                    name=performance.get('name', ''),
                    nav=performance.get('nav'),
                    date=performance.get('date', datetime.now()),
                    performance_1y=performance.get('performance_1y'),
                    performance_3y=performance.get('performance_3y'),
                    performance_5y=performance.get('performance_5y')
                )
                db.add(opcvm_data)
                db.commit()
            
            return performance
            
        except Exception as e:
            logger.error(f"Error fetching OPCVM performance: {str(e)}")
            return {}
        finally:
            db.close()
