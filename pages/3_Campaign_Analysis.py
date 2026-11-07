"""
MARKETIX Module 3: Campaign Performance Analysis — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, kpi_card, kpi_grid, animated_progress
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.campaign_analysis import analyze_campaign_performance, analyze_channel_performance
from src.visualizations import plot_campaign_comparison, plot_channel_comparison
import plotly.express as px

st.set_page_config(page_title="Campaign Analysis | MARKETIX", page_icon="📈", layout="wide")
inject_styles()

if "cleaned_df" not in st.session_state or st.session_state["cleaned_df"] is None:
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        st.session_state["cleaned_df"] = df_clean

df = st.session_state.get("cleaned_df")
if df is None:
    st.warning("⚠️ No dataset loaded. Please go to Data Management.")
    st.stop()

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='animation:fadeSlideDown 0.5s ease both;'>
<h1 style='margin:0;font-size:1.9rem;font-weight:900;color:#0F172A;'>
📈 Campaign Performance Analysis
</h1>
<p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
Comparative benchmarking across all 6 marketing campaigns and purchase acquisition channels.
</p>
</div>
""", unsafe_allow_html=True)

# Run Campaign Analysis
camp_results = analyze_campaign_performance(df)
summary_table = camp_results["summary_table"]
best_cmp = camp_results["best_campaign"]

# ── TOP KPI GRID ─────────────────────────────────────────────────────────────
st.markdown(kpi_grid(
    kpi_card("🏆", best_cmp['name'].split("(")[0].strip() if best_cmp else "N/A", "Top Campaign", f"{best_cmp['response_rate']:.1f}% conversion" if best_cmp else ""),
    kpi_card("🎯", f"{best_cmp['responses']:,}" if best_cmp else "0", "Top Conversions"),
    kpi_card("👥", f"{camp_results['total_contacted']:,}", "Customers Reached"),
    kpi_card("📊", f"{len(summary_table)}", "Campaign Waves"),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── FORMULA & BANNER ROW ─────────────────────────────────────────────────────
col_ban, col_form = st.columns([3, 2])
with col_ban:
    if best_cmp:
        st.markdown(f"""
<div style='background:linear-gradient(135deg, #ECFDF5, #D1FAE5);border-radius:14px;padding:1.4rem;border:1px solid #34D399;box-shadow:0 4px 15px rgba(16,185,129,0.1);animation:floatUp 0.5s ease both;'>
<div style='font-size:1.15rem;font-weight:800;color:#065F46;margin-bottom:0.4rem;'>
🏆 Benchmark Winner: {best_cmp['name']}
</div>
<div style='color:#047857;font-size:0.88rem;line-height:1.5;'>
Achieved the highest conversion rate at <b>{best_cmp['response_rate']:.2f}%</b>, securing <b>{best_cmp['responses']:,} positive conversions</b> out of {camp_results['total_contacted']:,} targeted customers.
</div>
</div>
""", unsafe_allow_html=True)

with col_form:
    st.markdown("""
<div style='background:white;border-radius:14px;padding:1.3rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.03);animation:floatUp 0.6s ease both;'>
<div style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.4rem;'>Mathematical Formulation</div>
<div style='font-size:0.78rem;color:#64748B;margin-bottom:0.6rem;'>Tracking efficiency of targeted conversion:</div>
""", unsafe_allow_html=True)
    st.latex(r"\text{Response Rate} = \frac{\text{Positive Responses}}{\text{Customers Contacted}} \times 100")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── CHARTS ROW ───────────────────────────────────────────────────────────────
st.markdown(section_header("📊", "Campaign Acceptance Comparison", "Visual comparison of conversion rates across waves"), unsafe_allow_html=True)
c_left, c_right = st.columns([3, 2])

with c_left:
    fig_cmp = plot_campaign_comparison(summary_table)
    st.plotly_chart(fig_cmp, width="stretch")

with c_right:
    st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.5rem;'>Campaign Metrics Table</p>", unsafe_allow_html=True)
    st.dataframe(
        summary_table[["Campaign_Name", "Positive_Responses", "Response_Rate"]].rename(
            columns={"Positive_Responses": "Responses", "Response_Rate": "Acceptance %"}
        ),
        width="stretch",
        hide_index=True
    )

st.markdown(divider(), unsafe_allow_html=True)

# ── SECONDARY ANALYTICS ROW ──────────────────────────────────────────────────
st.markdown(section_header("🛍️", "Multi-Wave Loyalty & Channel Acquisition"), unsafe_allow_html=True)
c_row1, c_row2 = st.columns(2)

with c_row1:
    st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.5rem;'>Repeat Campaign Loyalty</p>", unsafe_allow_html=True)
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
            color_continuous_scale="Teal",
            template="plotly_white"
        )
        fig_eng.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_eng.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=40))
        st.plotly_chart(fig_eng, width="stretch")

with c_row2:
    st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.5rem;'>Purchases by Acquisition Channel</p>", unsafe_allow_html=True)
    chan_df = analyze_channel_performance(df)
    fig_chan = plot_channel_comparison(chan_df)
    st.plotly_chart(fig_chan, width="stretch")
