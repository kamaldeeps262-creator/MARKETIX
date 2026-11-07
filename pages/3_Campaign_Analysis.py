"""
MARKETIX Module 3: Campaign Performance Analysis
In-depth comparative analysis of marketing campaigns, channel conversion,
and customer response distribution.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.campaign_analysis import analyze_campaign_performance, analyze_channel_performance
from src.visualizations import plot_campaign_comparison, plot_channel_comparison
import plotly.express as px

st.set_page_config(page_title="Campaign Analysis | MARKETIX", page_icon="📈", layout="wide")

st.title("📈 Campaign Performance Analysis")
st.caption("Benchmark conversion rates across multi-wave marketing campaigns and acquisition channels.")

# Load active data
if "cleaned_df" not in st.session_state or st.session_state["cleaned_df"] is None:
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        st.session_state["cleaned_df"] = df_clean

df = st.session_state.get("cleaned_df")
if df is None:
    st.warning("⚠️ No dataset loaded. Please go to Data Management.")
    st.stop()

# Run Campaign Analysis
camp_results = analyze_campaign_performance(df)
summary_table = camp_results["summary_table"]
best_cmp = camp_results["best_campaign"]

# Top Highlight: Best Campaign & Formula
col_highlight, col_formula = st.columns([3, 2])

with col_highlight:
    if best_cmp:
        st.success(
            f"🏆 **Top Performing Campaign: {best_cmp['name']}**\n\n"
            f"- **Acceptance Rate:** `{best_cmp['response_rate']:.2f}%`\n"
            f"- **Positive Conversions:** `{best_cmp['responses']:,}` out of `{camp_results['total_contacted']:,}` customers contacted."
        )

with col_formula:
    st.markdown("**Campaign Acceptance Rate Formula:**")
    st.latex(r"\text{Response Rate} = \frac{\text{Positive Responses}}{\text{Customers Contacted}} \times 100")
    st.caption("Tracks the percentage of targeted prospects converting to campaign offers.")

st.markdown("---")

# Visual Comparison Chart
col_chart, col_stats = st.columns([3, 2])

with col_chart:
    fig_cmp = plot_campaign_comparison(summary_table)
    st.plotly_chart(fig_cmp, use_container_width=True)

with col_stats:
    st.markdown("### Campaign Summary Table")
    st.dataframe(
        summary_table[["Campaign_Name", "Positive_Responses", "Response_Rate"]].rename(
            columns={"Positive_Responses": "Responses", "Response_Rate": "Acceptance %"}
        ),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# Customer Campaign Loyalty & Omnichannel Performance
c_row1, c_row2 = st.columns(2)

with c_row1:
    st.subheader("🔁 Campaign Response Multiplicity")
    st.caption("Measures how many historical campaigns each customer accepted.")
    eng_dist = camp_results["engagement_distribution"]
    if eng_dist:
        eng_df = pd.DataFrame([
            {"Campaigns Accepted": k, "Customer Count": v, "Percentage": round((v / len(df)) * 100, 2)}
            for k, v in eng_dist.items()
        ])
        fig_eng = px.bar(
            eng_df,
            x="Campaigns Accepted",
            y="Customer Count",
            text="Percentage",
            color="Customer Count",
            color_continuous_scale="Blues",
            title="<b>Distribution of Historical Campaign Acceptance</b>",
            template="plotly_white"
        )
        fig_eng.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig_eng, use_container_width=True)

with c_row2:
    st.subheader("🛍️ Purchase Acquisition Channels")
    st.caption("Evaluates volume of purchases through Store, Web, Catalog, and Deal promotions.")
    chan_df = analyze_channel_performance(df)
    fig_chan = plot_channel_comparison(chan_df)
    st.plotly_chart(fig_chan, use_container_width=True)

st.markdown("---")
st.subheader("💡 Analytical Insights (BCG X Decision Framework)")
st.markdown("""
- **Conversion Disparity:** The latest campaign recorded an acceptance rate of **14.91%**, significantly higher than early campaigns like Campaign 2 (1.34%).
- **Multi-Wave Loyalty:** Customers who accepted 2 or more previous campaigns represent high-value targets with significantly elevated propensities to convert on future offers.
- **Physical vs Digital Touchpoints:** In-store purchases remain the primary channel by transaction volume, closely followed by direct web catalog purchases.
""")
