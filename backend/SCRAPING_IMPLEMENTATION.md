# 📊 Guide d'Implémentation du Scraping - Jour 2

## 🎯 Objectif Business

Le système de scraping permet de récupérer les données réelles du marché marocain pour :
- **Optimisation de portefeuille** : Données historiques pour calculer rendements et covariances
- **Analyse comparative** : Comparer performances OPCVM
- **Conformité réglementaire** : Utiliser les données officielles (Bourse, ASFIM, AMMC)

## 🏗️ Architecture

### 1. Scrapers (`app/utils/scrapers/`)
- **CasablancaBourseScraper** : Données boursières (cours, volumes, indices)
- **ASFIMScraper** : Données OPCVM (VL, performances)
- **AMMCScraper** : États financiers et statistiques marché

### 2. Cache (`app/database/models.py`)
- **StockPrice** : Historique des prix
- **StockInfo** : Métadonnées des actions
- **OPCVMData** : Données OPCVM
- **MarketIndex** : Indices de marché (MASI, MASI 20)

### 3. Service (`app/api/services/data_service.py`)
- Gestion du cache (TTL 24h)
- Validation des données
- Gestion d'erreurs robuste
- Fallback sur cache en cas d'erreur

## 🔧 Implémentation des Scrapers

### Étape 1 : Analyser la Structure HTML

Pour chaque site, il faut :
1. Visiter le site web
2. Inspecter le HTML (F12 dans le navigateur)
3. Identifier les sélecteurs CSS/XPath
4. Adapter le code de parsing

### Étape 2 : Casablanca Bourse

**URLs importantes :**
- Instruments : `https://www.casablanca-bourse.com/fr/instruments`
- Historique indices : `https://www.casablanca-bourse.com/fr/historique-des-indices`
- Données marché : `https://www.casablanca-bourse.com/fr/data/donnees-de-marche/volume`

**À implémenter dans `casablanca_bourse.py` :**
```python
# Dans get_available_stocks()
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', class_='instruments-table')  # À adapter
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    # Extraire symbol, name, sector, market_cap
```

### Étape 3 : ASFIM

**URL importante :**
- Performances : `https://www.asfim.ma/publications/tableaux-des-performances/`

**À implémenter :**
- Parser le tableau HTML des performances
- Ou télécharger le fichier Excel/CSV hebdomadaire
- Extraire NAV et performances (1y, 3y, 5y)

### Étape 4 : AMMC

**URLs importantes :**
- États financiers : `https://www.ammc.ma/fr/liste-etats-financiers-emetteurs`
- Statistiques : `https://www.ammc.ma/fr/donnees-statistiques`

## 🧪 Tests

```bash
cd backend
source venv/bin/activate
pytest tests/test_scrapers.py -v
pytest tests/test_data_service.py -v
```

## 📝 Notes Importantes

1. **Respect des robots.txt** : Vérifier les règles de scraping
2. **Rate limiting** : Ajouter des délais entre requêtes
3. **User-Agent** : Utiliser un User-Agent approprié
4. **Gestion d'erreurs** : Toujours gérer les cas d'erreur
5. **Cache** : Utiliser le cache pour éviter les requêtes répétées

## 🚀 Prochaines Étapes

Une fois les scrapers implémentés :
1. Tester avec des données réelles
2. Valider la qualité des données
3. Optimiser les performances
4. Ajouter monitoring et alertes

