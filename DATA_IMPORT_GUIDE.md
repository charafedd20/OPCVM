# 📥 Guide d'Import des Données CSV - Bourse de Casablanca

## 🎯 Objectif

Importer manuellement les données historiques de 10 sociétés depuis la Bourse de Casablanca pour l'optimisation de portefeuille.

## 📊 Les 10 Sociétés

1. **Attijariwafa Bank** (ATW) - Banking
2. **Banque Centrale Populaire** (BCP) - Banking
3. **Bank of Africa** (BOA) - Banking
4. **Maroc Telecom** (IAM) - Telecommunications
5. **TAQA Morocco** - Energy
6. **LafargeHolcim Maroc** (LAA) - Construction
7. **Label'Vie** - Retail
8. **Wafa Assurance** - Insurance
9. **TGCC** - Construction
10. **Managem** - Mining

## 📥 Comment Télécharger les Fichiers CSV

### Méthode 1 : Site Web de la Bourse de Casablanca

1. **Aller sur le site :**
   ```
   https://www.casablanca-bourse.com/fr/instruments
   ```

2. **Pour chaque société :**
   - Cliquer sur le symbole de l'action (ex: ATW, BCP, etc.)
   - Chercher l'option "Télécharger" ou "Export" ou "Historique"
   - Sélectionner la période (minimum 3 ans recommandé)
   - Télécharger au format CSV

3. **Structure attendue du CSV :**
   ```
   Date,Open,High,Low,Close,Volume
   2022-01-01,100.50,102.30,99.80,101.20,1500000
   ...
   ```

### Méthode 2 : Section Données de Marché

1. **Aller sur :**
   ```
   https://www.casablanca-bourse.com/fr/data/donnees-de-marche
   ```

2. **Sélectionner :**
   - Type : Cours historiques
   - Instrument : Sélectionner chaque société
   - Période : 3-5 ans
   - Format : CSV

### Méthode 3 : API ou Export Direct

Si disponible, utiliser l'export direct depuis la page de chaque instrument.

## 📋 Informations Nécessaires

### Minimum Requis pour l'Optimisation :

1. **Données de Prix (OHLCV) :**
   - Date (format: YYYY-MM-DD)
   - Open (Prix d'ouverture)
   - High (Prix maximum)
   - Low (Prix minimum)
   - Close (Prix de clôture) ⭐ **ESSENTIEL**
   - Volume (Volume échangé)

2. **Période :**
   - Minimum : 1 an (252 jours de trading)
   - Recommandé : 3-5 ans (756-1260 jours de trading)
   - Plus de données = meilleure estimation de covariance

3. **Fréquence :**
   - Quotidienne (recommandé)
   - Hebdomadaire (acceptable mais moins précis)

### Informations Supplémentaires (Optionnelles) :

- Secteur d'activité
- Capitalisation boursière
- Dividendes (si disponible)

## 📁 Structure des Fichiers

Placez les fichiers CSV dans :
```
backend/data/csv/
```

Nommage recommandé :
```
ATW.csv  (Attijariwafa Bank)
BCP.csv  (Banque Centrale Populaire)
BOA.csv  (Bank of Africa)
IAM.csv  (Maroc Telecom)
TAQA.csv (TAQA Morocco)
LAA.csv  (LafargeHolcim Maroc)
LABEL.csv (Label'Vie)
WAFA.csv (Wafa Assurance)
TGCC.csv (TGCC)
MNG.csv  (Managem)
```

## ✅ Vérification des Données

Avant d'importer, vérifiez que chaque CSV contient :
- ✅ Au moins 252 lignes (1 an de données)
- ✅ Colonnes : Date, Open, High, Low, Close, Volume
- ✅ Format de date cohérent
- ✅ Pas de valeurs manquantes dans Close
- ✅ Prix en MAD (Dirhams marocains)

## 🔧 Prochaines Étapes

Une fois les fichiers téléchargés :
1. Placer les CSV dans `backend/data/csv/`
2. Exécuter le script d'import : `python scripts/import_csv_data.py`
3. Vérifier les données importées via l'API

## 📝 Notes Importantes

- **Légalité** : L'import manuel de données publiques est légal
- **Période** : Plus de données = meilleure optimisation
- **Qualité** : Vérifiez les données avant import
- **Format** : Si le format diffère, adaptez le script d'import

