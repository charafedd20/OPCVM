"""
Unit tests for data service
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from app.api.services.data_service import DataService
from app.database.models import StockInfo, StockPrice, OPCVMData


class TestDataService:
    """Tests for DataService"""
    
    @pytest.fixture
    def service(self):
        return DataService()
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        db = Mock()
        db.query.return_value.filter.return_value.all.return_value = []
        db.query.return_value.filter.return_value.first.return_value = None
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
        db.query.return_value.distinct.return_value.all.return_value = []
        db.commit = Mock()
        db.rollback = Mock()
        db.close = Mock()
        return db
    
    @pytest.mark.asyncio
    async def test_get_available_stocks_with_cache(self, service, mock_db):
        """Test getting stocks with valid cache"""
        # Mock cached stock
        cached_stock = Mock(spec=StockInfo)
        cached_stock.symbol = "ATW"
        cached_stock.name = "Attijariwafa Bank"
        cached_stock.sector = "Banking"
        cached_stock.market_cap = 1000000000.0
        cached_stock.currency = "MAD"
        cached_stock.last_updated = datetime.utcnow() - timedelta(hours=1)
        
        mock_db.query.return_value.all.return_value = [cached_stock]
        
        with patch('app.api.services.data_service.get_db', return_value=iter([mock_db])):
            result = await service.get_available_stocks(use_cache=True)
            assert len(result) > 0
            assert result[0].symbol == "ATW"
    
    @pytest.mark.asyncio
    async def test_get_stock_history_with_cache(self, service, mock_db):
        """Test getting stock history with cache"""
        # Mock cached prices
        cached_price = Mock(spec=StockPrice)
        cached_price.symbol = "ATW"
        cached_price.date = datetime.now()
        cached_price.open = 100.0
        cached_price.high = 105.0
        cached_price.low = 99.0
        cached_price.close = 103.0
        cached_price.volume = 1000000
        cached_price.adjusted_close = 103.0
        
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [cached_price]
        
        with patch('app.api.services.data_service.get_db', return_value=iter([mock_db])):
            result = await service.get_stock_history("ATW", use_cache=True)
            assert len(result) > 0
            assert result[0]['symbol'] == "ATW"
    
    def test_is_cache_valid(self, service):
        """Test cache validation logic"""
        recent = datetime.utcnow() - timedelta(hours=1)
        old = datetime.utcnow() - timedelta(hours=25)
        
        assert service._is_cache_valid(recent) == True
        assert service._is_cache_valid(old) == False
        assert service._is_cache_valid(None) == False

