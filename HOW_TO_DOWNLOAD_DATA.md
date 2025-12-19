# 📥 Guide Complet : Comment Télécharger les Données CSV

## 🎯 Objectif

Télécharger les données historiques de 10 sociétés depuis le site officiel de la Bourse de Casablanca.

## 📊 Les 10 Sociétés à Télécharger

| Symbole | Nom Complet | Secteur |
|---------|-------------|---------|
| **ATW** | Attijariwafa Bank | Banking |
| **BCP** | Banque Centrale Populaire | Banking |
| **BOA** | Bank of Africa | Banking |
| **IAM** | Maroc Telecom | Telecommunications |
| **TAQA** | TAQA Morocco | Energy |
| **LAA** | LafargeHolcim Maroc | Construction |
| **LABEL** | Label'Vie | Retail |
| **WAFA** | Wafa Assurance | Insurance |
| **TGCC** | TGCC | Construction |
| **MNG** | Managem | Mining |

## 🔍 Méthode 1 : Via la Page Instrument (Recommandé)

### Étape 1 : Accéder au Site
1. Allez sur : **https://www.casablanca-bourse.com/fr/instruments**
2. Utilisez la recherche pour trouver chaque société

### Étape 2 : Pour Chaque Société
1. **Cliquez sur le symbole** (ex: ATW, BCP, etc.)
2. **Cherchez l'onglet "Historique"** ou "Cours historiques"
3. **Sélectionnez la période** :
   - Minimum : **3 ans** (recommandé : 5 ans)
   - Date de début : 2020-01-01 (ou plus tôt)
   - Date de fin : Aujourd'hui
4. **Cherchez le bouton "Exporter"** ou "Télécharger" ou "Export CSV"
5. **Téléchargez le fichier CSV**

### Étape 3 : Nommer le Fichier
Renommez chaque fichier avec le symbole :
- `ATW.csv`
- `BCP.csv`
- `BOA.csv`
- etc.

## 🔍 Méthode 2 : Via la Section Données de Marché

1. Allez sur : **https://www.casablanca-bourse.com/fr/data/donnees-de-marche**
2. Sélectionnez :
   - **Type de données** : Cours historiques
   - **Instrument** : Sélectionnez chaque société une par une
   - **Période** : 3-5 ans
   - **Format** : CSV
3. Téléchargez et renommez les fichiers

## 🔍 Méthode 3 : Export Direct (Si Disponible)

Certaines pages d'instruments ont un bouton "Export" ou "Télécharger" directement visible.

## 📋 Format CSV Attendu

### Colonnes Minimum Requises :

| Colonne | Description | Obligatoire |
|---------|-------------|-------------|
| **Date** | Date de cotation (YYYY-MM-DD ou DD/MM/YYYY) | ✅ OUI |
| **Close** | Prix de clôture (en MAD) | ✅ OUI |

### Colonnes Recommandées :

| Colonne | Description | Obligatoire |
|---------|-------------|-------------|
| **Open** | Prix d'ouverture | ⚠️ Recommandé |
| **High** | Prix maximum | ⚠️ Recommandé |
| **Low** | Prix minimum | ⚠️ Recommandé |
| **Volume** | Volume échangé | ⚠️ Recommandé |

### Exemple de Format Accepté :

```csv
Date,Open,High,Low,Close,Volume
2022-01-01,100.50,102.30,99.80,101.20,1500000
2022-01-02,101.20,103.10,100.50,102.80,1800000
2022-01-03,102.80,104.20,101.90,103.50,1650000
```

**OU**

```csv
Date,Clôture,Ouverture,Maximum,Minimum,Volume
01/01/2022,101.20,100.50,102.30,99.80,1500000
02/01/2022,102.80,101.20,103.10,100.50,1800000
```

## ✅ Vérification Avant Import

Avant de placer les fichiers dans `backend/data/csv/`, vérifiez :

- ✅ Le fichier contient au moins **252 lignes** (1 an de données)
- ✅ La colonne **Date** est présente
- ✅ La colonne **Close** (ou Clôture) est présente
- ✅ Les prix sont en **MAD** (Dirhams marocains)
- ✅ Pas de valeurs manquantes dans la colonne Close
- ✅ Le format de date est cohérent

## 📁 Où Placer les Fichiers

Une fois téléchargés, placez tous les fichiers CSV dans :

```
backend/data/csv/
```

Structure finale :
```
backend/data/csv/
  ├── ATW.csv
  ├── BCP.csv
  ├── BOA.csv
  ├── IAM.csv
  ├── TAQA.csv
  ├── LAA.csv
  ├── LABEL.csv
  ├── WAFA.csv
  ├── TGCC.csv
  └── MNG.csv
```

## 🚀 Import des Données

Une fois tous les fichiers en place :

```bash
cd backend
source venv/bin/activate
python scripts/import_csv_data.py
```

Le script va :
- ✅ Détecter automatiquement les fichiers CSV
- ✅ Parser les différents formats de date
- ✅ Normaliser les noms de colonnes
- ✅ Importer dans la base de données
- ✅ Détecter et ignorer les doublons

## ⚠️ Si le Format Diffère

Si le CSV a un format différent :
1. Ouvrez le fichier dans Excel/LibreOffice
2. Vérifiez les noms de colonnes
3. Si nécessaire, renommez les colonnes pour correspondre :
   - Date → Date
   - Clôture / Dernier cours → Close
   - Ouverture → Open
   - Maximum / Haut → High
   - Minimum / Bas → Low
   - Volume → Volume

## 📞 Alternative : Contact Direct

Si vous avez des difficultés à télécharger :
- Contactez la Bourse de Casablanca pour demander les données historiques
- Ils peuvent fournir les fichiers CSV directement

## 🎯 Informations Nécessaires pour l'Optimisation

Pour une optimisation de portefeuille efficace, nous avons besoin de :

1. **Prix de clôture** (Close) - **ESSENTIEL**
   - Minimum : 252 jours (1 an)
   - Recommandé : 756-1260 jours (3-5 ans)

2. **Prix OHLC** (Open, High, Low, Close) - **Recommandé**
   - Pour calculer la volatilité intraday
   - Pour des estimations plus précises

3. **Volume** - **Optionnel mais utile**
   - Pour filtrer les jours avec faible liquidité
   - Pour pondérer les estimations

4. **Fréquence** - **Quotidienne recommandée**
   - Plus de données = meilleure estimation de covariance

## ✅ Checklist Finale

Avant de commencer l'import :

- [ ] 10 fichiers CSV téléchargés
- [ ] Fichiers nommés correctement (ATW.csv, BCP.csv, etc.)
- [ ] Chaque fichier contient au moins 252 lignes
- [ ] Colonnes Date et Close présentes
- [ ] Fichiers placés dans `backend/data/csv/`
- [ ] Prêt à exécuter `import_csv_data.py`

## 🆘 En Cas de Problème

Si vous ne trouvez pas comment télécharger :
1. Visitez le site et explorez les différentes sections
2. Cherchez "Export", "Télécharger", "Download", "CSV"
3. Contactez le support de la Bourse de Casablanca
4. Utilisez les données de test pour développer (nous pouvons les générer)

