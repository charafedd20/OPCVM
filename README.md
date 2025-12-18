# 🎯 Portfolio Optimizer Pro - Challenge Wafa Gestion 2026

## 📋 Vue d'ensemble

Plateforme web avancée d'optimisation de portefeuille sous contraintes de risque et réglementaires OPCVM, utilisant des techniques mathématiques avancées (optimisation convexe, CVaR, robuste optimization, copules) et des données du marché marocain.

**Stack Technique:**
- **Frontend:** React + TypeScript + Tailwind CSS + Recharts/Plotly.js
- **Backend:** Python FastAPI + NumPy + Pandas + CVXPY
- **Mathématiques:** Optimisation convexe, Programmation Quadratique, CVaR, Robust Optimization, Copules
- **Déploiement:** Vercel (Frontend) + Railway/Render (Backend)
- **Base de données:** PostgreSQL (Supabase) ou SQLite

---

## 🧮 Fondements Mathématiques

### 1. Programmation Quadratique (QP) - Markowitz
```
Minimiser:  w^T Σ w                    (variance du portefeuille)
Sous contraintes:
  - w^T μ = r_target                   (rendement cible)
  - Σ w_i = 1                          (contrainte de budget)
  - w_i ≥ 0                            (pas de vente à découvert)
  - w_i ≤ w_max                        (poids max par actif)
  - Σ_{i ∈ secteur_j} w_i ≤ w_sector   (contrainte sectorielle)
```

### 2. Conditional Value at Risk (CVaR)
```
CVaR_α = E[R | R ≤ VaR_α]

Où VaR_α = quantile α de la distribution des rendements
```

### 3. Optimisation Robuste (Robust Optimization)
```
Minimiser:  max_{Σ ∈ U} w^T Σ w

Où U = ensemble d'incertitude sur la covariance (ellipsoïde)
```

### 4. Estimation Robuste de Covariance
- **Shrinkage de Ledoit-Wolf:** `Σ_shrink = α Σ_sample + (1-α) Σ_target`
- **Factor Models:** `Σ = B Σ_factors B^T + D`
- **Régularisation Ridge:** `Σ_ridge = Σ + λ I`

### 5. Copules pour Stress Testing
- Copules Gaussiennes et t-Student pour modéliser les dépendances
- Simulation de scénarios corrélés via Monte Carlo

---

## 📊 Sources de Données Marocaines

### 1. Bourse de Casablanca
- **Cours & Volume:** `casablanca-bourse.com/fr/instruments`
- **Indices historiques:** `casablanca-bourse.com/fr/historique-des-indices` (MASI, MASI 20, MASIR)
- **Capitalisation:** `casablanca-bourse.com/fr/capitalisation`
- **Volumes:** `casablanca-bourse.com/fr/data/donnees-de-marche/volume`

### 2. ASFIM (Association des Sociétés de Fonds d'Investissement)
- **VL & Performances OPCVM:** `asfim.ma/publications/tableaux-des-performances/`
- **Fichier hebdomadaire:** Tableaux des performances hebdomadaire

### 3. Bank Al Maghrib
- **Données macro:** `bkam.ma`

### 4. AMMC (Autorité Marocaine du Marché des Capitaux)
- **États financiers:** `ammc.ma/fr/liste-etats-financiers-emetteurs`
- **Statistiques marché:** `ammc.ma/fr/donnees-statistiques`

---

## 🗓️ PLAN DE DÉVELOPPEMENT DÉTAILLÉ (20 Jours)

### **SEMAINE 1: FOUNDATION & CORE OPTIMIZATION (Jours 1-7)**

#### **Jour 1: Setup Projet & Architecture** ⏱️ **6-8 heures**
- [ ] Initialiser repo Git avec structure modulaire
- [ ] Setup backend FastAPI avec structure (routes, models, services)
- [ ] Setup frontend React + TypeScript + Tailwind
- [ ] Configuration environnement (requirements.txt, package.json)
- [ ] Setup CI/CD basique (GitHub Actions)
- [ ] Documentation architecture dans README

**Livrables:** Structure projet complète, environnement configuré

---

#### **Jour 2: Scraping & Intégration Données Marocaines** ⏱️ **7-8 heures**
- [ ] Scraper Bourse de Casablanca (cours historiques, volumes)
- [ ] Scraper ASFIM (VL OPCVM, performances hebdomadaires)
- [ ] Parser données AMMC (états financiers si nécessaire)
- [ ] API endpoints pour récupérer données (GET /api/stocks, /api/opcvm)
- [ ] Cache Redis ou SQLite pour données historiques
- [ ] Tests unitaires scraping

