# ✅ 1. **README.md (complet et professionnel)**

👉 **Copie-colle entièrement ce bloc dans ton README.md :**

```markdown
# 🏥 Optimisation du Flux de Lits - SPH

Application **Streamlit** permettant la **prévision du flux de lits hospitaliers (sorties)** à partir des données COVID hospitalières de Santé Publique France.

---

## 🚀 Objectif du projet

L’objectif est de développer un modèle simple capable d’estimer les **sorties de patients** (variable `discharges`) et de fournir des prévisions à court terme (J+1, J+2).  
Ces prédictions visent à **optimiser la gestion des lits hospitaliers** en anticipant les variations d’occupation.

---

## 📊 Données utilisées

Les données proviennent du jeu **covid_hosp.csv** de Santé Publique France.  
Elles ont été nettoyées et transformées via le script :

```

src/from_spf_to_daily.py

```

Les principales variables finales :
- `date` — Date du jour  
- `admissions` — Nombre estimé d’admissions hospitalières  
- `discharges` — Nombre de sorties d’hôpital  
- `occupancy_rate` — Taux d’occupation (capacité estimée à 100 000 lits)

---

## 🧠 Modèle de prévision

Le modèle de base est une **régression linéaire** construite avec `scikit-learn`, utilisant les features suivantes :

| Feature | Description |
|----------|--------------|
| `lag1`   | Sorties la veille |
| `lag7`   | Sorties à J-7 |
| `ma7`    | Moyenne mobile sur 7 jours |
| `dow`    | Jour de la semaine |

Deux benchmarks naïfs (`Naïf-1`, `Naïf-7`) sont utilisés pour comparaison.

---

## 🧩 Architecture du projet

```

HUG_Project/
│
├── app/                     # Application Streamlit
│   └── app.py
│
├── data/
│   ├── raw/                 # Données brutes (covid_hosp.csv)
│   └── pred/                # Prédictions générées
│
├── models/                  # Modèle enregistré (.pkl)
│
├── notebooks/               # Analyse exploratoire et modèles
│   ├── 01_EDA.ipynb
│   ├── 02_forecast_baseline.ipynb
│   ├── 03_evaluation_and_dashboard.ipynb
│   └── 04_evaluation_and_dashboard.ipynb
│
├── src/                     # Scripts Python de transformation
│   └── from_spf_to_daily.py
│
└── reports/eda/             # Graphiques d’analyse

````

---

## 💻 Installation locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/FaycalHass/optimisation-flux-lits-SPH.git
cd optimisation-flux-lits-SPH
````

### 2. Créer l’environnement

```bash
conda create -n hug_sph python=3.12 -y
conda activate hug_sph
pip install -r requirements.txt
```

### 3. Lancer l’application Streamlit

```bash
cd app
streamlit run app.py
```

---

## 📈 Exemple de prévisions

```
Prévision J+1 (2023-04-01) : 864,182 lits  
Prévision J+2 (2023-04-02) : 864,521 lits  
```

---

## 📚 Technologies utilisées

* Python 3.12
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Streamlit

---

## 👨‍💻 Auteur

**Fayçal Hass**
Projet HUG / Santé Publique Hospitalière
📧 [faycalhass@gmail.com](mailto:faycalhass@gmail.com)

---

## 🪪 Licence

Ce projet est distribué sous licence **MIT**.
Vous êtes libre de le réutiliser, le modifier et le partager.

```

---

# ✅ 2. **requirements.txt (colle dans un fichier à la racine)**

👉 Crée un fichier `requirements.txt` et colle ceci :

```

pandas
numpy
scikit-learn
matplotlib
streamlit
joblib

```

---

# ✅ 3. **.gitignore (important pour éviter les fichiers inutiles)**  

👉 Crée un fichier `.gitignore` et colle ceci :

```

# Environnements

.env
.venv
**pycache**/
.ipynb_checkpoints/
*.pkl

# Données sensibles

data/raw/*
!data/raw/hospital_daily.csv

# Fichiers système

.DS_Store
Thumbs.db

```

---




