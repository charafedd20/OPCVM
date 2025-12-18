"""
Script to seed extended historical data (1 year, 3 years, 5 years)
Creates comprehensive historical data for better portfolio optimization
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import StockInfo, StockPrice, OPCVMData, init_db, SessionLocal
from datetime import datetime, timedelta
import random
import numpy as np

def seed_extended_stock_data(years: int = 3):
    """
    Seed extended historical data for stocks
    
    Args:
        years: Number of years of data to generate (1, 3, or 5)
    """
    db = SessionLocal()
    
    try:
        # Get all existing stocks
        stocks = db.query(StockInfo).all()
        
        if not stocks:
            print("❌ No stocks found. Please run seed_test_data.py first.")
            return
        
        print(f"\n🌱 Generating {years} years of historical data for {len(stocks)} stocks...")
        print("="*60)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        # Approximate trading days (252 per year)
        max_trading_days = years * 252
        
        for stock in stocks:
            symbol = stock.symbol
            base_price = random.uniform(10, 200)  # Realistic base price
            current_date = start_date
            current_price = base_price
            trading_days_count = 0
            prices_added = 0
            
            print(f"\n📊 Processing {symbol} ({stock.name})...")
            
            while current_date <= end_date and trading_days_count < max_trading_days:
                # Only trading days (Monday-Friday)
                if current_date.weekday() < 5:
                    # Check if price already exists
                    existing = db.query(StockPrice).filter(
                        StockPrice.symbol == symbol,
                        StockPrice.date == current_date
                    ).first()
                    
                    if not existing:
                        # Generate realistic price movement
                        # Add slight trend based on sector
                        sector_trend = {
                            "Banking": 0.15,  # 15% growth over period
                            "Telecommunications": 0.10,
                            "Construction": 0.05,
                            "Financial Services": 0.12,
                            "Healthcare": 0.20,  # Healthcare grows faster
                        }
                        
                        trend = sector_trend.get(stock.sector, 0.10)
                        trend_factor = 1 + (trading_days_count / max_trading_days) * trend
                        
                        # Daily volatility
                        daily_change = random.gauss(0, 0.02)  # Normal distribution, 2% std
                        current_price = current_price * (1 + daily_change) * (1 + trend / max_trading_days)
                        
                        # Ensure price stays positive and realistic
                        current_price = max(1.0, current_price)
                        
                        # Generate OHLC
                        high = current_price * random.uniform(1.0, 1.025)
                        low = current_price * random.uniform(0.975, 1.0)
                        open_price = current_price * random.uniform(0.99, 1.01)
                        
                        # Volume varies by day of week (lower on Monday/Friday)
                        base_volume = random.randint(50000, 3000000)
                        if current_date.weekday() == 0 or current_date.weekday() == 4:
                            volume = int(base_volume * 0.8)  # Lower on Mon/Fri
                        else:
                            volume = base_volume
                        
                        stock_price = StockPrice(
                            symbol=symbol,
                            date=current_date,
                            open=round(open_price, 2),
                            high=round(high, 2),
                            low=round(low, 2),
                            close=round(current_price, 2),
                            volume=volume,
                            adjusted_close=round(current_price, 2)
                        )
                        db.add(stock_price)
                        prices_added += 1
                        trading_days_count += 1
                
                current_date += timedelta(days=1)
            
            db.commit()
            print(f"   ✅ Added {prices_added} price points for {symbol}")
        
        print(f"\n✅ Extended data seeding completed!")
        print(f"   Total period: {years} years")
        print(f"   Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print("="*60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding extended data: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed extended historical data')
    parser.add_argument('--years', type=int, default=3, choices=[1, 3, 5],
                        help='Number of years of data to generate (default: 3)')
    
    args = parser.parse_args()
    
    print("\n" + "🚀"*30)
    print("  EXTENDED DATA SEEDING")
    print("🚀"*30)
    
    # Initialize database
    init_db()
    
    # Seed extended data
    seed_extended_stock_data(years=args.years)


if __name__ == "__main__":
    main()

