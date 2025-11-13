# 🏥 Optimisation du Flux de Lits – SPH

Application **Streamlit** permettant la **prévision du flux de lits hospitaliers (sorties)** à partir des données hospitalières COVID de **Santé Publique France**.

---

## 🎯 Objectif du projet

Ce projet vise à développer un modèle prédictif simple et robuste permettant :

- d’estimer le **nombre de sorties hospitalières**,
- de prévoir les flux en **J+1** et **J+2**,
- d’**aider à la gestion opérationnelle des lits** dans les hôpitaux.

---

## 📊 Données utilisées

Les données proviennent du fichier public **covid_hosp.csv** disponible sur Santé Publique France.  
Elles sont nettoyées et transformées via le script :

src/from_spf_to_daily.py

yaml
Copier le code

Variables finales principales :

- `date` — Date du jour
- `admissions` — Admissions estimées
- `discharges` — Sorties hospitalières
- `occupancy_rate` — Taux d’occupation (capacité estimée à 100 000 lits)

---

## 🤖 Modèle utilisé

Modèle : **Régression linéaire Scikit-learn**

### Features :

| Feature | Description |
|--------|-------------|
| `lag1` | Sorties la veille |
| `lag7` | Sorties à J-7 |
| `ma7`  | Moyenne mobile 7 jours |
| `dow`  | Jour de la semaine |

**Benchmarks de comparaison :**

- *Naïf-1* : prédiction = valeur de la veille  
- *Naïf-7* : prédiction = valeur de J-7  

---

## 🧩 Architecture du projet

```text
optimisation-flux-lits-SPH/
│
├── app/
│   └── app.py                 # Application Streamlit
│
├── data/
│   ├── raw/                   # Données brutes
│   └── pred/                  # Prédictions générées
│
├── models/
│   └── baseline_linreg.pkl    # Modèle sauvegardé
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_forecast_baseline.ipynb
│   ├── 03_evaluation_and_dashboard.ipynb
│   └── 04_dashboard_tests.ipynb
│
├── src/
│   └── from_spf_to_daily.py   # Transformation des données
│
└── reports/
    └── eda/                   # Graphiques d’analyse

---

💻 Installation locale
1. Cloner le dépôt
bash
Copier le code
git clone https://github.com/FaycalHass/optimisation-flux-lits-SPH.git
cd optimisation-flux-lits-SPH
2. Créer l’environnement
bash
Copier le code
conda create -n hug_sph python=3.12 -y
conda activate hug_sph
pip install -r requirements.txt
3. Lancer l'application Streamlit
bash
Copier le code
cd app
streamlit run app.py
📈 Exemple de prévisions
Copier le code
Prévision J+1 : 864 lits
Prévision J+2 : 865 lits
🛠️ Technologies utilisées
Python 3.12

Pandas

NumPy

Scikit-learn

Matplotlib

Streamlit

Joblib

👨‍💻 Auteur
Faycal Hass
Projet HUG – Santé Publique Hospitalière
📧 faycalhass@gmail.com

🪪 Licence
Ce projet est distribué sous licence MIT.
Vous êtes libre de l’utiliser, le modifier et le redistribuer.
