"""
Script to seed test data for demonstration
Creates sample stock and OPCVM data for testing endpoints
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import StockInfo, StockPrice, OPCVMData, init_db, SessionLocal
from datetime import datetime, timedelta
import random
import numpy as np

def seed_stock_data():
    """Seed sample stock data"""
    db = SessionLocal()
    
    try:
        # Sample stocks - Including requested stocks: Cashplus, Akdital, SGTM
        stocks = [
            {"symbol": "ATW", "name": "Attijariwafa Bank", "sector": "Banking", "market_cap": 50000000000},
            {"symbol": "IAM", "name": "Itissalat Al-Maghrib", "sector": "Telecommunications", "market_cap": 30000000000},
            {"symbol": "BCP", "name": "Banque Centrale Populaire", "sector": "Banking", "market_cap": 40000000000},
            {"symbol": "LAA", "name": "LafargeHolcim Maroc", "sector": "Construction", "market_cap": 15000000000},
            {"symbol": "CDM", "name": "Ciments du Maroc", "sector": "Construction", "market_cap": 8000000000},
            {"symbol": "CSH", "name": "Cashplus", "sector": "Financial Services", "market_cap": 5000000000},
            {"symbol": "AKD", "name": "Akdital", "sector": "Healthcare", "market_cap": 3000000000},
            {"symbol": "SGT", "name": "SGTM - Société Générale des Travaux du Maroc", "sector": "Construction", "market_cap": 2000000000},
        ]
        
        # Create stock info
        for stock in stocks:
            existing = db.query(StockInfo).filter(StockInfo.symbol == stock["symbol"]).first()
            if not existing:
                stock_info = StockInfo(
                    symbol=stock["symbol"],
                    name=stock["name"],
                    sector=stock["sector"],
                    market_cap=stock["market_cap"],
                    currency="MAD"
                )
                db.add(stock_info)
        
        db.commit()
        
        # Generate price history for last 90 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        for stock in stocks:
            symbol = stock["symbol"]
            base_price = random.uniform(50, 200)
            
            current_date = start_date
            current_price = base_price
            
            while current_date <= end_date:
                # Check if price already exists
                existing = db.query(StockPrice).filter(
                    StockPrice.symbol == symbol,
                    StockPrice.date == current_date
                ).first()
                
                if not existing:
                    # Generate realistic price movement
                    change = random.uniform(-0.03, 0.03)  # ±3% daily change
                    current_price = current_price * (1 + change)
                    
                    high = current_price * random.uniform(1.0, 1.02)
                    low = current_price * random.uniform(0.98, 1.0)
                    open_price = current_price * random.uniform(0.99, 1.01)
                    volume = random.randint(100000, 5000000)
                    
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
                
                current_date += timedelta(days=1)
        
        db.commit()
        print(f"✅ Seeded stock data for {len(stocks)} stocks")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding stock data: {str(e)}")
    finally:
        db.close()


def seed_opcvm_data():
    """Seed sample OPCVM data"""
    db = SessionLocal()
    
    try:
        opcvm_list = [
            {"id": "OPCVM_001", "name": "Fond Actions Maroc", "category": "Actions"},
            {"id": "OPCVM_002", "name": "Fond Obligations", "category": "Obligations"},
            {"id": "OPCVM_003", "name": "Fond Mixte", "category": "Mixte"},
            {"id": "OPCVM_004", "name": "Fond Monétaire", "category": "Monétaire"},
        ]
        
        for opcvm in opcvm_list:
            opcvm_data = OPCVMData(
                opcvm_id=opcvm["id"],
                name=opcvm["name"],
                category=opcvm["category"],
                nav=random.uniform(100, 500),
                date=datetime.now(),
                performance_1y=random.uniform(-5, 15),
                performance_3y=random.uniform(0, 20),
                performance_5y=random.uniform(5, 25)
            )
            db.add(opcvm_data)
        
        db.commit()
        print(f"✅ Seeded OPCVM data for {len(opcvm_list)} OPCVM")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding OPCVM data: {str(e)}")
    finally:
        db.close()


def main():
    """Main seeding function"""
    print("\n🌱 Seeding test data...")
    print("="*60)
    
    # Initialize database
    init_db()
    
    # Seed data
    seed_stock_data()
    seed_opcvm_data()
    
    print("\n✅ Seeding completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

