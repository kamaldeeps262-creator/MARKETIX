"""
MARKETIX Core Analytics Engine
Computes key performance indicators (KPIs), summary statistics,
and business metrics from customer marketing data.
"""

import pandas as pd
import numpy as np


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Computes primary high-level marketing metrics:
    - Total Customers
    - Total Campaigns analyzed
    - Total Positive Responses
    - Response Rate (%)
    - Average Income ($)
    - Average Spending ($)
    """
    total_customers = int(len(df))
    
    # Target campaign response column
    resp_col = "Response" if "Response" in df.columns else None
    pos_responses = int(df[resp_col].sum()) if resp_col else 0
    resp_rate = round((pos_responses / total_customers * 100), 2) if total_customers > 0 else 0.0

    avg_income = round(float(df["Income"].mean()), 2) if "Income" in df.columns and len(df) > 0 else 0.0
    
    if "Total_Spending" in df.columns:
        avg_spending = round(float(df["Total_Spending"].mean()), 2)
    else:
        spend_cols = [c for c in ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"] if c in df.columns]
        avg_spending = round(float(df[spend_cols].sum(axis=1).mean()), 2) if spend_cols else 0.0

    # Count campaigns present
    cmp_cols = [c for c in ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"] if c in df.columns]
    total_campaigns = len(cmp_cols)

    return {
        "total_customers": total_customers,
        "total_campaigns": total_campaigns if total_campaigns > 0 else 5,
        "positive_responses": pos_responses,
        "response_rate": resp_rate,
        "average_income": avg_income,
        "average_spending": avg_spending,
    }


def compute_category_spend_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Returns total and average spending per product category."""
    mapping = {
        "MntWines": "Wines",
        "MntFruits": "Fruits",
        "MntMeatProducts": "Meat Products",
        "MntFishProducts": "Fish Products",
        "MntSweetProducts": "Sweet Treats",
        "MntGoldProds": "Gold Products"
    }
    records = []
    for col, name in mapping.items():
        if col in df.columns:
            tot = df[col].sum()
            avg = df[col].mean()
            records.append({
                "Category": name,
                "Total_Spending": round(float(tot), 2),
                "Average_Spending": round(float(avg), 2),
                "Share_Pct": 0.0 # will calculate below
            })
    
    res_df = pd.DataFrame(records)
    if not res_df.empty and res_df["Total_Spending"].sum() > 0:
        res_df["Share_Pct"] = round(res_df["Total_Spending"] / res_df["Total_Spending"].sum() * 100, 2)
        res_df = res_df.sort_values(by="Total_Spending", ascending=False).reset_index(drop=True)
    return res_df


def compute_purchase_channel_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Returns breakdown of purchase channel engagement."""
    channels = {
        "NumStorePurchases": "Store Purchases",
        "NumWebPurchases": "Web Purchases",
        "NumCatalogPurchases": "Catalog Purchases",
        "NumDealsPurchases": "Discount Purchases"
    }
    records = []
    for col, name in channels.items():
        if col in df.columns:
            tot = df[col].sum()
            avg = df[col].mean()
            records.append({
                "Channel": name,
                "Total_Purchases": int(tot),
                "Average_Per_Customer": round(float(avg), 2)
            })
    res_df = pd.DataFrame(records)
    if not res_df.empty and res_df["Total_Purchases"].sum() > 0:
        res_df["Share_Pct"] = round(res_df["Total_Purchases"] / res_df["Total_Purchases"].sum() * 100, 2)
        res_df = res_df.sort_values(by="Total_Purchases", ascending=False).reset_index(drop=True)
    return res_df
