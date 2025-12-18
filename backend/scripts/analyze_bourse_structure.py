"""
Script pour analyser la structure réelle du site Casablanca Bourse
Aide à identifier les vrais sélecteurs HTML
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def analyze_site_structure():
    """Analyse la structure HTML du site"""
    base_url = "https://www.casablanca-bourse.com"
    
    print("\n" + "🔍"*30)
    print("  ANALYSE DE LA STRUCTURE - Bourse de Casablanca")
    print("🔍"*30 + "\n")
    
    urls_to_test = [
        "/fr/instruments",
        "/fr",
        "/fr/cours",
        "/fr/data/donnees-de-marche",
    ]
    
    for path in urls_to_test:
        url = base_url + path
        print(f"\n{'='*60}")
        print(f"📄 Analyse de: {url}")
        print(f"{'='*60}")
        
        try:
            response = requests.get(url, verify=False, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                print(f"✅ Status: {response.status_code}")
                print(f"📏 Taille: {len(response.content)} bytes")
                print(f"📝 Titre: {soup.title.string if soup.title else 'N/A'}")
                
                # Analyser la structure
                print(f"\n📊 Structure HTML:")
                print(f"  - Tables: {len(soup.find_all('table'))}")
                print(f"  - Divs: {len(soup.find_all('div'))}")
                print(f"  - Liens: {len(soup.find_all('a'))}")
                print(f"  - Scripts: {len(soup.find_all('script'))}")
                
                # Chercher des patterns intéressants
                tables = soup.find_all('table')
                if tables:
                    print(f"\n  📋 Tables trouvées:")
                    for i, table in enumerate(tables[:3]):
                        print(f"    Table {i+1}:")
                        print(f"      Classes: {table.get('class', [])}")
                        rows = table.find_all('tr')
                        print(f"      Lignes: {len(rows)}")
                        if rows:
                            first_row = rows[0]
                            cells = first_row.find_all(['td', 'th'])
                            print(f"      Colonnes (première ligne): {len(cells)}")
                            if cells:
                                print(f"      Exemple de contenu: {[c.get_text(strip=True)[:30] for c in cells[:5]]}")
                
                # Chercher des liens vers des instruments
                links = soup.find_all('a', href=True)
                instrument_links = []
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    if any(symbol in href.upper() or symbol in text.upper() for symbol in ['ATW', 'CSH', 'AKD', 'SGT', 'IAM']):
                        instrument_links.append((href, text[:50]))
                
                if instrument_links:
                    print(f"\n  🔗 Liens intéressants trouvés:")
                    for href, text in instrument_links[:10]:
                        print(f"    {href[:60]:60s} - {text}")
                
                # Chercher des scripts JSON (peut contenir des données)
                scripts = soup.find_all('script')
                json_scripts = []
                for script in scripts:
                    content = script.string or ''
                    if 'symbol' in content.lower() or 'price' in content.lower() or 'instrument' in content.lower():
                        json_scripts.append(content[:200])
                
                if json_scripts:
                    print(f"\n  📜 Scripts avec données potentielles: {len(json_scripts)}")
                    for i, script_content in enumerate(json_scripts[:2]):
                        print(f"    Script {i+1}: {script_content[:150]}...")
                
            else:
                print(f"❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
    
    print("\n" + "="*60)
    print("📝 RECOMMANDATIONS:")
    print("="*60)
    print("""
1. Visitez manuellement le site dans votre navigateur
2. Utilisez F12 pour inspecter les éléments
3. Identifiez les sélecteurs CSS/XPath exacts
4. Adaptez le code dans real_casablanca_bourse.py

Alternative: Utilisez des données de test pour le développement
et mentionnez dans la présentation que le scraping réel nécessite
l'adaptation à la structure HTML spécifique du site.
    """)

if __name__ == "__main__":
    analyze_site_structure()

