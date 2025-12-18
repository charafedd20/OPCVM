# 🏗️ Architecture du Projet - Portfolio Optimizer Pro

## 📁 Structure du Projet

```
OPCVM/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/        # API endpoints
│   │   │   │   ├── health.py
│   │   │   │   ├── data.py
│   │   │   │   └── optimization.py
│   │   │   ├── models/        # Pydantic models
│   │   │   │   ├── data.py
│   │   │   │   └── optimization.py
│   │   │   └── services/      # Business logic
│   │   │       ├── data_service.py
│   │   │       └── optimization_service.py
│   │   ├── core/              # Core configuration
│   │   │   └── config.py
│   │   ├── utils/             # Utilities
│   │   │   ├── data_scraper.py
│   │   │   ├── optimizers.py
│   │   │   └── covariance_estimator.py
│   │   └── main.py           # FastAPI app
│   ├── tests/                 # Tests
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
│
├── frontend/                   # Frontend React + TypeScript
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom hooks
│   │   ├── utils/             # Utilities
│   │   ├── types/             # TypeScript types
│   │   ├── services/          # API services
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI
│
├── README.md
├── ARCHITECTURE.md
└── .gitignore
```

## 🔧 Technologies

### Backend
- **FastAPI**: Framework web moderne et rapide
- **NumPy/Pandas**: Traitement de données
- **CVXPY**: Optimisation convexe
- **Scikit-learn**: Machine learning (Ledoit-Wolf)
- **SQLAlchemy**: ORM pour base de données
- **Pydantic**: Validation de données

### Frontend
- **React 18**: Bibliothèque UI
- **TypeScript**: Typage statique
- **Vite**: Build tool rapide
- **Tailwind CSS**: Framework CSS
- **Recharts/Plotly**: Visualisations
- **React Router**: Navigation

## 🚀 Démarrage Rapide

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Health
- `GET /api/health` - Health check

### Data
- `GET /api/v1/stocks` - Liste des actions
- `GET /api/v1/stocks/{symbol}/history` - Historique d'une action
- `GET /api/v1/opcvm` - Liste des OPCVM
- `GET /api/v1/opcvm/{id}/performance` - Performance d'un OPCVM

### Optimization
- `POST /api/v1/optimize/mean-variance` - Optimisation Mean-Variance
- `POST /api/v1/optimize/cvar` - Optimisation CVaR
- `POST /api/v1/optimize/robust` - Optimisation Robuste
- `POST /api/v1/efficient-frontier` - Frontière efficiente
- `POST /api/v1/stress-test` - Stress testing

## 🔐 Configuration

Les variables d'environnement sont définies dans `backend/.env` (copier depuis `.env.example`).

## 📝 Notes d'Implémentation

- Les services contiennent la logique métier
- Les routes sont minces et délèguent aux services
- Les modèles Pydantic valident les données
- Les optimiseurs sont dans `utils/optimizers.py`
- L'estimation de covariance est dans `utils/covariance_estimator.py`

