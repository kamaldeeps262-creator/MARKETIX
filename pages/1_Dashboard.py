"""
MARKETIX Module 1: Executive Marketing Dashboard — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, kpi_card, kpi_grid, section_header, divider, animated_progress
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.analytics import compute_kpis, compute_category_spend_breakdown, compute_purchase_channel_breakdown
from src.campaign_analysis import analyze_campaign_performance
from src.visualizations import plot_campaign_comparison, plot_spend_donut, plot_channel_comparison, plot_income_vs_spending

st.set_page_config(page_title="Dashboard | MARKETIX", page_icon="📊", layout="wide")
inject_styles()

# ── DATA ──────────────────────────────────────────────────────────────────────
if "cleaned_df" not in st.session_state or st.session_state["cleaned_df"] is None:
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        st.session_state["cleaned_df"] = df_clean

df = st.session_state.get("cleaned_df")
if df is None:
    st.warning("⚠️ No dataset available. Please visit **Data Management** to upload data.")
    st.stop()

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='animation:fadeSlideDown 0.5s ease both;'>
    <h1 style='margin:0;font-size:1.9rem;font-weight:900;color:#0F172A;'>
        📊 Marketing Intelligence Dashboard
    </h1>
    <p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
        Real-time executive performance monitoring across campaigns, customers and channels.
    </p>
</div>
""", unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
with st.expander("🔍  Filter Dashboard  —  click to expand", expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        edu_opts = ["All"] + sorted(df["Education"].dropna().unique().tolist()) if "Education" in df.columns else ["All"]
        sel_edu = st.selectbox("Education Level", edu_opts)
    with f2:
        mar_opts = ["All"] + sorted(df["Marital_Status"].dropna().unique().tolist()) if "Marital_Status" in df.columns else ["All"]
        sel_mar = st.selectbox("Marital Status", mar_opts)
    with f3:
        min_i = int(df["Income"].min()) if "Income" in df.columns else 0
        max_i = int(df["Income"].max()) if "Income" in df.columns else 150000
        inc_range = st.slider("Income Range ($)", min_value=min_i, max_value=min(max_i, 150000),
                              value=(min_i, min(max_i, 120000)))

df_f = df.copy()
if sel_edu != "All" and "Education" in df_f.columns:
    df_f = df_f[df_f["Education"] == sel_edu]
if sel_mar != "All" and "Marital_Status" in df_f.columns:
    df_f = df_f[df_f["Marital_Status"] == sel_mar]
if "Income" in df_f.columns:
    df_f = df_f[(df_f["Income"] >= inc_range[0]) & (df_f["Income"] <= inc_range[1])]

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
kpis = compute_kpis(df_f)
st.markdown(kpi_grid(
    kpi_card("👥", f"{kpis['total_customers']:,}",    "Total Customers"),
    kpi_card("📣", str(kpis['total_campaigns']),       "Campaigns"),
    kpi_card("✅", f"{kpis['positive_responses']:,}", "Positive Responses"),
    kpi_card("📈", f"{kpis['response_rate']:.2f}%",  "Acceptance Rate"),
    kpi_card("💰", f"${kpis['average_income']:,.0f}", "Avg Income"),
    kpi_card("🛒", f"${kpis['average_spending']:,.0f}","Avg Spending"),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── ROW 1: Campaign chart + Spend donut ───────────────────────────────────────
st.markdown(section_header("📈", "Campaign Performance vs Spending Breakdown",
            "How each wave converted and where customers spend their money."), unsafe_allow_html=True)

r1a, r1b = st.columns([3, 2])
camp_analysis = analyze_campaign_performance(df_f)
with r1a:
    st.plotly_chart(plot_campaign_comparison(camp_analysis["summary_table"]),
                    use_container_width=True)
with r1b:
    spend_df = compute_category_spend_breakdown(df_f)
    st.plotly_chart(plot_spend_donut(spend_df), use_container_width=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── ROW 2: Channels + Scatter ─────────────────────────────────────────────────
st.markdown(section_header("🛍️", "Purchase Channels & Income–Spend Correlation",
            "Where customers buy and how income drives spending behaviour."), unsafe_allow_html=True)

r2a, r2b = st.columns([2, 3])
with r2a:
    channel_df = compute_purchase_channel_breakdown(df_f)
    st.plotly_chart(plot_channel_comparison(channel_df), use_container_width=True)
with r2b:
    st.plotly_chart(plot_income_vs_spending(df_f), use_container_width=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── CAMPAIGN TABLE + PROGRESS BARS ───────────────────────────────────────────
st.markdown(section_header("📋", "Detailed Campaign Conversion Summary"), unsafe_allow_html=True)
tb_col, prog_col = st.columns([3, 2])

with tb_col:
    st.dataframe(
        camp_analysis["summary_table"].style.format({
            "Customers_Contacted": "{:,}",
            "Positive_Responses": "{:,}",
            "Response_Rate": "{:.2f}%"
        }),
        use_container_width=True, hide_index=True
    )

with prog_col:
    st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.8rem;'>"
                "Campaign Acceptance Rates</p>", unsafe_allow_html=True)
    colors = ["#3B82F6","#0D9488","#8B5CF6","#F59E0B","#EC4899","#10B981"]
    for i, row in camp_analysis["summary_table"].iterrows():
        c = colors[i % len(colors)]
        st.markdown(
            animated_progress(row["Campaign_Name"].split("(")[0].strip(),
                              float(row["Response_Rate"]), c),
            unsafe_allow_html=True
        )
