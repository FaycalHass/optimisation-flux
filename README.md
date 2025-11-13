# 🏥 Optimisation du Flux de Lits – SPH

Application **Streamlit** permettant la **prévision des sorties hospitalières (discharges)** à partir des données COVID hospitalières de Santé Publique France.

---

## 🚀 Objectif du projet

L’objectif est de développer un modèle capable d’estimer les **sorties de patients** et de fournir des prévisions J+1 et J+2 pour **optimiser la gestion des lits hospitaliers**.

---

## 📊 Données utilisées

Les données proviennent du fichier SPF **covid_hosp.csv**, transformé en série temporelle quotidienne via :

src/from_spf_to_daily.py

yaml
Copier le code

Variables finales utilisées :
- `date` — Date du jour  
- `admissions` — Admissions estimées  
- `discharges` — Sorties  
- `occupancy_rate` — Taux d’occupation estimé

---

## 🧠 Modèle de prévision

Modèle utilisé : **Régression linéaire (scikit-learn)**  
Features :

| Feature | Description |
|--------|-------------|
| `lag1` | Sorties la veille |
| `lag7` | Sorties il y a 7 jours |
| `ma7`  | Moyenne mobile 7 jours |
| `dow`  | Jour de la semaine |

Benchmarks utilisés :
- **Naïf-1** : prédiction = valeur de la veille  
- **Naïf-7** : prédiction = valeur de J-7  

## 🧩 Architecture du projet

optimisation-flux-lits-SPH/
│
├── app/
│ └── app.py # Application Streamlit
│
├── data/
│ ├── raw/ # Données brutes
│ └── pred/ # Prédictions générées
│
├── models/
│ └── baseline_linreg.pkl # Modèle sauvegardé
│
├── notebooks/
│ ├── 01_EDA.ipynb
│ ├── 02_forecast_baseline.ipynb
│ ├── 03_evaluation_and_dashboard.ipynb
│ └── 04_dashboard_tests.ipynb
│
├── src/
│ └── from_spf_to_daily.py # Transformation des données
│
└── reports/
└── eda/ # Graphiques d'analyse


## 💻 Installation locale

```bash
git clone https://github.com/FaycalHass/optimisation-flux-lits-SPH.git
cd optimisation-flux-lits-SPH
2. Créer l’environnement
bash
Copier le code
conda create -n hug_sph python=3.12 -y
conda activate hug_sph
pip install -r requirements.txt
3. Lancer l’application Streamlit
bash
Copier le code
cd app
streamlit run app.py
📈 Exemple de prévisions
scss
Copier le code
Prévision J+1 (2023-04-01) : 864,182 lits  
Prévision J+2 (2023-04-02) : 864,521 lits
📚 Technologies utilisées
Python 3.12

Pandas

NumPy

Scikit-learn

Matplotlib

Streamlit

Joblib

👨‍💻 Auteur
Fayçal Hass
Projet HUG / Santé Publique Hospitalière
📧 faycalhass@gmail.com

🪪 Licence
Projet distribué sous licence MIT.