**Livrables:** Module de données fonctionnel, API endpoints données

---

#### **Jour 3: Estimation Paramètres & Covariance Robuste** ⏱️ **6-7 heures**
- [ ] Calcul rendements historiques (log returns)
- [ ] Estimation covariance naïve
- [ ] **Implémentation Ledoit-Wolf Shrinkage** (math avancée)
- [ ] **Factor Model pour covariance** (PCA-based ou Fama-French simplifié)
- [ ] Estimation rendements espérés (moyenne historique ou CAPM)
- [ ] API endpoint: POST /api/estimate-parameters

**Livrables:** Module estimation robuste, API fonctionnelle

**Code mathématique à montrer:**
```python
def ledoit_wolf_shrinkage(returns):
    """
    Σ_shrink = α Σ_sample + (1-α) Σ_target
    Où α optimisé pour minimiser l'erreur quadratique
    """
```

---

#### **Jour 4: Optimisation Mean-Variance (QP Classique)** ⏱️ **7-8 heures**
- [ ] **Implémentation QP avec CVXPY** (formulation math complète)
- [ ] Résolution frontière efficiente (50-100 points)
- [ ] Contraintes de base: budget, long-only, poids max
- [ ] API endpoint: POST /api/optimize/mean-variance
- [ ] Tests avec données réelles marocaines
- [ ] Validation résultats (vérifier contraintes)

**Livrables:** Optimiseur Mean-Variance fonctionnel

**Code mathématique à montrer:**
```python
def solve_mean_variance_qp(mu, Sigma, target_return, constraints):
    """
    Résout: min w^T Σ w
    s.t. w^T μ = r_target, Σw = 1, w ≥ 0, w ≤ w_max
    """
```

---

#### **Jour 5: Frontend - UI Base & Visualisations** ⏱️ **6-7 heures**
- [ ] Composants React: sélection actifs, paramètres optimisation
- [ ] Graphique frontière efficiente (Recharts/Plotly)
- [ ] Tableau allocation optimale (camembert + tableau)
- [ ] Intégration API backend
- [ ] UI moderne avec Tailwind (design system)

**Livrables:** Interface utilisateur fonctionnelle, visualisations de base

---

#### **Jour 6: Contraintes OPCVM Réalistes** ⏱️ **6-7 heures**
- [ ] Contrainte diversification: HHI ≤ HHI_max
- [ ] Contraintes sectorielles (si données disponibles)
- [ ] Contrainte liquidité (filtre actifs éligibles)
- [ ] Validation automatique conformité OPCVM
- [ ] API endpoint avec toutes contraintes
- [ ] Tests contraintes combinées

**Livrables:** Module contraintes OPCVM complet

**Mathématique:**
```python
def calculate_hhi(weights):
    """HHI = Σ w_i², Diversification effective = 1/HHI"""
    return np.sum(weights ** 2)
```

---

#### **Jour 7: MVP Fonctionnel & Tests** ⏱️ **5-6 heures**
- [ ] Intégration complète frontend-backend
- [ ] Tests end-to-end (scénario complet)
- [ ] Correction bugs majeurs
- [ ] Documentation API (Swagger/OpenAPI)
- [ ] Démo MVP fonctionnel

**Livrables:** MVP complet et fonctionnel

---

### **SEMAINE 2: FEATURES AVANCÉES & RISK MANAGEMENT (Jours 8-14)**

#### **Jour 8: CVaR Optimization (Math Avancée)** ⏱️ **8-9 heures**
- [ ] **Implémentation CVaR avec formulation linéaire** (variables auxiliaires)
- [ ] Calcul VaR (Value at Risk) pour différents α (0.01, 0.05, 0.10)
- [ ] Optimisation sous contrainte CVaR: `CVaR_α(w) ≤ CVaR_max`
- [ ] Frontière efficiente CVaR (comparaison avec variance)
- [ ] API endpoint: POST /api/optimize/cvar
- [ ] Tests validation CVaR

**Livrables:** Optimiseur CVaR fonctionnel

**Code mathématique critique:**
```python
def optimize_cvar_portfolio(returns, alpha=0.05, cvar_max=0.02):
    """
    Formulation avec variables auxiliaires:
    min w^T μ
    s.t. CVaR_α(w) ≤ cvar_max
    """
    # Utiliser formulation linéaire avec quantile
```

---

#### **Jour 9: Optimisation Robuste (Très Avancé)** ⏱️ **8-9 heures**
- [ ] **Implémentation Robust Optimization** (min-max sur ensemble incertitude)
- [ ] Ellipsoïde d'incertitude pour covariance: `U = {Σ: ||Σ - Σ_0|| ≤ ρ}`
- [ ] Résolution problème robuste (SDP ou approximation)
- [ ] Comparaison robuste vs classique (sensibilité paramètres)
- [ ] API endpoint: POST /api/optimize/robust
- [ ] Visualisation impact incertitude

