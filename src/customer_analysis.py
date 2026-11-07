"""
MARKETIX Customer Insights Analysis Module
Examines customer demographic patterns, product spending preferences,
and behavioral engagement drivers.
"""

import pandas as pd
import numpy as np


def analyze_demographics(df: pd.DataFrame) -> dict:
    """Analyzes customer age groups, education, and marital status distributions."""
    res = {}
    
    # 1. Age Cohorts
    if "Age" in df.columns:
        bins = [0, 35, 50, 65, 120]
        labels = ["Young Adult (<35)", "Adult (35-50)", "Mature (50-65)", "Senior (65+)"]
        df_temp = df.copy()
        df_temp["Age_Group"] = pd.cut(df_temp["Age"], bins=bins, labels=labels, right=False)
        age_dist = df_temp["Age_Group"].value_counts().sort_index().to_dict()
        res["age_distribution"] = {str(k): int(v) for k, v in age_dist.items()}
        res["median_age"] = float(df["Age"].median())
    
    # 2. Education
    if "Education" in df.columns:
        res["education_distribution"] = {str(k): int(v) for k, v in df["Education"].value_counts().items()}
        
    # 3. Marital Status
    if "Marital_Status" in df.columns:
        res["marital_distribution"] = {str(k): int(v) for k, v in df["Marital_Status"].value_counts().items()}

    # 4. Income statistics
    if "Income" in df.columns:
        res["income_stats"] = {
            "mean": round(float(df["Income"].mean()), 2),
            "median": round(float(df["Income"].median()), 2),
            "std": round(float(df["Income"].std()), 2),
            "min": round(float(df["Income"].min()), 2),
            "max": round(float(df["Income"].max()), 2)
        }
    return res


def analyze_spending_by_tier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Segments customers into spending tiers (Low, Medium, High Spenders)
    and evaluates their respective campaign response rates.
    Directly validates the hypothesis: higher historical spending leads to higher acceptance.
    """
    df_calc = df.copy()
    if "Total_Spending" not in df_calc.columns:
        spend_cols = [c for c in ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"] if c in df_calc.columns]
        df_calc["Total_Spending"] = df_calc[spend_cols].sum(axis=1) if spend_cols else 0

    # Categorize into quartiles: Low (0-25%), Medium (25-75%), High (75-100%)
    q25 = df_calc["Total_Spending"].quantile(0.25)
    q75 = df_calc["Total_Spending"].quantile(0.75)

    def assign_tier(val):
        if val <= q25:
            return "1. Low Spender (Bottom 25%)"
        elif val <= q75:
            return "2. Moderate Spender (25-75%)"
        else:
            return "3. High Spender (Top 25%)"

    df_calc["Spending_Tier"] = df_calc["Total_Spending"].apply(assign_tier)

    # Calculate metrics per tier
    grouped = df_calc.groupby("Spending_Tier").agg(
        Customer_Count=("ID" if "ID" in df_calc.columns else "Total_Spending", "count"),
        Avg_Income=("Income", "mean"),
        Avg_Spending=("Total_Spending", "mean"),
        Avg_Purchases=("Total_Purchases" if "Total_Purchases" in df_calc.columns else "Total_Spending", "mean"),
        Response_Rate=("Response", lambda s: round(s.mean() * 100, 2) if "Response" in df_calc.columns else 0.0)
    ).reset_index()

    grouped["Avg_Income"] = grouped["Avg_Income"].round(2)
    grouped["Avg_Spending"] = grouped["Avg_Spending"].round(2)
    grouped["Avg_Purchases"] = grouped["Avg_Purchases"].round(1)

    return grouped


def analyze_product_affinity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes average spend per product category conditioned on whether the customer
    responded to the latest marketing campaign.
    """
    spend_map = {
        "MntWines": "Wines",
        "MntMeatProducts": "Meat",
        "MntGoldProds": "Gold",
        "MntFishProducts": "Fish",
        "MntSweetProducts": "Sweets",
        "MntFruits": "Fruits"
    }
    
    records = []
    if "Response" in df.columns:
        for col, label in spend_map.items():
            if col in df.columns:
                resp_mean = df[df["Response"] == 1][col].mean()
                non_resp_mean = df[df["Response"] == 0][col].mean()
                records.append({
                    "Product_Category": label,
                    "Responders_Avg_Spend": round(float(resp_mean), 2),
                    "Non_Responders_Avg_Spend": round(float(non_resp_mean), 2),
                    "Spend_Difference_%": round(((resp_mean - non_resp_mean) / (non_resp_mean + 1e-5)) * 100, 2)
                })
    return pd.DataFrame(records).sort_values(by="Spend_Difference_%", ascending=False)
