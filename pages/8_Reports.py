"""
MARKETIX Module 8: Reports & Exports
Comprehensive data export and professional PDF report generation facility.
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
from src.analytics import compute_kpis
from src.campaign_analysis import analyze_campaign_performance
from src.recommendations import generate_recommendations
from reports.generator import generate_pdf_report

st.set_page_config(page_title="Reports | MARKETIX", page_icon="📑", layout="wide")

st.title("📑 Reports & Analytical Exports")
st.caption("Generate downloadable executive summary reports and export cleaned analytical datasets.")

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

kpis = compute_kpis(df)
camp_results = analyze_campaign_performance(df)
recs = generate_recommendations(df, campaign_summary=camp_results)

# 1. Executive PDF Generation Section
st.subheader("📄 Executive Summary PDF Report")
st.markdown("""
Generates a formal, high-resolution analytical brief formatted for presentation
to stakeholders, academic reviewers, and corporate supervisors.
Includes KPIs, campaign conversion tables, and strategic recommendations.
""")

with st.spinner("Compiling executive PDF report..."):
    pdf_bytes = generate_pdf_report(
        metrics=kpis,
        campaign_summary=camp_results["summary_table"],
        recommendations=recs
    )

st.download_button(
    label="📥 Download Official Executive PDF Report",
    data=pdf_bytes,
    file_name="MARKETIX_Executive_Marketing_Report.pdf",
    mime="application/pdf",
    type="primary"
)

st.markdown("---")

# 2. Data Exports in CSV format
st.subheader("📊 Structured CSV Exports")
st.markdown("Export cleansed datasets and analytical results for downstream consumption.")

exp_c1, exp_c2 = st.columns(2)

with exp_c1:
    with st.container(border=True):
        st.markdown("#### Cleaned Marketing Dataset")
        st.markdown(f"**Records:** `{len(df):,}` rows | **Columns:** `{df.shape[1]}` features")
        csv_clean = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned Dataset (CSV)", data=csv_clean, file_name="marketix_cleaned_dataset.csv", mime="text/csv")

    with exp_c2:
        with st.container(border=True):
            st.markdown("#### Campaign Performance Summary")
            st.markdown(f"**Campaigns:** `{len(camp_results['summary_table'])}` campaigns evaluated")
            csv_camp = camp_results["summary_table"].to_csv(index=False).encode("utf-8")
            st.download_button("Download Campaign Summary (CSV)", data=csv_camp, file_name="marketix_campaign_performance.csv", mime="text/csv")

exp_c3, exp_c4 = st.columns(2)

with exp_c3:
    with st.container(border=True):
        st.markdown("#### Customer Segmentation Clusters")
        seg_df = st.session_state.get("segmented_df")
        if seg_df is not None:
            csv_seg = seg_df[["ID", "Cluster", "Segment_Name", "Income", "Total_Spending", "Total_Purchases"]].to_csv(index=False).encode("utf-8")
            st.download_button("Download Segmentation CSV", data=csv_seg, file_name="marketix_customer_segments.csv", mime="text/csv")
        else:
            st.caption("Run Customer Segmentation (Module 5) to enable cluster export.")

with exp_c4:
    with st.container(border=True):
        st.markdown("#### Model Scored Prospect Predictions")
        score_df = st.session_state.get("scored_df")
        if score_df is not None:
            csv_pred = score_df[["ID", "Income", "Total_Spending", "Predicted_Probability", "Predicted_Response"]].to_csv(index=False).encode("utf-8")
            st.download_button("Download Scored Predictions CSV", data=csv_pred, file_name="marketix_scored_predictions.csv", mime="text/csv")
        else:
            st.caption("Run Batch Scoring in Module 6 to enable propensity score export.")