**Livrables:** Optimiseur robuste fonctionnel (différenciateur majeur)

**Code mathématique avancé:**
```python
def robust_portfolio_optimization(mu, Sigma_0, uncertainty_radius):
    """
    min_w max_{Σ ∈ U} w^T Σ w
    Où U = {Σ: ||Σ - Σ_0||_F ≤ ρ}
    """
    # Formulation SDP ou approximation conservative
```

---

#### **Jour 10: Stress Testing & Monte Carlo** ⏱️ **7-8 heures**
- [ ] Scénarios de stress prédéfinis (crise 2008, COVID, inflation)
- [ ] **Implémentation Monte Carlo** (1000+ simulations)
- [ ] Distribution rendements sous stress
- [ ] Heatmap performance par scénario
- [ ] API endpoint: POST /api/stress-test
- [ ] Visualisations stress tests

**Livrables:** Module stress testing complet

---

#### **Jour 11: Copules pour Dépendances (Math Avancée)** ⏱️ **8-9 heures**
- [ ] **Implémentation Copules Gaussiennes et t-Student**
- [ ] Estimation paramètres copule (corrélation, degrés liberté)
- [ ] Simulation scénarios corrélés via copules
- [ ] Comparaison copule vs corrélation linéaire
- [ ] Intégration dans stress tests
- [ ] API endpoint: POST /api/simulate-copula

**Livrables:** Module copules fonctionnel (différenciateur)

**Code mathématique:**
```python
def gaussian_copula_simulation(correlation_matrix, n_simulations):
    """
    Simule via copule gaussienne:
    1. Générer U ~ Uniform[0,1] corrélés
    2. Transformer via quantiles marginaux
    """
```

---

#### **Jour 12: Backtesting & Métriques Avancées** ⏱️ **7-8 heures**
- [ ] Backtesting historique (1 an, 3 ans, 5 ans)
- [ ] Calcul métriques: Sharpe, Sortino, Calmar, Information Ratio
- [ ] **Tests statistiques:** significativité Sharpe (t-test), bootstrap VaR
- [ ] Rolling window analysis (stabilité allocation)
- [ ] Comparaison avec benchmark (MASI, MASI 20)
- [ ] API endpoint: POST /api/backtest
- [ ] Graphiques performance cumulée

**Livrables:** Module backtesting complet avec tests statistiques

**Mathématique:**
```python
def test_sharpe_significance(portfolio_returns, benchmark_returns):
    """
    Test t: H0: SR_portfolio = SR_benchmark
    t-stat = (SR_p - SR_b) / SE(SR_p - SR_b)
    """
```

---

#### **Jour 13: Analyse Factorielle & Attribution** ⏱️ **6-7 heures**
- [ ] **Décomposition Fama-French simplifiée** (3 facteurs: Market, Size, Value)
- [ ] Attribution performance par facteur
- [ ] Exposition aux risques (beta, sectoriel)
- [ ] Diversification effective (nombre actifs équivalents)
- [ ] API endpoint: POST /api/factor-analysis
- [ ] Visualisations attribution

**Livrables:** Module analyse factorielle

---

#### **Jour 14: Tests & Optimisation Performance** ⏱️ **5-6 heures**
- [ ] Tests unitaires complets (coverage > 80%)
- [ ] Tests d'intégration
- [ ] Optimisation performance (cache, parallélisation)
- [ ] Correction bugs
- [ ] Documentation code (docstrings mathématiques)

**Livrables:** Code testé et optimisé

---

### **SEMAINE 3: INNOVATION IA & DÉPLOIEMENT (Jours 15-20)**

#### **Jour 15: Clustering Actifs & Recommandations IA** ⏱️ **7-8 heures**
- [ ] **Clustering K-means** sur rendements/corrélations
- [ ] Détection groupes d'actifs similaires
- [ ] Recommandations allocation basées sur clustering
- [ ] **Détection régimes marché simple** (HMM basique ou clustering temporel)
- [ ] API endpoint: POST /api/cluster-assets
- [ ] Visualisations clustering

**Livrables:** Features IA fonctionnelles

---

#### **Jour 16: Génération Rapports Automatiques** ⏱️ **6-7 heures**
- [ ] Template rapport PDF (allocation, risques, performance)
- [ ] Génération automatique avec données calculées
- [ ] Export Excel (allocation, métriques)
- [ ] Dashboard exécutif (KPIs résumés)
- [ ] API endpoint: POST /api/generate-report

