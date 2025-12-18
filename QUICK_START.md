# 🚀 Démarrage Rapide

## ✅ Installation Complète

Toutes les dépendances sont installées et testées !

## 🎯 Démarrer l'Application

### Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
python run.py
```

Le serveur démarre sur **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Le frontend démarre sur **http://localhost:5173**

## 🧪 Tests

### Backend
```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Frontend
```bash
cd frontend
npm run build  # Test de build
```

## 📝 Notes

- Le fichier `.env` est déjà créé dans `backend/`
- Toutes les dépendances sont installées
- L'architecture est prête pour le développement

## 🎉 Prochaines Étapes

- Jour 2: Implémentation du scraping des données marocaines
- Jour 3: Estimation robuste de covariance
- Jour 4: Optimisation Mean-Variance

