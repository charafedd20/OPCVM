"""
Test analytics endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_analytics():
    """Test all analytics endpoints"""
    print("\n" + "📊"*30)
    print("  TEST DES ENDPOINTS ANALYTICS")
    print("📊"*30)
    
    endpoints = [
        ("GET", "/api/v1/analytics/stocks/summary", "Résumé des actions"),
        ("GET", "/api/v1/analytics/stocks/ATW/statistics", "Statistiques ATW"),
        ("GET", "/api/v1/analytics/stocks/ATW/chart-data?chart_type=line", "Données graphique ATW (line)"),
        ("GET", "/api/v1/analytics/stocks/ATW/chart-data?chart_type=candlestick", "Données graphique ATW (candlestick)"),
        ("GET", "/api/v1/analytics/opcvm/summary", "Résumé OPCVM"),
        ("GET", "/api/v1/analytics/market/overview", "Vue d'ensemble marché"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"\n{'='*60}")
        print(f"  {description}")
        print(f"{'='*60}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success")
                print(f"📝 Response (preview):")
                print(json.dumps(data, indent=2, default=str)[:1000])
            else:
                print(f"❌ Error: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "✅"*30)
    print("  TESTS ANALYTICS TERMINÉS")
    print("✅"*30 + "\n")

if __name__ == "__main__":
    test_analytics()

