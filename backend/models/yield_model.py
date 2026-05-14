"""
ML-powered Crop Yield Prediction Model.
Uses RandomForestRegressor trained on synthetic Karnataka agricultural data.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from typing import Tuple

from data.generate_dataset import generate_karnataka_crop_data, save_dataset
import config


FEATURE_COLUMNS = [
    "rainfall_mm",
    "temperature_c",
    "soil_ph",
    "soil_moisture_pct",
    "fertilizer_kg_per_hectare",
    "irrigation_level_pct",
]

TARGET_COLUMN = "yield_tons_per_hectare"

# Global model instance
_model: RandomForestRegressor = None
_model_metrics: dict = {}


def _get_or_create_dataset() -> pd.DataFrame:
    """Load existing dataset or generate a new one."""
    if os.path.exists(config.DATASET_PATH):
        return pd.read_csv(config.DATASET_PATH)

    df = generate_karnataka_crop_data(n_samples=config.TRAINING_SAMPLES)
    save_dataset(df, config.DATASET_PATH)
    return df


def train_model() -> Tuple[RandomForestRegressor, dict]:
    """Train the RandomForest yield prediction model."""
    global _model, _model_metrics

    print(" Training Crop Yield Prediction Model...")

    df = _get_or_create_dataset()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "r2_score": round(r2_score(y_test, y_pred), 4),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_importances": dict(
            zip(FEATURE_COLUMNS, [round(fi, 4) for fi in model.feature_importances_])
        ),
    }

    # Save model
    os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)
    joblib.dump(model, config.MODEL_PATH)

    _model = model
    _model_metrics = metrics

    print(f" Model trained — R2 = {metrics['r2_score']}, MAE = {metrics['mae']}")
    print(f" Model saved -> {config.MODEL_PATH}")

    return model, metrics


def load_model() -> RandomForestRegressor:
    """Load a previously trained model or train a new one."""
    global _model, _model_metrics

    if _model is not None:
        return _model

    if os.path.exists(config.MODEL_PATH):
        print(" Loading pre-trained model...")
        _model = joblib.load(config.MODEL_PATH)
        return _model

    model, _ = train_model()
    return model


def predict_yield(
    rainfall_mm: float,
    temperature_c: float,
    soil_ph: float,
    soil_moisture_pct: float,
    fertilizer_kg_per_hectare: float,
    irrigation_level_pct: float,
) -> dict:
    """
    Predict crop yield given agricultural parameters.
    Returns yield value and metadata.
    """
    model = load_model()

    features = np.array([[
        rainfall_mm,
        temperature_c,
        soil_ph,
        soil_moisture_pct,
        fertilizer_kg_per_hectare,
        irrigation_level_pct,
    ]])

    predicted_yield = float(model.predict(features)[0])
    predicted_yield = round(max(0.5, min(predicted_yield, 8.0)), 2)

    # Confidence from prediction variance across trees
    tree_predictions = np.array([
        tree.predict(features)[0] for tree in model.estimators_
    ])
    std_dev = np.std(tree_predictions)
    confidence = round(max(0.0, min(1.0, 1.0 - (std_dev / predicted_yield))), 2)

    # Categorize yield
    thresholds = config.YIELD_THRESHOLDS
    if predicted_yield < thresholds["very_low"]:
        category = "very_low"
    elif predicted_yield < thresholds["low"]:
        category = "low"
    elif predicted_yield < thresholds["average"]:
        category = "average"
    elif predicted_yield < thresholds["good"]:
        category = "good"
    else:
        category = "excellent"

    return {
        "predicted_yield": predicted_yield,
        "category": category,
        "confidence": confidence,
    }


def get_model_metrics() -> dict:
    """Return model training metrics."""
    return _model_metrics


def get_feature_importances() -> dict:
    """Get feature importances from the trained model."""
    model = load_model()
    return dict(
        zip(FEATURE_COLUMNS, [round(fi, 4) for fi in model.feature_importances_])
    )


if __name__ == "__main__":
    model, metrics = train_model()
    print(f"\n📊 Model Metrics:\n{metrics}")

    # Test prediction
    result = predict_yield(
        rainfall_mm=750,
        temperature_c=28,
        soil_ph=6.5,
        soil_moisture_pct=45,
        fertilizer_kg_per_hectare=80,
        irrigation_level_pct=60,
    )
    print(f"\n🌾 Test Prediction: {result}")