**Livrables:** Module reporting complet

---

#### **Jour 17: UX Avancée & Visualisations Interactives** ⏱️ **6-7 heures**
- [ ] Graphiques 3D (frontière efficiente, surface risque)
- [ ] Animations transitions
- [ ] Mode sombre
- [ ] Responsive design (mobile)
- [ ] Tooltips explicatifs (aide contextuelle)
- [ ] Amélioration UI/UX globale

**Livrables:** Interface utilisateur professionnelle

---

#### **Jour 18: Déploiement Production** ⏱️ **6-7 heures**
- [ ] Déploiement frontend (Vercel/Netlify)
- [ ] Déploiement backend (Railway/Render)
- [ ] Configuration base de données (Supabase/PostgreSQL)
- [ ] Variables d'environnement sécurisées
- [ ] Tests déploiement (end-to-end)
- [ ] Monitoring basique (logs, erreurs)

**Livrables:** Application déployée et accessible

---

#### **Jour 19: Documentation & Préparation Présentation** ⏱️ **7-8 heures**
- [ ] README complet (architecture, math, usage)
- [ ] Documentation API (Swagger)
- [ ] Guide utilisateur
- [ ] **Préparation PPT** (10-15 slides)
  - Slide mathématiques avancées
  - Screenshots plateforme
  - Cas d'usage concret
  - Impact métier
- [ ] Vidéo démo (2-3 minutes)

**Livrables:** Documentation complète, PPT prêt

---

#### **Jour 20: Finalisation & Polish** ⏱️ **5-6 heures**
- [ ] Correction bugs mineurs
- [ ] Amélioration performance
- [ ] Tests finaux complets
- [ ] Vérification tous les features
- [ ] Préparation soumission (dossier Google Drive)
- [ ] Relecture documentation

**Livrables:** Projet finalisé, prêt pour soumission

---

## 🎯 FEATURES PRIORITAIRES (Checklist)

### ✅ Core Features (MVP)
- [x] Optimisation Mean-Variance (QP)
- [x] Frontière efficiente interactive
- [x] Contraintes OPCVM (diversification, sectorielles)
- [x] Interface utilisateur moderne
- [x] Intégration données marocaines

### ✅ Features Avancées (Différenciateurs)
- [x] CVaR Optimization
- [x] Optimisation Robuste (min-max)
- [x] Estimation covariance robuste (Ledoit-Wolf)
- [x] Copules pour stress testing
- [x] Tests statistiques rigoureux
- [x] Backtesting avec métriques avancées

### ✅ Innovation IA
- [x] Clustering actifs
- [x] Détection régimes marché
- [x] Recommandations intelligentes

### ✅ Production-Ready
- [x] Déploiement cloud
- [x] Documentation complète
- [x] Tests unitaires
- [x] Performance optimisée

---

## 📈 MÉTRIQUES DE SUCCÈS

### Technique
- ✅ Tous les algorithmes d'optimisation fonctionnels
- ✅ Performance: calcul allocation < 2 secondes
- ✅ Coverage tests > 80%
- ✅ Application déployée et accessible 24/7

### Mathématique
- ✅ Code commenté avec formules mathématiques
- ✅ Documentation théorie (README)
- ✅ Comparaisons algorithmes (variance vs CVaR vs robuste)

### Métier
- ✅ Contraintes OPCVM réalistes
- ✅ Cas d'usage concret (exemple portefeuille marocain)
- ✅ Impact mesurable (gain temps, réduction risques)

---

## 🚀 COMMANDES UTILES

### Backend
```bash
# Installation
pip install -r requirements.txt

# Lancer serveur
uvicorn main:app --reload

# Tests
pytest tests/
```

### Frontend
```bash
# Installation
npm install

# Lancer dev
npm run dev

# Build production
npm run build
```

---

## 📚 RÉFÉRENCES MATHÉMATIQUES

1. **Markowitz, H. (1952).** Portfolio Selection. Journal of Finance.
2. **Rockafellar, R.T. & Uryasev, S. (2002).** Conditional value-at-risk for general loss distributions. Journal of Banking & Finance.
3. **Ledoit, O. & Wolf, M. (2004).** A well-conditioned estimator for large-dimensional covariance matrices. Journal of Multivariate Analysis.
4. **Ben-Tal, A. & Nemirovski, A. (1998).** Robust convex optimization. Mathematics of Operations Research.

---

## 👤 Auteur

Développé pour le **Data & AI Internship Challenge 2026 - Wafa Gestion**

---

## 📄 Licence

Projet académique - Challenge Wafa Gestion 2026

