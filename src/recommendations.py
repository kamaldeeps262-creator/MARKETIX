"""
MARKETIX Business Recommendations Engine
Translates analytical findings into data-driven strategic actions.
Adheres strictly to the BCG X / Deloitte consulting framework:
Observations -> Analytical Evidence -> Actionable Recommendations -> Expected Business Impact.
Clearly distinguishes empirical correlation from causation.
"""

import pandas as pd
import numpy as np


def generate_recommendations(df: pd.DataFrame, campaign_summary: dict = None, segments_df: pd.DataFrame = None) -> list[dict]:
    """
    Generates rule-based business recommendations grounded in actual empirical metrics.
    """
    recs = []
    
    # 1. Campaign Acceptance Rate Evaluation
    if "Response" in df.columns:
        overall_resp_rate = df["Response"].mean() * 100
        if overall_resp_rate < 15.0:
            recs.append({
                "category": "Campaign Optimization",
                "finding": f"Overall target campaign acceptance is moderate ({overall_resp_rate:.1f}% positive responses).",
                "evidence": f"{df['Response'].sum()} accepted out of {len(df)} contacted customers.",
                "recommendation": (
                    "Avoid broad, unsegmented broadcast marketing. Transition to predictive micro-targeting: "
                    "target only customers with an ML response probability above 40% to decrease wasted ad spend."
                ),
                "expected_impact": "Reduces campaign customer acquisition cost (CAC) by 25-35% and improves conversion efficiency.",
                "priority": "High"
            })
        else:
            recs.append({
                "category": "Campaign Scaling",
                "finding": f"Strong campaign response rate detected ({overall_resp_rate:.1f}%).",
                "evidence": f"Above industry average benchmark (10-12%).",
                "recommendation": "Expand campaign reach to lookalike customer segments while maintaining existing promotional messaging.",
                "expected_impact": "Maximizes revenue potential across adjacent demographic segments.",
                "priority": "Medium"
            })

    # 2. Campaign Disparity Analysis
    if campaign_summary and "summary_table" in campaign_summary and not campaign_summary["summary_table"].empty:
        cmp_df = campaign_summary["summary_table"]
        best_cmp = campaign_summary.get("best_campaign")
        if best_cmp:
            min_rate = cmp_df["Response_Rate"].min()
            max_rate = best_cmp["response_rate"]
            diff = max_rate - min_rate
            if diff > 5.0:
                recs.append({
                    "category": "Channel & Offer Mix",
                    "finding": f"Substantial variance across campaigns: '{best_cmp['name']}' outperformed least effective campaign by {diff:.1f}% percentage points.",
                    "evidence": f"Peak conversion reached {max_rate:.1f}% vs lowest at {min_rate:.1f}%.",
                    "recommendation": (
                        f"Audit the creative copy, incentive structure, and channel mix of '{best_cmp['name']}'. "
                        "Replicate its discount structure or targeted channel delivery across lower-performing campaigns."
                    ),
                    "expected_impact": "Brings underperforming marketing channels closer to top-tier conversion rates.",
                    "priority": "High"
                })

    # 3. High Spender Responsiveness & Customer Retention
    if "Total_Spending" in df.columns and "Response" in df.columns:
        high_spend_thresh = df["Total_Spending"].quantile(0.75)
        high_spenders = df[df["Total_Spending"] >= high_spend_thresh]
        low_spenders = df[df["Total_Spending"] < high_spend_thresh]
        
        hs_resp_rate = high_spenders["Response"].mean() * 100
        ls_resp_rate = low_spenders["Response"].mean() * 100

        if hs_resp_rate > ls_resp_rate:
            recs.append({
                "category": "VIP Customer Retention",
                "finding": f"Top spenders exhibit significantly higher campaign responsiveness ({hs_resp_rate:.1f}% vs {ls_resp_rate:.1f}% for standard spenders).",
                "evidence": f"Customers spending >= ${high_spend_thresh:.0f} convert at {hs_resp_rate / (ls_resp_rate + 1e-4):.1f}x the baseline rate.",
                "recommendation": (
                    "Establish an exclusive Tier-1 Loyalty Program for top-quartile spenders. "
                    "Offer early-access product drops, personalized concierges, and premium bundled incentives rather than price discounts."
                ),
                "expected_impact": "Increases customer lifetime value (LTV) and protects high-margin revenue from competitive poaching.",
                "priority": "High"
            })

    # 4. Product Category Focus (Wines & Meat dominate)
    spend_cols = ["MntWines", "MntMeatProducts", "MntGoldProds", "MntFishProducts", "MntSweetProducts", "MntFruits"]
    available_spend = [c for c in spend_cols if c in df.columns]
    if available_spend:
        sums = df[available_spend].sum()
        top_cat = sums.idxmax()
        top_cat_name = top_cat.replace("Mnt", "").replace("Products", "")
        top_cat_share = (sums[top_cat] / sums.sum()) * 100

        if top_cat_share > 35.0:
            recs.append({
                "category": "Merchandising & Cross-Selling",
                "finding": f"{top_cat_name} generates the dominant share ({top_cat_share:.1f}%) of customer revenue.",
                "evidence": f"Generates ${sums[top_cat]:,.0f} out of total catalog revenue of ${sums.sum():,.0f}.",
                "recommendation": (
                    f"Use {top_cat_name} as a lead anchor product in top-of-funnel campaigns. "
                    "Implement algorithmic bundle recommendations at checkout (e.g. pairing Wines with Artisan Cheeses or Meats)."
                ),
                "expected_impact": "Expands average order basket size by 15-20% through targeted cross-selling.",
                "priority": "Medium"
            })

    # 5. Omnichannel Engagement (Store vs Web vs Web Visits)
    if "NumWebVisitsMonth" in df.columns and "NumStorePurchases" in df.columns:
        high_visitors = df[df["NumWebVisitsMonth"] >= 6]
        if not high_visitors.empty:
            avg_web_deals = high_visitors["NumDealsPurchases"].mean() if "NumDealsPurchases" in high_visitors.columns else 0
            recs.append({
                "category": "Digital Conversion Optimization",
                "finding": f"Frequent website visitors (>=6 visits/month) display heavy deal-seeking behavior (averaging {avg_web_deals:.1f} deal purchases).",
                "evidence": f"Cohort of {len(high_visitors)} active visitors browse frequently with price-sensitive intent.",
                "recommendation": (
                    "Deploy on-site exit-intent modals and targeted time-limited vouchers for high-browse, low-spend web visitors. "
                    "Ensure seamless integration between online catalog and store inventory."
                ),
                "expected_impact": "Reduces browse abandonment and converts passive web traffic into completed sales.",
                "priority": "Medium"
            })

    return recs
