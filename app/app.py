# app/app.py
import pandas as pd
import numpy as np
import joblib
import streamlit as st
from pathlib import Path
from datetime import timedelta

# ================== CONFIG ==================
st.set_page_config(page_title="SPH – Prévision sorties lits", layout="wide")
ROOT = Path(_file_).resolve().parents[1]
DATA_PATH  = ROOT / "data" / "raw" / "hospital_daily.csv"
MODEL_PATH = ROOT / "models" / "baseline_linreg.pkl"
FEATS = ["dow", "lag1", "lag7", "ma7"]

# ================== STYLES ==================
st.markdown("""
<style>
/* Police plus lisible */
html, body, [class*="css"] { font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
[data-testid="stMetricValue"] { font-weight: 700 !important; }
.badge { padding: 4px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; display:inline-block; }
.badge.ok  { background:#E9F9EE; color:#1D7A46; border:1px solid #B9E7C9; }
.badge.warn{ background:#FFF5E5; color:#8C4B00; border:1px solid #FFD59E; }
.card { border:1px solid #eee; border-radius:16px; padding:16px; }
.small { color:#666; font-size:12px; }
hr { border: none; height: 1px; background: #eee; margin: 6px 0 12px; }
</style>
""", unsafe_allow_html=True)

# ================== HELPERS ==================
def fmt_int(x): 
    try:
        return f"{int(round(x)):,}".replace(",", " ")
    except Exception:
        return "—"

def load_data_and_model():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"]).sort_values("date")
    m  = joblib.load(MODEL_PATH)
    return df, m

def build_features(df):
    data = df.copy()
    data["dow"]  = data["date"].dt.dayofweek
    data["lag1"] = data["discharges"].shift(1)
    data["lag7"] = data["discharges"].shift(7)
    data["ma7"]  = data["discharges"].rolling(7).mean()
    data = data.dropna(subset=["lag1","lag7","ma7"]).reset_index(drop=True)
    return data

def predict_next_days(model, data):
    last_date = data["date"].max()
    s = data.set_index("date")["discharges"]

    # J+1
    d1 = last_date + timedelta(days=1)
    X1 = pd.DataFrame([{
        "dow": d1.weekday(),
        "lag1": s.iloc[-1],
        "lag7": s.iloc[-7],
        "ma7":  s.iloc[-7:].mean()
    }], columns=FEATS)
    p1 = float(model.predict(X1)[0])

    # J+2 (récursif)
    d2 = last_date + timedelta(days=2)
    X2 = pd.DataFrame([{
        "dow": d2.weekday(),
        "lag1": p1,
        "lag7": s.iloc[-6],
        "ma7":  pd.Series([*s.iloc[-6:], p1]).mean()
    }], columns=FEATS)
    p2 = float(model.predict(X2)[0])

    return (d1, p1), (d2, p2)

def compute_baselines_and_mae(model, data):
    from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
    cut = int(len(data)*0.8)
    X, y = data[FEATS], data["discharges"]
    Xtr, Xte = X.iloc[:cut], X.iloc[cut:]
    ytr, yte = y.iloc[:cut], y.iloc[cut:]
    pred = model.predict(Xte)
    mae  = mean_absolute_error(yte, pred)
    mape = mean_absolute_percentage_error(yte, pred)*100

    naive1 = data["discharges"].shift(1).iloc[cut:cut+len(yte)].values
    naive7 = data["discharges"].shift(7).iloc[cut:cut+len(yte)].values
    mae_n1 = mean_absolute_error(yte, naive1)
    mae_n7 = mean_absolute_error(yte, naive7)
    return (mae, mape), (mae_n1, mae_n7), (yte.index, yte.values, pred)

# ================== SIDEBAR ==================
st.sidebar.header("⚙ Paramètres d’affichage")
window = st.sidebar.select_slider("Fenêtre historique", options=[7, 14, 30, 60, 90, 180], value=30)
smooth = st.sidebar.checkbox("Lissee la courbe (MM7)", value=True)
percentile = st.sidebar.slider("Seuil d’alerte (percentile historique)", 50, 95, 75, step=5)
st.sidebar.caption("Astuce : passe à 90 jours pour une vue plus globale.")

# ================== CHARGEMENT ==================
df, m = load_data_and_model()
data = build_features(df)

