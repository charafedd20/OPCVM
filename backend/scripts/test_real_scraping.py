"""
Script to test REAL scraping from Casablanca Stock Exchange
Verifies that we can actually fetch real data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from app.utils.scrapers.real_casablanca_bourse import RealCasablancaBourseScraper
from datetime import datetime, timedelta

async def test_real_scraping():
    """Test real scraping functionality"""
    print("\n" + "🔍"*30)
    print("  TEST DE SCRAPING RÉEL - Bourse de Casablanca")
    print("🔍"*30 + "\n")
    
    scraper = RealCasablancaBourseScraper()
    
    # Test 1: Get available stocks
    print("="*60)
    print("Test 1: Récupération de la liste des actions")
    print("="*60)
    stocks = await scraper.get_available_stocks()
    print(f"\n✅ Actions trouvées: {len(stocks)}")
    
    if stocks:
        print("\n📊 Premières actions:")
        for stock in stocks[:10]:
            print(f"  - {stock['symbol']}: {stock['name']} ({stock.get('sector', 'N/A')})")
    else:
        print("❌ Aucune action trouvée - Le scraping doit être adapté à la structure HTML réelle")
    
    # Test 2: Get history for specific stocks
    print("\n" + "="*60)
    print("Test 2: Récupération de l'historique pour CSH, AKD, SGT")
    print("="*60)
    
    test_symbols = ['CSH', 'AKD', 'SGT', 'ATW']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    for symbol in test_symbols:
        print(f"\n📈 Test pour {symbol}:")
        history = await scraper.get_stock_history_real(symbol, start_date, end_date)
        
        if history:
            print(f"  ✅ {len(history)} points de données trouvés")
            print(f"  📅 Période: {history[0]['date']} à {history[-1]['date']}")
            print(f"  💰 Dernier prix: {history[-1]['close']} MAD")
            print(f"  📊 Exemple de données:")
            for i, price in enumerate(history[:3]):
                print(f"    {price['date'].strftime('%Y-%m-%d')}: {price['close']} MAD (Vol: {price['volume']:,})")
        else:
            print(f"  ⚠️  Aucune donnée trouvée pour {symbol}")
            print(f"     → Le parsing HTML doit être adapté à la structure réelle du site")
    
    print("\n" + "="*60)
    print("📝 NOTE IMPORTANTE:")
    print("="*60)
    print("""
Pour que le scraping fonctionne avec les VRAIES données:
1. Visitez https://www.casablanca-bourse.com dans votre navigateur
2. Inspectez le HTML (F12) pour voir la structure réelle
3. Adaptez les sélecteurs dans real_casablanca_bourse.py
4. Testez avec les vraies URLs et structures HTML

Les données actuelles sont simulées pour les tests.
Le scraper est prêt mais doit être adapté à la structure HTML réelle.
    """)
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_real_scraping())

