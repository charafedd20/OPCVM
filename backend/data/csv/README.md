# 📁 Dossier CSV - Données Historiques

## 📥 Instructions

1. **Téléchargez les fichiers CSV** depuis la Bourse de Casablanca pour chaque société
2. **Placez-les ici** avec les noms suivants :

### Fichiers Requis :

- `ATW.csv` - Attijariwafa Bank
- `BCP.csv` - Banque Centrale Populaire
- `BOA.csv` - Bank of Africa
- `IAM.csv` - Maroc Telecom
- `TAQA.csv` - TAQA Morocco
- `LAA.csv` - LafargeHolcim Maroc
- `LABEL.csv` - Label'Vie
- `WAFA.csv` - Wafa Assurance
- `TGCC.csv` - TGCC
- `MNG.csv` - Managem

## 📋 Format CSV Attendu

Le CSV doit contenir au minimum :
- **Date** (format: YYYY-MM-DD ou DD/MM/YYYY)
- **Close** (Prix de clôture) ⭐ **OBLIGATOIRE**

Optionnel mais recommandé :
- **Open** (Prix d'ouverture)
- **High** (Prix maximum)
- **Low** (Prix minimum)
- **Volume** (Volume échangé)

### Exemple :

```csv
Date,Open,High,Low,Close,Volume
2022-01-01,100.50,102.30,99.80,101.20,1500000
2022-01-02,101.20,103.10,100.50,102.80,1800000
...
```

## 🚀 Import

Une fois les fichiers placés ici, exécutez :

```bash
cd backend
source venv/bin/activate
python scripts/import_csv_data.py
```