# petit garde-fou : data doit être “plus court” (lags/ma7)
last_hist = df.tail(window).copy()
if smooth:
    last_hist["discharges_mm7"] = last_hist["discharges"].rolling(7).mean()

# prévisions J+1/J+2
(d1, p1), (d2, p2) = predict_next_days(m, data)

# seuil d’alerte basé sur percentile
threshold = int(df["discharges"].quantile(percentile/100))
badge1 = '<span class="badge warn">🔴 Alerte</span>' if p1 >= threshold else '<span class="badge ok">🟢 OK</span>'
badge2 = '<span class="badge warn">🔴 Alerte</span>' if p2 >= threshold else '<span class="badge ok">🟢 OK</span>'

# ================== HEADER ==================
st.title("🧹 Pilotage SPH — Prévisions de sorties (lits à traiter)")
st.caption("Sorties = rad + dc (quotidien). Modèle baseline : dow, lag1, lag7, ma7.")

# ================== METRICS ==================
m1, m2, m3 = st.columns([1,1,1])
m1.metric(f"Prévision J+1 ({d1.date()})", fmt_int(p1), delta=None)
m2.metric(f"Prévision J+2 ({d2.date()})", fmt_int(p2), delta=None)
m3.markdown(f"""
<div class="card">
<b>Seuil d’alerte</b> : {fmt_int(threshold)} lits<hr/>
J+1 : {badge1} &nbsp;&nbsp; J+2 : {badge2}<br/>
<span class="small">Réglable via le percentile dans la barre latérale</span>
</div>
""", unsafe_allow_html=True)

# ================== TABS ==================
tab1, tab2, tab3 = st.tabs(["📈 Historique & Prévisions", "📥 Export", "🔎 Diagnostics modèle"])

with tab1:
    st.subheader("Historique récent et prévisions")
    # Préparer série à afficher
    plot_df = last_hist[["date","discharges"]].copy()
    plot_df = plot_df.rename(columns={"discharges":"Réel (quotidien)"})
    pred_df = pd.DataFrame({"date":[d1, d2], "Prévision":[p1, p2]})

    if smooth:
        plot_df["Réel (MM7)"] = last_hist["discharges_mm7"]

    # Chart
    st.line_chart(plot_df.set_index("date"))

    # Points de prévision
    st.write("*Prévisions*")
    c1, c2 = st.columns(2)
    c1.metric(f"J+1 ({d1.date()})", fmt_int(p1))
    c2.metric(f"J+2 ({d2.date()})", fmt_int(p2))

with tab2:
    st.subheader("Exporter les données")
    # Table des 30 derniers jours + prévisions
    export_df = df.tail(window).copy()[["date","admissions","discharges"]]
    export_df = pd.concat([export_df, pd.DataFrame({
        "date":[d1, d2],
        "admissions":[np.nan, np.nan],
        "discharges":[p1, p2]
    })]).reset_index(drop=True)

    st.dataframe(export_df.rename(columns={
        "date":"Date", "admissions":"Admissions (≈)", "discharges":"Sorties (réel/prévu)"
    }), use_container_width=True)

    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Télécharger CSV (historique + prévisions)", data=csv, file_name="sph_forecast_export.csv", mime="text/csv")

with tab3:
    st.subheader("Qualité du modèle (baseline)")
    (mae, mape), (mae_n1, mae_n7), (idx, y_true, y_pred) = compute_baselines_and_mae(m, data)

    c1, c2, c3 = st.columns(3)
    c1.metric("MAE (modèle)", fmt_int(mae))
    c2.metric("MAE Naïf-1", fmt_int(mae_n1))
    c3.metric("MAE Naïf-7", fmt_int(mae_n7))
    st.caption(f"MAPE (modèle) : {mape:.1f} %  —  Le modèle doit battre Naïf-1 et Naïf-7.")

    # Mini-plot résidus
    res = pd.DataFrame({
        "date": data.iloc[idx]["date"].values,
        "residus": (y_true - y_pred)
    }).set_index("date")
    st.line_chart(res)
    st.caption("Résidus (réel - prédit) sur la période de test")

st.markdown("<br><span class='small'>© SPH Forecast — baseline lags&MA7. Améliorer avec jours fériés, effectifs, admissions lag, etc.</span>", unsafe_allow_html=True)
