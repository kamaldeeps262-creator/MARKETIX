"""
MARKETIX ML Model Evaluation Module
Calculates granular performance metrics, confusion matrices, and ROC metrics.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "saved_models" / "logistic_model.joblib"


def get_model_status() -> dict:
    """Checks if model is trained and returns stored metrics."""
    if not MODEL_PATH.exists():
        return {"trained": False, "message": "No trained model found on disk."}
    try:
        artifacts = joblib.load(MODEL_PATH)
        return {
            "trained": True,
            "version": artifacts.get("version", "1.0-logreg"),
            "metrics": artifacts.get("metrics", {}),
            "features_count": len(artifacts.get("feature_names", [])),
            "feature_names": artifacts.get("feature_names", [])
        }
    except Exception as e:
        return {"trained": False, "message": f"Error loading model: {e}"}


def calculate_metrics_summary(y_true, y_pred, y_prob) -> dict:
    """Computes comprehensive evaluation metrics."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4),
        "specificity": round(float(specificity), 4),
        "confusion_matrix": cm.tolist(),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }
