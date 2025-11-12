# 🏥 Optimisation du Flux de Lits - SPH

Application **Streamlit** permettant de prévoir le **flux de sorties hospitalières** en utilisant les données COVID hospitalières de Santé Publique France.

---

## 🎯 Objectif du projet

Créer un modèle simple capable de prédire les **sorties de patients (`discharges`)** à J+1 et J+2, afin d’aider à **anticiper la gestion des lits hospitaliers**.

---

## 📊 Données utilisées

Les données proviennent du fichier **covid_hosp.csv** (Santé Publique France).

Elles sont transformées à l’aide du script :

src/from_spf_to_daily.py

yaml
Copier le code

Variables finales disponibles :

- **date** – date du jour  
- **admissions** – admissions estimées  
- **discharges** – sorties d’hôpital  
- **occupancy_rate** – taux d’occupation

---

## 🧠 Modèle de prévision

Le modèle utilisé est une **régression linéaire (scikit-learn)** basée sur :

| Feature | Rôle |
|--------|------|
| `lag1` | Sorties de la veille |
| `lag7` | Sorties à J-7 |
| `ma7` | Moyenne mobile sur 7 jours |
| `dow` | Jour de la semaine |

Un benchmark naïf (Naïf-1, Naïf-7) sert de comparaison.

---

## 🧩 Architecture du projet

optimisation-flux-lits-SPH/
│
├── app/
│ └── app.py # Application Streamlit
│
├── data/
│ ├── raw/ # Données brutes
│ └── pred/ # Prévisions générées
│
├── models/
│ └── baseline_linreg.pkl # Modèle sauvegardé
│
├── notebooks/
│ ├── 01_EDA.ipynb
│ ├── 02_forecast_baseline.ipynb
│ ├── 03_model_training.ipynb
│ └── 04_dashboard_tests.ipynb
│
├── src/
│ └── from_spf_to_daily.py # Transformation des données
│
└── reports/
└── eda/ # Graphiques d'analyse

yaml
Copier le code

---

## 💻 Installation locale

### 1. Cloner le dépôt

```bash
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
📈 Exemple de résultats
Copier le code
Prévision J+1 : 864 lits  
Prévision J+2 : 865 lits  
🛠️ Technologies utilisées
Python 3.12

Pandas

NumPy

Scikit-learn

Streamlit

Matplotlib

Joblib

👤 Auteur
Fayçal Hass
Projet HUG / Santé Publique Hospitalière
📧 faycalhass@gmail.com

📄 Licence
Ce projet est distribué sous licence MIT.
