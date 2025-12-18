"""
Script de test des endpoints API
Teste tous les endpoints et affiche les résultats
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_endpoint(method, endpoint, params=None, data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"\n📍 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success")
            if isinstance(result, list):
                print(f"   📊 Count: {len(result)}")
                if len(result) > 0:
                    print(f"   📝 Sample: {json.dumps(result[0], indent=2, default=str)}")
            elif isinstance(result, dict):
                print(f"   📝 Response: {json.dumps(result, indent=2, default=str)[:500]}...")
            return True, response.json()
        else:
            print(f"   ❌ Error: {response.text[:200]}")
            return False, None
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False, None

def main():
    """Test all endpoints"""
    print("\n" + "🚀"*30)
    print("  TEST DES ENDPOINTS - Portfolio Optimizer Pro")
    print("🚀"*30)
    
    # Health check
    print_section("Health Check")
    test_endpoint("GET", "/api/health")
    test_endpoint("GET", "/")
    
    # Stocks endpoints
    print_section("Stocks Endpoints")
    test_endpoint("GET", "/api/v1/stocks")
    test_endpoint("GET", "/api/v1/stocks", params={"use_cache": False})
    
    # Stock history
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    test_endpoint("GET", "/api/v1/stocks/ATW/history", params={
        "start_date": start_date,
        "end_date": end_date
    })
    
    # OPCVM endpoints
    print_section("OPCVM Endpoints")
    test_endpoint("GET", "/api/v1/opcvm")
    test_endpoint("GET", "/api/v1/opcvm", params={"use_cache": False})
    
    # OPCVM performance
    test_endpoint("GET", "/api/v1/opcvm/TEST_OPCVM/performance")
    
    print("\n" + "✅"*30)
    print("  TESTS TERMINÉS")
    print("✅"*30 + "\n")

if __name__ == "__main__":
    main()

