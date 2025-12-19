"""
Script to import CSV data from Casablanca Stock Exchange
Imports historical price data for portfolio optimization
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime
from pathlib import Path
from app.database.models import StockInfo, StockPrice, SessionLocal, init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping des symboles aux noms complets
STOCK_MAPPING = {
    'ATW': {'name': 'Attijariwafa Bank', 'sector': 'Banking'},
    'BCP': {'name': 'Banque Centrale Populaire', 'sector': 'Banking'},
    'BOA': {'name': 'Bank of Africa', 'sector': 'Banking'},
    'IAM': {'name': 'Maroc Telecom', 'sector': 'Telecommunications'},
    'TAQA': {'name': 'TAQA Morocco', 'sector': 'Energy'},
    'LAA': {'name': 'LafargeHolcim Maroc', 'sector': 'Construction'},
    'LABEL': {'name': "Label'Vie", 'sector': 'Retail'},
    'WAFA': {'name': 'Wafa Assurance', 'sector': 'Insurance'},
    'TGCC': {'name': 'TGCC', 'sector': 'Construction'},
    'MNG': {'name': 'Managem', 'sector': 'Mining'},
}

# Variations possibles des noms de colonnes
COLUMN_MAPPINGS = {
    'date': ['date', 'Date', 'DATE', 'jour', 'Jour', 'Date de cotation'],
    'open': ['open', 'Open', 'OPEN', 'ouverture', 'Ouverture', 'Prix d\'ouverture'],
    'high': ['high', 'High', 'HIGH', 'haut', 'Haut', 'Prix maximum', 'Maximum'],
    'low': ['low', 'Low', 'LOW', 'bas', 'Bas', 'Prix minimum', 'Minimum'],
    'close': ['close', 'Close', 'CLOSE', 'cloture', 'Clôture', 'Prix de clôture', 'Dernier cours'],
    'volume': ['volume', 'Volume', 'VOLUME', 'vol', 'Vol', 'Volume échangé', 'Quantité'],
}


def normalize_column_name(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to standard format"""
    df = df.copy()
    
    # Try to find matching columns
    column_map = {}
    for standard_name, possible_names in COLUMN_MAPPINGS.items():
        for col in df.columns:
            if col in possible_names:
                column_map[col] = standard_name
                break
    
    # Rename columns
    df = df.rename(columns=column_map)
    
    return df


def parse_date(date_str):
    """Parse date string with multiple format support"""
    if pd.isna(date_str):
        return None
    
    date_str = str(date_str).strip()
    
    # Common date formats
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d %m %Y',
        '%d/%m/%y',
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    # Try pandas default parsing
    try:
        return pd.to_datetime(date_str)
    except:
        logger.warning(f"Could not parse date: {date_str}")
        return None


def import_csv_file(csv_path: Path, symbol: str) -> tuple[int, int]:
    """
    Import a single CSV file
    
    Returns:
        (rows_imported, rows_skipped)
    """
    db = SessionLocal()
    
    try:
        logger.info(f"\n📄 Importing {csv_path.name} for {symbol}...")
        
        # Read CSV
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            # Try with different encoding
            df = pd.read_csv(csv_path, encoding='latin-1')
        
        # Normalize column names
        df = normalize_column_name(df)
        
        # Check required columns
        required_cols = ['date', 'close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.error(f"❌ Missing required columns: {missing_cols}")
            logger.info(f"   Available columns: {list(df.columns)}")
            return 0, len(df)
        
        # Parse date
        df['date'] = df['date'].apply(parse_date)
        df = df.dropna(subset=['date'])  # Remove rows with invalid dates
        
        # Ensure close price is numeric
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df = df.dropna(subset=['close'])  # Remove rows with invalid prices
        
        # Fill missing OHLC with close price
        if 'open' not in df.columns:
            df['open'] = df['close']
        else:
            df['open'] = pd.to_numeric(df['open'], errors='coerce').fillna(df['close'])
        
        if 'high' not in df.columns:
            df['high'] = df['close']
        else:
            df['high'] = pd.to_numeric(df['high'], errors='coerce').fillna(df['close'])
        
        if 'low' not in df.columns:
            df['low'] = df['close']
        else:
            df['low'] = pd.to_numeric(df['low'], errors='coerce').fillna(df['close'])
        
        # Volume (optional, default to 0)
        if 'volume' not in df.columns:
            df['volume'] = 0
        else:
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna(0).astype(int)
        
        # Sort by date
        df = df.sort_values('date')
        
        # Get or create stock info
        stock_info = db.query(StockInfo).filter(StockInfo.symbol == symbol).first()
        if not stock_info:
            stock_mapping = STOCK_MAPPING.get(symbol, {'name': symbol, 'sector': None})
            stock_info = StockInfo(
                symbol=symbol,
                name=stock_mapping['name'],
                sector=stock_mapping['sector'],
                currency='MAD'
            )
            db.add(stock_info)
            db.commit()
            logger.info(f"   ✅ Created stock info for {symbol}")
        
        # Import price data
        rows_imported = 0
        rows_skipped = 0
        
        for _, row in df.iterrows():
            # Check if price already exists
            existing = db.query(StockPrice).filter(
                StockPrice.symbol == symbol,
                StockPrice.date == row['date']
            ).first()
            
            if existing:
                rows_skipped += 1
                continue
            
            stock_price = StockPrice(
                symbol=symbol,
                date=row['date'],
                open=float(row['open']),
                high=float(row['high']),
                low=float(row['low']),
                close=float(row['close']),
                volume=int(row['volume']),
                adjusted_close=float(row['close'])  # Assume no adjustments for now
            )
            db.add(stock_price)
            rows_imported += 1
        
        db.commit()
        
        logger.info(f"   ✅ Imported {rows_imported} rows, skipped {rows_skipped} duplicates")
        logger.info(f"   📅 Period: {df['date'].min()} to {df['date'].max()}")
        logger.info(f"   💰 Price range: {df['close'].min():.2f} - {df['close'].max():.2f} MAD")
        
        return rows_imported, rows_skipped
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error importing {csv_path.name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0, 0
    finally:
        db.close()


def main():
    """Main import function"""
    print("\n" + "📥"*30)
    print("  IMPORT CSV DATA - Bourse de Casablanca")
    print("📥"*30 + "\n")
    
    # Initialize database
    init_db()
    
    # Data directory
    data_dir = Path(__file__).parent.parent / "data" / "csv"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Find CSV files
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"❌ No CSV files found in {data_dir}")
        print(f"\n📝 Please:")
        print(f"   1. Download CSV files from Casablanca Bourse")
        print(f"   2. Place them in: {data_dir}")
        print(f"   3. Name them: ATW.csv, BCP.csv, BOA.csv, etc.")
        return
    
    print(f"📁 Found {len(csv_files)} CSV files in {data_dir}\n")
    
    # Import each file
    total_imported = 0
    total_skipped = 0
    
    for csv_file in sorted(csv_files):
        # Extract symbol from filename (e.g., ATW.csv -> ATW)
        symbol = csv_file.stem.upper()
        
        imported, skipped = import_csv_file(csv_file, symbol)
        total_imported += imported
        total_skipped += skipped
    
    print("\n" + "="*60)
    print("✅ Import completed!")
    print(f"   Total imported: {total_imported} rows")
    print(f"   Total skipped: {total_skipped} rows (duplicates)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

