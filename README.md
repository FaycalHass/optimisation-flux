
# 🏥 Optimisation du Flux de Lits – SPH  
Application Streamlit permettant la **prévision du flux de sorties hospitalières** à partir des données COVID hospitalières (Santé Publique France).

---

## 🎯 Objectif du projet  
L’objectif est d’estimer les **sorties d’hôpital (discharges)** et de générer des prévisions à **J+1 et J+2** afin de soutenir :  
- la gestion des lits  
- l’anticipation des flux  
- la planification hospitalière  

---

## 📊 Données utilisées  
Les données proviennent de **Santé Publique France** via le fichier `covid_hosp.csv`, puis sont transformées avec :

```

src/from_spf_to_daily.py

```

Variables produites :  
- `date` — Date  
- `admissions` — Admissions estimées  
- `discharges` — Sorties estimées  
- `occupancy_rate` — Taux d’occupation  

---

## 🤖 Modèle de prévision  
Modèle principal : **Régression Linéaire (scikit-learn)**  

| Feature | Description |
|--------|-------------|
| `lag1` | Sorties J-1 |
| `lag7` | Sorties J-7 |
| `ma7`  | Moyenne mobile 7 jours |
| `dow`  | Jour de la semaine |

Benchmarks :  
- **Naïf-1** → valeur de la veille  
- **Naïf-7** → valeur de J-7  

---

## 🗂️ Architecture du projet

```text
optimisation-flux-lits-SPH/
│
├── app/
│   └── app.py                     # Application Streamlit
│
├── data/
│   ├── raw/                       # Données brutes
│   └── pred/                      # Prédictions générées
│
├── models/
│   └── baseline_linreg.pkl        # Modèle sauvegardé
│
├── notebooks/
│   ├── 01_EDA.ipynb               # Analyse exploratoire
│   ├── 02_forecast_baseline.ipynb # Modèle baseline
│   ├── 03_model_training.ipynb    # Entraînement modèle
│   └── 04_dashboard_tests.ipynb   # Tests Streamlit
│
├── src/
│   └── from_spf_to_daily.py       # Transformation quotidienne
│
└── reports/
    └── eda/                       # Graphiques EDA


---

## 💻 Installation locale

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/FaycalHass/optimisation-flux-lits-SPH.git
cd optimisation-flux-lits-SPH
````

---

### 2️⃣ Créer l’environnement

```bash
conda create -n hug_sph python=3.12 -y
conda activate hug_sph
pip install -r requirements.txt
```

---

### 3️⃣ Lancer l’application Streamlit

```bash
cd app
streamlit run app.py
```

---

## 📈 Exemple de prévisions

```text
Prévision J+1 : 864 lits
Prévision J+2 : 865 lits
```

---

## 🛠️ Technologies utilisées

* Python 3.12
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Matplotlib
* Joblib

---

## 👤 Auteur

**Fayçal Hass**
Projet HUG – Santé Publique Hospitalière
📧 [faycal.hassani.etu@univ-lille.fr](mailto:faycal.hassani.etu@univ-lille.fr)

---

## 🪪 Licence

Projet distribué sous licence **MIT**.
