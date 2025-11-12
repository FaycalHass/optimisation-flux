# src/from_spf_to_daily.py
import pandas as pd
from pathlib import Path

# ========= PARAMÈTRES MODIFIABLES =========
AGGREGATION   = "FR"        # "FR" (France entière) ou "REGION"
REGION_CODE   = None        # ex: "11" pour Île-de-France si AGGREGATION="REGION"
USE_ICU_RATE  = True        # calcule aussi un taux ICU (réanimation)
CAP_ICU       = 7000        # capacité réa (proxy national; remplace par ta capacité locale si dispo)
# ==========================================

RAW_IN  = Path("data/raw/covid_hosp.csv")
RAW_OUT = Path("data/raw/hospital_daily.csv")


def main():
    print(f"📥 READ  : {RAW_IN.resolve()}")
    print(f"📤 WRITE : {RAW_OUT.resolve()}")

    # --- Lecture robuste du CSV SPF ---
    df = pd.read_csv(RAW_IN, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    print("➡️ Colonnes brutes :", df.columns.tolist())
    print("➡️ Nb lignes brutes :", len(df))

    # --- Colonnes utiles si présentes ---
    keep = [c for c in ["jour", "date", "hosp", "rea", "rad", "dc", "sex", "sexe", "dep", "region"] if c in df.columns]
    df = df[keep].copy()

    # Harmoniser 'sexe' -> 'sex'
    if "sexe" in df.columns and "sex" not in df.columns:
        df = df.rename(columns={"sexe": "sex"})

    # Détection/renommage de la colonne date
    date_col = next((c for c in df.columns if c in ("jour", "date")), None)
    if date_col is None:
        raise ValueError(f"Aucune colonne 'jour' ou 'date'. Colonnes lues: {list(df.columns)}")
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.rename(columns={date_col: "jour"})

    # Filtrer agrégat 'tous sexes' si présent
    if "sex" in df.columns:
        df = df[(df["sex"].astype(str) == "0") | (df["sex"].isna())]

    # Option: filtrer région si demandé
    if AGGREGATION.upper() == "REGION" and "region" in df.columns and REGION_CODE is not None:
        df = df[df["region"].astype(str) == str(REGION_CODE)]

    print("➡️ Après nettoyage :", df.shape)

    # --- Agrégation quotidienne (FR ou région) ---
    agg_cols = [c for c in ["hosp", "rea", "rad", "dc"] if c in df.columns]
    if not agg_cols:
        raise ValueError("Aucune des colonnes ['hosp','rea','rad','dc'] n'est disponible pour agréger.")
    daily = (
        df.groupby("jour", as_index=False)[agg_cols]
          .sum()
          .sort_values("jour")
    )
    print("➡️ daily :", daily.shape, "| dates :", daily["jour"].min(), "→", daily["jour"].max())

    # --- Variables projet ---
    out = daily.rename(columns={"jour": "date", "rad": "discharges"})
    # Admissions approx = Δ(hosp) + discharges + dc  (clip ≥ 0)
    hosp = out["hosp"] if "hosp" in out.columns else 0
    dc   = out["dc"]   if "dc"   in out.columns else 0
    out["admissions"] = (getattr(hosp, "diff", lambda: 0)().fillna(0) + out.get("discharges", 0) + dc)\
                        .clip(lower=0).round().astype(int)

    # ➜ Occupation relative (pic = 100%) : remplace l'ancien occupancy_rate basé sur 100 000
    if "hosp" in out.columns and out["hosp"].max() > 0:
        cap_scale = out["hosp"].max()
        out["hosp_rel"] = out["hosp"] / cap_scale  # 0..1, pic=1.0
    else:
        out["hosp_rel"] = pd.NA

    # (Option) Taux ICU (réanimation) si souhaité
    if USE_ICU_RATE and "rea" in out.columns:
        out["icu_rate"] = (out["rea"] / CAP_ICU).clip(0, 1.0)
    else:
        out["icu_rate"] = pd.NA

    # --- Sélection des colonnes finales ---
    final_cols = ["date", "admissions", "discharges"]
    # garder aussi hosp/rea pour contextes & features
    if "hosp" in out.columns:
        final_cols.append("hosp")
    if "rea" in out.columns:
        final_cols.append("rea")
    # ajouter les ratios
    final_cols += ["hosp_rel", "icu_rate"]

    final = out[final_cols].copy()
    print("➡️ final :", final.shape)

    # --- Créer le dossier et écrire ---
    RAW_OUT.parent.mkdir(parents=True, exist_ok=True)
    if final.empty:
        print("⚠️ Aucune ligne agrégée — vérifie le contenu de covid_hosp.csv")
        return

    final.to_csv(RAW_OUT, index=False)
    print(f"✅ Écrit {RAW_OUT} : {final.shape[0]} lignes | "
          f"{final['date'].min().date()} → {final['date'].max().date()}")


if __name__ == "__main__":
    main()
