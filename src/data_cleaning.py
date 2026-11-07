"""
MARKETIX Data Cleaning & Preprocessing Module
Implements robust data cleaning, outlier handling, categorical normalization,
and domain-specific feature engineering for marketing intelligence.
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "cleaned_marketing_data.csv"


def clean_marketing_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw customer marketing dataset:
    - Imputes missing income based on education group medians.
    - Treats birth year outliers (ages > 100).
    - Normalizes marital status anomalies.
    - Converts date columns.
    - Engineers critical marketing domain KPIs: Total_Spending, Total_Purchases,
      Children, Is_Parent, Total_Campaigns_Accepted, Customer_Tenure_Days.
    """
    df_clean = df.copy()
    report = {
        "initial_rows": int(len(df_clean)),
        "initial_columns": int(df_clean.shape[1]),
        "missing_income_imputed": 0,
        "outliers_adjusted": 0,
        "marital_status_normalized": 0,
    }

    # 1. Clean column names
    df_clean.columns = [col.strip() for col in df_clean.columns]

    # 2. Impute Missing Income with Education-Group Median
    if "Income" in df_clean.columns:
        missing_count = int(df_clean["Income"].isnull().sum())
        report["missing_income_imputed"] = missing_count
        if missing_count > 0:
            if "Education" in df_clean.columns:
                df_clean["Income"] = df_clean.groupby("Education")["Income"].transform(
                    lambda grp: grp.fillna(grp.median())
                )
            df_clean["Income"] = df_clean["Income"].fillna(df_clean["Income"].median())

    # 3. Date conversion and Customer Tenure
    if "Dt_Customer" in df_clean.columns:
        df_clean["Dt_Customer"] = pd.to_datetime(df_clean["Dt_Customer"], errors="coerce")
        ref_date = df_clean["Dt_Customer"].max() if pd.notnull(df_clean["Dt_Customer"].max()) else pd.to_datetime("2014-12-31")
        df_clean["Customer_Tenure_Days"] = (ref_date - df_clean["Dt_Customer"]).dt.days.fillna(0).astype(int)

    # 4. Outlier Handling on Year_Birth / Age
    if "Year_Birth" in df_clean.columns:
        current_year = 2026
        df_clean["Age"] = current_year - df_clean["Year_Birth"]
        # Realistic threshold: age > 100 is anomalous in this marketing cohort
        outliers_mask = df_clean["Age"] > 100
        report["outliers_adjusted"] = int(outliers_mask.sum())
        median_age = df_clean.loc[~outliers_mask, "Age"].median()
        df_clean.loc[outliers_mask, "Age"] = median_age
        df_clean.loc[outliers_mask, "Year_Birth"] = current_year - median_age

    # 5. Normalize Marital_Status categories
    if "Marital_Status" in df_clean.columns:
        uncommon_mask = df_clean["Marital_Status"].isin(["Alone", "Absurd", "YOLO"])
        report["marital_status_normalized"] = int(uncommon_mask.sum())
        df_clean["Marital_Status"] = df_clean["Marital_Status"].replace({
            "Alone": "Single",
            "Absurd": "Single",
            "YOLO": "Single"
        })

    # 6. Feature Engineering: Total Spending across 6 categories
    spend_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
    available_spend_cols = [c for c in spend_cols if c in df_clean.columns]
    if available_spend_cols:
        df_clean["Total_Spending"] = df_clean[available_spend_cols].sum(axis=1)

    # 7. Feature Engineering: Total Purchases across channels
    purch_cols = ["NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]
    available_purch_cols = [c for c in purch_cols if c in df_clean.columns]
    if available_purch_cols:
        df_clean["Total_Purchases"] = df_clean[available_purch_cols].sum(axis=1)

    # 8. Feature Engineering: Household composition
    kid_col = df_clean["Kidhome"] if "Kidhome" in df_clean.columns else 0
    teen_col = df_clean["Teenhome"] if "Teenhome" in df_clean.columns else 0
    df_clean["Children"] = kid_col + teen_col
    df_clean["Is_Parent"] = (df_clean["Children"] > 0).astype(int)

    # 9. Feature Engineering: Historical Campaign Responses
    campaign_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]
    available_cmp = [c for c in campaign_cols if c in df_clean.columns]
    if available_cmp:
        df_clean["Total_Campaigns_Accepted"] = df_clean[available_cmp].sum(axis=1)

    # Drop non-informative constant columns if present
    for const_col in ["Z_CostContact", "Z_Revenue"]:
        if const_col in df_clean.columns and df_clean[const_col].nunique() <= 1:
            df_clean = df_clean.drop(columns=[const_col])

    report["final_rows"] = int(len(df_clean))
    report["final_columns"] = int(df_clean.shape[1])

    # Save to processed directory
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)

    return df_clean, report
