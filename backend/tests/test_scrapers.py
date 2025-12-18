"""
Unit tests for scrapers
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.utils.scrapers import CasablancaBourseScraper, ASFIMScraper, AMMCScraper


class TestCasablancaBourseScraper:
    """Tests for Casablanca Stock Exchange scraper"""
    
    @pytest.fixture
    def scraper(self):
        return CasablancaBourseScraper()
    
    @pytest.mark.asyncio
    async def test_get_available_stocks_success(self, scraper):
        """Test successful stock list retrieval"""
        with patch.object(scraper, '_make_request') as mock_request:
            mock_response = Mock()
            mock_response.content = b'<html><body>Test</body></html>'
            mock_request.return_value = mock_response
            
            result = await scraper.get_available_stocks()
            assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_get_available_stocks_failure(self, scraper):
        """Test handling of request failure"""
        with patch.object(scraper, '_make_request', return_value=None):
            result = await scraper.get_available_stocks()
            assert result == []
    
    @pytest.mark.asyncio
    async def test_get_stock_history(self, scraper):
        """Test stock history retrieval"""
        from datetime import datetime, timedelta
        
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        result = await scraper.get_stock_history("ATW", start_date, end_date)
        assert isinstance(result, list)
    
    def test_parse_market_cap(self, scraper):
        """Test market cap parsing"""
        assert scraper._parse_market_cap("1,234.56 M MAD") == 1234560000.0
        assert scraper._parse_market_cap("Invalid") is None
    
    def test_parse_price(self, scraper):
        """Test price parsing"""
        assert scraper._parse_price("123.45 MAD") == 123.45
        assert scraper._parse_price("Invalid") is None


class TestASFIMScraper:
    """Tests for ASFIM scraper"""
    
    @pytest.fixture
    def scraper(self):
        return ASFIMScraper()
    
    @pytest.mark.asyncio
    async def test_get_opcvm_list_success(self, scraper):
        """Test successful OPCVM list retrieval"""
        with patch.object(scraper, '_make_request') as mock_request:
            mock_response = Mock()
            mock_response.content = b'<html><body>Test</body></html>'
            mock_request.return_value = mock_response
            
            result = await scraper.get_opcvm_list()
            assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_get_opcvm_performance(self, scraper):
        """Test OPCVM performance retrieval"""
        result = await scraper.get_opcvm_performance("TEST_OPCVM")
        assert isinstance(result, dict)
        assert 'opcvm_id' in result


class TestAMMCScraper:
    """Tests for AMMC scraper"""
    
    @pytest.fixture
    def scraper(self):
        return AMMCScraper()
    
    @pytest.mark.asyncio
    async def test_get_financial_statements(self, scraper):
        """Test financial statements retrieval"""
        result = await scraper.get_financial_statements("ATW")
        assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_get_market_statistics(self, scraper):
        """Test market statistics retrieval"""
        result = await scraper.get_market_statistics()
        assert isinstance(result, dict)

