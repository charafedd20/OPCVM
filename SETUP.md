# 🚀 Guide de Démarrage - Portfolio Optimizer Pro

## ⚙️ Configuration Initiale

### 1. Backend Setup

```bash
cd backend

# Créer environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp env.example.txt .env

# Lancer le serveur
python run.py
```

Le serveur backend sera accessible sur `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173`

## 📝 Notes Importantes

1. **Fichier .env**: Créez un fichier `.env` dans le dossier `backend/` en copiant `env.example.txt`
2. **Python Version**: Python 3.10+ requis
3. **Node Version**: Node.js 18+ requis

## 🔧 Prochaines Étapes

- Jour 2: Implémentation du scraping des données marocaines
- Jour 3: Estimation robuste de covariance
- Jour 4: Optimisation Mean-Variance

