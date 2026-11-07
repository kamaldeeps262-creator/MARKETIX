"""
MARKETIX Campaign Analysis Module
Evaluates and compares performance across all marketing campaigns.
"""

import pandas as pd
import numpy as np


def analyze_campaign_performance(df: pd.DataFrame) -> dict:
    """
    Analyzes historical campaigns (1 through 5) and the latest target campaign.
    Calculates contacts, responses, response rates, and identifies the top-performing campaign.
    """
    total_customers = len(df)
    campaign_cols = {
        "AcceptedCmp1": "Campaign 1 (Email)",
        "AcceptedCmp2": "Campaign 2 (Direct Mail)",
        "AcceptedCmp3": "Campaign 3 (Discount Voucher)",
        "AcceptedCmp4": "Campaign 4 (Catalog Special)",
        "AcceptedCmp5": "Campaign 5 (Premium Club)",
        "Response": "Latest Campaign (Target)"
    }
    
    records = []
    for col, name in campaign_cols.items():
        if col in df.columns:
            responses = int(df[col].sum())
            rate = round((responses / total_customers * 100), 2) if total_customers > 0 else 0.0
            records.append({
                "Campaign_Key": col,
                "Campaign_Name": name,
                "Customers_Contacted": total_customers,
                "Positive_Responses": responses,
                "Response_Rate": rate
            })
            
    summary_df = pd.DataFrame(records)
    
    # Identify best performing campaign
    best_campaign = None
    if not summary_df.empty:
        best_row = summary_df.loc[summary_df["Response_Rate"].idxmax()]
        best_campaign = {
            "name": best_row["Campaign_Name"],
            "key": best_row["Campaign_Key"],
            "response_rate": best_row["Response_Rate"],
            "responses": int(best_row["Positive_Responses"])
        }

    # Customer loyalty: How many campaigns did customers accept?
    cmp_subset = [c for c in ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"] if c in df.columns]
    engagement_distribution = {}
    if cmp_subset:
        eng_counts = df[cmp_subset].sum(axis=1).value_counts().sort_index()
        engagement_distribution = {f"{k} Campaigns Accepted": int(v) for k, v in eng_counts.items()}

    return {
        "summary_table": summary_df,
        "best_campaign": best_campaign,
        "engagement_distribution": engagement_distribution,
        "total_contacted": total_customers,
    }


def analyze_channel_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates sales conversion across channels: Store, Web, Catalog, and Deals.
    """
    channels = {
        "NumStorePurchases": ("Store Purchases", "In-Store Experience"),
        "NumWebPurchases": ("Web Purchases", "Digital / E-Commerce"),
        "NumCatalogPurchases": ("Catalog Purchases", "Direct Print / Mail"),
        "NumDealsPurchases": ("Deal Purchases", "Promotional Discounts"),
    }
    records = []
    for col, (label, desc) in channels.items():
        if col in df.columns:
            total_purch = int(df[col].sum())
            avg_purch = round(float(df[col].mean()), 2)
            records.append({
                "Channel": label,
                "Category": desc,
                "Total_Transactions": total_purch,
                "Avg_Per_Customer": avg_purch
            })
    res_df = pd.DataFrame(records)
    if not res_df.empty and res_df["Total_Transactions"].sum() > 0:
        res_df["Transaction_Share_%"] = round(res_df["Total_Transactions"] / res_df["Total_Transactions"].sum() * 100, 2)
        res_df = res_df.sort_values(by="Total_Transactions", ascending=False).reset_index(drop=True)
    return res_df
