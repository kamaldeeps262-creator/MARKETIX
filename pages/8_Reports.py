"""
MARKETIX Module 8: Reports & Exports — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, kpi_card, kpi_grid
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.analytics import compute_kpis
from src.campaign_analysis import analyze_campaign_performance
from src.recommendations import generate_recommendations
from reports.generator import generate_pdf_report

st.set_page_config(page_title="Reports | MARKETIX", page_icon="📑", layout="wide")
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
📑 Reports & Analytical Exports
</h1>
<p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
Generate high-resolution executive PDF briefs and export structured analytical datasets.
</p>
</div>
""", unsafe_allow_html=True)

kpis = compute_kpis(df)
camp_results = analyze_campaign_performance(df)
recs = generate_recommendations(df, campaign_summary=camp_results)

# ── KPI METRICS CARDS ─────────────────────────────────────────────────────────
st.markdown(kpi_grid(
    kpi_card("📄", "PDF Executive Brief", "Format: Vector PDF"),
    kpi_card("📊", "4 CSV Datasets", "Ready for Export"),
    kpi_card("👥", f"{kpis['total_customers']:,}", "Audited Records"),
    kpi_card("💼", "Consulting Ready", "BCG X & Deloitte"),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── 1. EXECUTIVE PDF SECTION ─────────────────────────────────────────────────
st.markdown(section_header("📄", "Official Executive PDF Brief (ReportLab Engine)"), unsafe_allow_html=True)

with st.container():
    st.markdown("""
<div style='background:linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);border-radius:16px;padding:2rem;color:white;margin-bottom:1.2rem;box-shadow:0 8px 30px rgba(30,58,138,0.25);animation:floatUp 0.5s ease both;'>
<div style='display:flex;align-items:center;gap:1rem;margin-bottom:0.8rem;'>
<div style='font-size:2rem;'>🏛️</div>
<div>
<div style='font-size:1.3rem;font-weight:800;'>MARKETIX Executive Marketing Intelligence Brief</div>
<div style='color:#93C5FD;font-size:0.85rem;'>Automated ReportLab compilation · Formatted for corporate supervisors and academic evaluators</div>
</div>
</div>
<div style='color:#E2E8F0;font-size:0.88rem;line-height:1.6;margin-bottom:1.2rem;'>
Contains formal performance indicator tables, multi-wave campaign conversion benchmarks, top customer segment characteristics, and prioritized strategic initiatives distinguishing empirical correlation from causality.
</div>
</div>
""", unsafe_allow_html=True)

    with st.spinner("Compiling high-resolution vector PDF..."):
        pdf_bytes = generate_pdf_report(
            metrics=kpis,
            campaign_summary=camp_results["summary_table"],
            recommendations=recs
        )

    st.download_button(
        label="📥  Download Official Executive PDF Report",
        data=pdf_bytes,
        file_name="MARKETIX_Executive_Marketing_Report.pdf",
        mime="application/pdf",
        type="primary",
        width="stretch"
    )

st.markdown(divider(), unsafe_allow_html=True)

# ── 2. CSV EXPORT CARDS ──────────────────────────────────────────────────────
st.markdown(section_header("📊", "Structured CSV Data Exports"), unsafe_allow_html=True)

exp_c1, exp_c2 = st.columns(2)
with exp_c1:
    st.markdown(f"""
<div style='background:white;border-radius:14px;padding:1.4rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.04);margin-bottom:1rem;animation:floatUp 0.5s ease both;'>
<div style='font-size:1.1rem;font-weight:700;color:#0F172A;margin-bottom:0.3rem;'>🧹 Cleaned Marketing Dataset</div>
<div style='font-size:0.8rem;color:#64748B;margin-bottom:0.8rem;'>
Includes imputed income, normalized categoricals, and engineered domain KPIs (<code>Total_Spending</code>, <code>Total_Purchases</code>, <code>Children</code>).<br>
<b>Size:</b> {len(df):,} records · {df.shape[1]} features
</div>
</div>
""", unsafe_allow_html=True)
    csv_clean = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Cleaned Dataset (CSV)", data=csv_clean, file_name="marketix_cleaned_dataset.csv", mime="text/csv", width="stretch")

with exp_c2:
    st.markdown(f"""
<div style='background:white;border-radius:14px;padding:1.4rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.04);margin-bottom:1rem;animation:floatUp 0.6s ease both;'>
<div style='font-size:1.1rem;font-weight:700;color:#0F172A;margin-bottom:0.3rem;'>📈 Campaign Performance Summary</div>
<div style='font-size:0.8rem;color:#64748B;margin-bottom:0.8rem;'>
Aggregated conversion metrics, contacts, and response percentages across all 6 evaluated campaign waves.<br>
<b>Waves:</b> {len(camp_results['summary_table'])} campaigns evaluated
</div>
</div>
""", unsafe_allow_html=True)
    csv_camp = camp_results["summary_table"].to_csv(index=False).encode("utf-8")
    st.download_button("Download Campaign Summary (CSV)", data=csv_camp, file_name="marketix_campaign_performance.csv", mime="text/csv", width="stretch")

exp_c3, exp_c4 = st.columns(2)
with exp_c3:
    seg_df = st.session_state.get("segmented_df")
    seg_text = f"<b>Personas:</b> {seg_df['Cluster'].nunique()} clusters identified" if seg_df is not None else "Run Module 5 to generate segmentation."
    st.markdown(f"""
<div style='background:white;border-radius:14px;padding:1.4rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.04);margin-bottom:1rem;animation:floatUp 0.7s ease both;'>
<div style='font-size:1.1rem;font-weight:700;color:#0F172A;margin-bottom:0.3rem;'>🎯 Customer Segmentation Personas</div>
<div style='font-size:0.8rem;color:#64748B;margin-bottom:0.8rem;'>
K-Means cluster assignments, standardized features, and assigned marketing personas.<br>
{seg_text}
</div>
</div>
""", unsafe_allow_html=True)
    if seg_df is not None:
        csv_seg = seg_df[["ID", "Cluster", "Segment_Name", "Income", "Total_Spending", "Total_Purchases"]].to_csv(index=False).encode("utf-8")
        st.download_button("Download Customer Segments (CSV)", data=csv_seg, file_name="marketix_customer_segments.csv", mime="text/csv", width="stretch")
    else:
        st.info("Run Customer Segmentation (Module 5) first to enable this export.")

with exp_c4:
    score_df = st.session_state.get("scored_df")
    score_text = f"<b>Scored:</b> {len(score_df):,} leads scored with Logistic Regression" if score_df is not None else "Run Batch Scoring in Module 6 to generate predictions."
    st.markdown(f"""
<div style='background:white;border-radius:14px;padding:1.4rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.04);margin-bottom:1rem;animation:floatUp 0.8s ease both;'>
<div style='font-size:1.1rem;font-weight:700;color:#0F172A;margin-bottom:0.3rem;'>🤖 Scored Campaign Prospects</div>
<div style='font-size:0.8rem;color:#64748B;margin-bottom:0.8rem;'>
Probabilities and binary propensity conversion predictions for targeted marketing execution.<br>
{score_text}
</div>
</div>
""", unsafe_allow_html=True)
    if score_df is not None:
        csv_pred = score_df[["ID", "Income", "Total_Spending", "Predicted_Probability", "Predicted_Response"]].to_csv(index=False).encode("utf-8")
        st.download_button("Download Scored Prospects (CSV)", data=csv_pred, file_name="marketix_scored_predictions.csv", mime="text/csv", width="stretch")
    else:
        st.info("Run Batch Scoring in Response Prediction (Module 6) first to enable this export.")
