import json
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "anantapur_balanced_crops.csv"
ARTIFACTS_DIR = ROOT / "stage2" / "artifacts"


SEASON_TO_INT = {"Kharif": 0, "Rabi": 1, "Summer": 2}


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATASET_PATH)
    required_cols = ["pH", "TDS", "Turbidity", "Temp", "Season", "Recommended_Crop"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")

    # Train only on rows that actually map to one of the 16 crops.
    df = df[df["Recommended_Crop"].astype(str).str.strip().ne("No Crops Suitable")].copy()
    df = df[df["Season"].isin(SEASON_TO_INT.keys())].copy()

    # Build season -> crops mapping for strict seasonal filtering at inference time.
    season_to_crops = (
        df.groupby("Season")["Recommended_Crop"]
        .apply(lambda s: sorted(set(map(str, s))))
        .to_dict()
    )

    # Features
    X_num = df[["pH", "TDS", "Turbidity", "Temp"]].astype(float).values
    X_season = df["Season"].map(SEASON_TO_INT).astype(int).values.reshape(-1, 1)

    scaler = StandardScaler()
    X_num_scaled = scaler.fit_transform(X_num)
    X = np.hstack([X_num_scaled, X_season])

    # Target
    y_raw = df["Recommended_Crop"].astype(str).values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=450,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample",
        min_samples_leaf=2,
    )
    model.fit(X_train, y_train)

    acc = float(model.score(X_test, y_test))
    print(f"[stage2] RandomForest test accuracy: {acc:.4f}")
    print(f"[stage2] Classes: {list(label_encoder.classes_)}")

    joblib.dump(model, ARTIFACTS_DIR / "stage2_random_forest.pkl")
    joblib.dump(scaler, ARTIFACTS_DIR / "stage2_scaler.pkl")
    joblib.dump(label_encoder, ARTIFACTS_DIR / "stage2_label_encoder.pkl")

    (ARTIFACTS_DIR / "stage2_season_to_crops.json").write_text(
        json.dumps(season_to_crops, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ARTIFACTS_DIR / "stage2_metadata.json").write_text(
        json.dumps(
            {
                "dataset": str(DATASET_PATH.name),
                "season_to_int": SEASON_TO_INT,
                "n_crops": int(len(label_encoder.classes_)),
                "model": "RandomForestClassifier",
                "test_accuracy": acc,
                "feature_order": ["pH", "TDS", "Turbidity", "Temp", "SeasonInt"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[stage2] Saved artifacts to: {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()

