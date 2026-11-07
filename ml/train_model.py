"""
MARKETIX Supervised ML Training Module
Trains a balanced Logistic Regression model to predict customer campaign responses.
Includes rigorous leakage prevention, stratified train/test splitting,
and artifact persistence.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve
import logging

logger = logging.getLogger("marketix.ml.train")

MODEL_DIR = Path(__file__).resolve().parent / "saved_models"
MODEL_PATH = MODEL_DIR / "logistic_model.joblib"

FEATURE_COLUMNS = [
    "Age",
    "Income",
    "Recency",
    "Kidhome",
    "Teenhome",
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
    "NumDealsPurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Customer_Tenure_Days"
]

CATEGORICAL_COLUMNS = ["Education", "Marital_Status"]


def train_logistic_regression(df: pd.DataFrame) -> dict:
    """
    Trains and validates the campaign response classification model.
    """
    if "Response" not in df.columns:
        raise ValueError("Dataset does not contain the target column 'Response'.")

    # 1. Feature selection (Leakage prevention: ensure Response is strictly target)
    available_numeric = [c for c in FEATURE_COLUMNS if c in df.columns]
    available_cat = [c for c in CATEGORICAL_COLUMNS if c in df.columns]

    X_num = df[available_numeric].copy()
    for col in X_num.columns:
        X_num[col] = X_num[col].fillna(X_num[col].median())

    # One-hot encode categoricals
    if available_cat:
        X_cat = pd.get_dummies(df[available_cat], drop_first=True, dtype=float)
        X = pd.concat([X_num, X_cat], axis=1)
    else:
        X = X_num

    y = df["Response"].astype(int)

    # 2. Stratified Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 3. Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Model Training with balanced class weights
    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    # 5. Predictions & Evaluation
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    # 6. Feature Importance (Logistic Regression Coefficients)
    feature_names = list(X.columns)
    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": model.coef_[0]
    }).sort_values(by="Coefficient", ascending=False).reset_index(drop=True)

    # 7. Persist Artifacts
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "model": model,
        "scaler": scaler,
        "feature_names": feature_names,
        "available_numeric": available_numeric,
        "available_cat": available_cat,
        "version": "1.0-logreg",
        "metrics": {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
        }
    }
    joblib.dump(artifacts, MODEL_PATH)

    return {
        "metrics": artifacts["metrics"],
        "confusion_matrix": cm,
        "roc_curve": {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "auc": round(float(auc), 4)},
        "coefficients": coef_df,
        "test_size": len(y_test),
        "train_size": len(y_train),
        "saved_path": str(MODEL_PATH)
    }
