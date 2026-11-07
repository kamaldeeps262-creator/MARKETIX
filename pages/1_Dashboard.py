"""
MARKETIX Module 1: Executive Marketing Dashboard
Comprehensive overview of marketing campaign performance, customer metrics,
and multi-channel conversion KPIs.
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
from src.analytics import compute_kpis, compute_category_spend_breakdown, compute_purchase_channel_breakdown
from src.campaign_analysis import analyze_campaign_performance
from src.visualizations import plot_campaign_comparison, plot_spend_donut, plot_channel_comparison, plot_income_vs_spending

st.set_page_config(page_title="Dashboard | MARKETIX", page_icon="📊", layout="wide")

st.title("📊 Marketing Intelligence Dashboard")
st.caption("Real-time executive performance monitoring, marketing KPIs, and demographic distributions.")

# Data Access
if "cleaned_df" not in st.session_state or st.session_state["cleaned_df"] is None:
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        st.session_state["cleaned_df"] = df_clean
        st.session_state["clean_report"] = report

df = st.session_state.get("cleaned_df")

if df is None:
    st.warning("⚠️ No dataset available. Please visit the **Data Management** page to upload your data.")
    st.stop()

# Interactive Filter Bar
with st.expander("🔍 Filter Dashboard Data", expanded=False):
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        edu_options = ["All"] + sorted(df["Education"].dropna().unique().tolist()) if "Education" in df.columns else ["All"]
        selected_edu = st.selectbox("Education Level", edu_options)
    with f_col2:
        mar_options = ["All"] + sorted(df["Marital_Status"].dropna().unique().tolist()) if "Marital_Status" in df.columns else ["All"]
        selected_mar = st.selectbox("Marital Status", mar_options)
    with f_col3:
        min_inc = int(df["Income"].min()) if "Income" in df.columns else 0
        max_inc = int(df["Income"].max()) if "Income" in df.columns else 100000
        income_range = st.slider("Income Range ($)", min_value=min_inc, max_value=min(max_inc, 150000), value=(min_inc, min(max_inc, 120000)))

# Apply Filters
df_filtered = df.copy()
if selected_edu != "All" and "Education" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["Education"] == selected_edu]
if selected_mar != "All" and "Marital_Status" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["Marital_Status"] == selected_mar]
if "Income" in df_filtered.columns:
    df_filtered = df_filtered[(df_filtered["Income"] >= income_range[0]) & (df_filtered["Income"] <= income_range[1])]

# 1. Executive KPI Cards
kpis = compute_kpis(df_filtered)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("Total Customers", f"{kpis['total_customers']:,}")
with c2:
    st.metric("Campaigns Analyzed", f"{kpis['total_campaigns']}")
with c3:
    st.metric("Positive Responses", f"{kpis['positive_responses']:,}")
with c4:
    st.metric("Response Rate", f"{kpis['response_rate']:.2f}%")
with c5:
    st.metric("Average Income", f"${kpis['average_income']:,.0f}")
with c6:
    st.metric("Average Spending", f"${kpis['average_spending']:,.0f}")

st.markdown("---")

# 2. Main Analytics Row: Campaign Performance & Spend Breakdown
row1_left, row1_right = st.columns([3, 2])

with row1_left:
    camp_analysis = analyze_campaign_performance(df_filtered)
    fig_camp = plot_campaign_comparison(camp_analysis["summary_table"])
    st.plotly_chart(fig_camp, use_container_width=True)

with row1_right:
    spend_df = compute_category_spend_breakdown(df_filtered)
    fig_spend = plot_spend_donut(spend_df)
    st.plotly_chart(fig_spend, use_container_width=True)

# 3. Secondary Analytics Row: Channels & Income Correlation
row2_left, row2_right = st.columns([2, 3])

with row2_left:
    channel_df = compute_purchase_channel_breakdown(df_filtered)
    fig_channel = plot_channel_comparison(channel_df)
    st.plotly_chart(fig_channel, use_container_width=True)

with row2_right:
    fig_scatter = plot_income_vs_spending(df_filtered)
    st.plotly_chart(fig_scatter, use_container_width=True)

# 4. Campaign Summary Highlights Table
st.subheader("📋 Campaign Acceptance Summary")
st.dataframe(
    camp_analysis["summary_table"].style.format({
        "Customers_Contacted": "{:,}",
        "Positive_Responses": "{:,}",
        "Response_Rate": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
