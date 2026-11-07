"""
MARKETIX Response Prediction Inference Engine
Provides single-customer interactive inference and batch campaign predictions.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import logging

logger = logging.getLogger("marketix.ml.predict")

MODEL_PATH = Path(__file__).resolve().parent / "saved_models" / "logistic_model.joblib"


def load_model():
    """Loads trained artifacts from disk."""
    if not MODEL_PATH.exists():
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None


def predict_single_customer(customer_data: dict, threshold: float = 0.5) -> dict:
    """
    Computes predicted response and likelihood percentage for a single customer profile.
    """
    artifacts = load_model()
    if artifacts is None:
        return {"error": "Model has not been trained yet. Please run model training first."}

    model = artifacts["model"]
    scaler = artifacts["scaler"]
    feature_names = artifacts["feature_names"]

    # Build input row matching feature_names
    input_row = {feat: 0.0 for feat in feature_names}
    
    # Fill numeric values
    for k, v in customer_data.items():
        if k in input_row:
            try:
                input_row[k] = float(v)
            except (ValueError, TypeError):
                pass

    # One-hot encoding matches
    edu = customer_data.get("Education")
    if edu:
        dummy_col = f"Education_{edu}"
        if dummy_col in input_row:
            input_row[dummy_col] = 1.0

    marital = customer_data.get("Marital_Status")
    if marital:
        dummy_col = f"Marital_Status_{marital}"
        if dummy_col in input_row:
            input_row[dummy_col] = 1.0

    # Convert to DataFrame with exact column order
    input_df = pd.DataFrame([input_row])[feature_names]
    input_scaled = scaler.transform(input_df)

    prob = float(model.predict_proba(input_scaled)[0, 1])
    is_positive = prob >= threshold

    return {
        "customer_id": customer_data.get("ID", 101),
        "predicted_response": bool(is_positive),
        "probability_positive": round(prob * 100, 2),
        "probability_negative": round((1.0 - prob) * 100, 2),
        "prediction_label": "Likely to Respond" if is_positive else "Unlikely to Respond",
        "threshold_used": threshold,
        "model_version": artifacts.get("version", "1.0-logreg")
    }


def predict_batch_customers(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Scores an entire customer DataFrame and appends prediction columns.
    """
    artifacts = load_model()
    if artifacts is None:
        raise ValueError("Model artifacts not found.")

    model = artifacts["model"]
    scaler = artifacts["scaler"]
    feature_names = artifacts["feature_names"]
    available_numeric = artifacts["available_numeric"]
    available_cat = artifacts["available_cat"]

    df_in = df.copy()
    X_num = df_in[[c for c in available_numeric if c in df_in.columns]].copy()
    for col in X_num.columns:
        X_num[col] = X_num[col].fillna(X_num[col].median())

    if available_cat:
        X_cat = pd.get_dummies(df_in[[c for c in available_cat if c in df_in.columns]], drop_first=True, dtype=float)
        X = pd.concat([X_num, X_cat], axis=1)
    else:
        X = X_num

    # Align columns
    X_aligned = pd.DataFrame(0.0, index=df_in.index, columns=feature_names)
    for col in feature_names:
        if col in X.columns:
            X_aligned[col] = X[col]

    X_scaled = scaler.transform(X_aligned)
    probabilities = model.predict_proba(X_scaled)[:, 1]

    df_in["Predicted_Probability"] = np.round(probabilities * 100, 2)
    df_in["Predicted_Response"] = (probabilities >= threshold).astype(int)
    df_in["Response_Likelihood"] = np.where(probabilities >= threshold, "Likely to Respond", "Unlikely to Respond")

    return df_in
