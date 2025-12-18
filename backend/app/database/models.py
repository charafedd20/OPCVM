"""
Database models for caching market data
"""
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings

Base = declarative_base()


class StockPrice(Base):
    """Stock price historical data"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    adjusted_close = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
    )


class StockInfo(Base):
    """Stock information (metadata)"""
    __tablename__ = "stock_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    sector = Column(String(100), nullable=True)
    market_cap = Column(Float, nullable=True)
    currency = Column(String(10), default="MAD")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OPCVMData(Base):
    """OPCVM data"""
    __tablename__ = "opcvm_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    opcvm_id = Column(String(50), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)
    nav = Column(Float, nullable=True)  # Net Asset Value
    date = Column(DateTime, nullable=False, index=True)
    performance_1y = Column(Float, nullable=True)
    performance_3y = Column(Float, nullable=True)
    performance_5y = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_opcvm_date', 'opcvm_id', 'date'),
    )


class MarketIndex(Base):
    """Market indices (MASI, MASI 20, etc.)"""
    __tablename__ = "market_indices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    index_name = Column(String(50), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    variation = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_index_date', 'index_name', 'date'),
    )


# Database setup
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

