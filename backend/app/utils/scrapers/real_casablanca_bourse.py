"""
Real scraper for Casablanca Stock Exchange
Scrapes actual data from the website
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
import ssl
import urllib3
from app.core.config import settings

# Disable SSL warnings for testing (to be configured properly in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class RealCasablancaBourseScraper:
    """
    Real scraper that actually fetches data from Casablanca Stock Exchange
    """
    
    def __init__(self):
        self.base_url = settings.CASABLANCA_BOURSE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.timeout = 30
        # For SSL issues, we'll verify=False in development (NOT for production!)
        self.verify_ssl = False  # TODO: Configure proper SSL certificates
    
    def _make_request(self, url: str, params: Optional[Dict] = None, retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with error handling and SSL workaround"""
        for attempt in range(retries):
            try:
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
                response.raise_for_status()
                return response
            except requests.exceptions.SSLError as e:
                logger.warning(f"SSL error for {url}, trying without verification: {str(e)}")
                # Try without SSL verification (development only)
                try:
                    response = self.session.get(
                        url,
                        params=params,
                        timeout=self.timeout,
                        verify=False
                    )
                    response.raise_for_status()
                    return response
                except Exception as e2:
                    logger.error(f"Error fetching {url}: {str(e2)}")
                    if attempt == retries - 1:
                        return None
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {url} (attempt {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    return None
                import time
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    async def get_available_stocks(self) -> List[Dict]:
        """
        Get list of all available stocks from Casablanca Stock Exchange
        REAL scraping implementation
        """
        url = f"{self.base_url}/fr/instruments"
        response = self._make_request(url)
        
        if not response:
            logger.error("Failed to fetch stocks list from Casablanca Bourse")
            return []
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            stocks = []
            
            # Strategy 0: Extract from JSON in scripts (Next.js app)
            scripts = soup.find_all('script')
            for script in scripts:
                content = script.string or ''
                # Look for JSON data with instruments
                if '__NEXT_DATA__' in content or 'instruments' in content.lower() or 'ticker' in content.lower():
                    try:
                        import json
                        import re
                        # Try to extract JSON
                        json_match = re.search(r'\{.*"props".*\}', content, re.DOTALL)
                        if json_match:
                            data = json.loads(json_match.group())
                            # Navigate through Next.js data structure
                            # This needs to be adapted based on actual structure
                            logger.debug("Found JSON data in script")
                    except:
                        pass
            
            # Strategy 1: Look for tables with stock data (found structure: table with class 'w-full')
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 2:  # Need at least header + 1 data row
                    continue
                
                # Parse header to understand column structure
                header = rows[0]
                header_cells = header.find_all(['th', 'td'])
                header_texts = [cell.get_text(strip=True) for cell in header_cells]
                
                # Find column indices
                ticker_idx = -1
                instrument_idx = -1
                for i, text in enumerate(header_texts):
                    if 'ticker' in text.lower() or 'symbole' in text.lower():
                        ticker_idx = i
                    if 'instrument' in text.lower() or 'nom' in text.lower():
                        instrument_idx = i
                
                # Parse data rows
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 2:
                        continue
                    
                    # Extract symbol (ticker)
                    if ticker_idx >= 0 and ticker_idx < len(cells):
                        symbol = cells[ticker_idx].get_text(strip=True).upper()
                    else:
                        # Try to find symbol in any cell (usually short uppercase)
                        symbol = None
                        for cell in cells:
                            text = cell.get_text(strip=True).upper()
                            if len(text) <= 5 and text.isalpha() and text.isupper():
                                symbol = text
                                break
                    
                    # Extract name (instrument)
                    if instrument_idx >= 0 and instrument_idx < len(cells):
                        name = cells[instrument_idx].get_text(strip=True)
                    else:
                        name = None
                    
                    # Filter valid stock symbols
                    if symbol and len(symbol) >= 2 and len(symbol) <= 5:
                        stocks.append({
                            'symbol': symbol,
                            'name': name or symbol,
                            'sector': None,  # Will need to find this
                            'market_cap': None,  # Will need to find this
                            'currency': 'MAD'
                        })
            
            # Strategy 2: Look for links with stock symbols
            if not stocks:
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    # Look for patterns like /instruments/ATW or ?symbol=ATW
                    if '/instruments/' in href or 'symbol=' in href:
                        symbol = href.split('/instruments/')[-1].split('?')[0].split('&')[0] if '/instruments/' in href else href.split('symbol=')[-1].split('&')[0]
                        if symbol and len(symbol) <= 5:
                            stocks.append({
                                'symbol': symbol.upper(),
                                'name': text or symbol,
                                'sector': None,
                                'market_cap': None,
                                'currency': 'MAD'
                            })
            
            # Remove duplicates
            seen = set()
            unique_stocks = []
            for stock in stocks:
                if stock['symbol'] not in seen:
                    seen.add(stock['symbol'])
                    unique_stocks.append(stock)
            
            logger.info(f"Scraped {len(unique_stocks)} stocks from Casablanca Bourse")
            return unique_stocks
            
        except Exception as e:
            logger.error(f"Error parsing stocks list: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    async def get_stock_history_real(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Get REAL historical price data for a stock from Casablanca Bourse
        
        Args:
            symbol: Stock symbol (CSH, AKD, SGT, ATW, etc.)
            start_date: Start date
            end_date: End date
        
        Returns:
            List of real price dictionaries
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        # Try different URL patterns for historical data
        urls_to_try = [
            f"{self.base_url}/fr/instruments/{symbol}/historique",
            f"{self.base_url}/fr/cours/{symbol}",
            f"{self.base_url}/fr/data/historique/{symbol}",
            f"{self.base_url}/fr/instruments/{symbol}?period=historical",
        ]
        
        prices = []
        
        for url in urls_to_try:
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'symbol': symbol
            }
            
            response = self._make_request(url, params=params)
            if response:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    parsed_prices = self._parse_price_table_real(soup, symbol, start_date, end_date)
                    if parsed_prices:
                        prices.extend(parsed_prices)
                        logger.info(f"Successfully scraped {len(parsed_prices)} price points for {symbol}")
                        break
                except Exception as e:
                    logger.warning(f"Error parsing history from {url}: {str(e)}")
                    continue
        
        if not prices:
            logger.warning(f"Could not scrape real data for {symbol}, returning empty list")
            logger.info("NOTE: You may need to implement the actual HTML parsing based on the website structure")
        
        return prices
    
    def _parse_price_table_real(
        self,
        soup: BeautifulSoup,
        symbol: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Parse real price table from HTML"""
        prices = []
        
        # Look for tables with price data
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cells = row.find_all(['td', 'th'])
                
                if len(cells) >= 5:  # Date, Open, High, Low, Close, Volume
                    try:
                        # Extract date (usually first column)
                        date_str = cells[0].get_text(strip=True)
                        price_date = self._parse_date_real(date_str)
                        
                        if not price_date or price_date < start_date or price_date > end_date:
                            continue
                        
                        # Extract prices
                        open_price = self._parse_price_real(cells[1].get_text(strip=True))
                        high_price = self._parse_price_real(cells[2].get_text(strip=True))
                        low_price = self._parse_price_real(cells[3].get_text(strip=True))
                        close_price = self._parse_price_real(cells[4].get_text(strip=True))
                        volume = self._parse_volume_real(cells[5].get_text(strip=True)) if len(cells) > 5 else 0
                        
                        if price_date and close_price:
                            prices.append({
                                'date': price_date,
                                'open': open_price or close_price,
                                'high': high_price or close_price,
                                'low': low_price or close_price,
                                'close': close_price,
                                'volume': volume,
                                'adjusted_close': close_price
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing row: {str(e)}")
                        continue
        
        return prices
    
    def _parse_date_real(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime - handles various formats"""
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%d %m %Y',
            '%d %B %Y',  # 15 décembre 2024
            '%d %b %Y',  # 15 déc 2024
        ]
        
        date_str = date_str.strip()
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        
        # Try to extract date from complex strings
        import re
        date_match = re.search(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', date_str)
        if date_match:
            day, month, year = date_match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except:
                pass
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    def _parse_price_real(self, price_str: str) -> Optional[float]:
        """Parse price string to float"""
        if not price_str:
            return None
        
        try:
            # Remove currency symbols, spaces, commas
            cleaned = price_str.replace('MAD', '').replace('DH', '').replace(' ', '').replace(',', '').replace('€', '').replace('$', '').strip()
            # Handle French decimal separator
            cleaned = cleaned.replace(' ', '').replace('\xa0', '')  # Non-breaking space
            return float(cleaned)
        except Exception as e:
            logger.debug(f"Could not parse price '{price_str}': {str(e)}")
            return None
    
    def _parse_volume_real(self, volume_str: str) -> int:
        """Parse volume string to int"""
        if not volume_str:
            return 0
        
        try:
            # Remove spaces, commas, and handle K, M suffixes
            cleaned = volume_str.replace(' ', '').replace(',', '').replace('\xa0', '').strip().upper()
            
            multiplier = 1
            if cleaned.endswith('K'):
                multiplier = 1000
                cleaned = cleaned[:-1]
            elif cleaned.endswith('M'):
                multiplier = 1000000
                cleaned = cleaned[:-1]
            
            return int(float(cleaned) * multiplier)
        except:
            return 0
    
    def _parse_market_cap(self, text: str) -> Optional[float]:
        """Parse market capitalization"""
        if not text:
            return None
        
        try:
            # Remove currency and handle M (millions), B (billions)
            cleaned = text.replace('MAD', '').replace(' ', '').replace(',', '').strip().upper()
            
            multiplier = 1
            if 'B' in cleaned or 'MM' in cleaned:
                multiplier = 1_000_000_000
                cleaned = cleaned.replace('B', '').replace('MM', '')
            elif 'M' in cleaned:
                multiplier = 1_000_000
                cleaned = cleaned.replace('M', '')
            
            return float(cleaned) * multiplier
        except:
            return None

