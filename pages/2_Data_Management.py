"""
MARKETIX Module 2: Data Upload & Management — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, kpi_card, kpi_grid
from src.data_loader import load_dataset, get_dataset_summary
from src.data_cleaning import clean_marketing_data
from database.queries import sync_processed_data_to_db, log_upload
from database.connection import get_db_status

st.set_page_config(page_title="Data Management | MARKETIX", page_icon="📁", layout="wide")
inject_styles()

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='animation:fadeSlideDown 0.5s ease both;'>
    <h1 style='margin:0;font-size:1.9rem;font-weight:900;color:#0F172A;'>
        📁 Data Upload & Management
    </h1>
    <p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
        Ingest marketing files, inspect schema quality, identify anomalies, and execute automated data cleaning.
    </p>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOADER ─────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Choose a marketing dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
    help="Upload your campaign performance or customer personality analysis dataset."
)

if uploaded_file is not None:
    df_raw, msg = load_dataset(uploaded_file)
    st.session_state["raw_df"] = df_raw
    st.session_state["current_file_name"] = uploaded_file.name
    st.success(f"✓ {msg}")
else:
    if "raw_df" not in st.session_state or st.session_state["raw_df"] is None:
        df_raw, msg = load_dataset()
        st.session_state["raw_df"] = df_raw
        st.session_state["current_file_name"] = "marketing_campaign.csv (Default)"

df_raw = st.session_state.get("raw_df")
if df_raw is None:
    st.error("Failed to load dataset. Please check the file format.")
    st.stop()

# ── KPI METRICS CARDS ─────────────────────────────────────────────────────────
summary = get_dataset_summary(df_raw)
missing_count = sum(summary["missing_values"].values())
dup_count = summary["duplicate_rows"]

st.markdown(kpi_grid(
    kpi_card("📊", f"{summary['total_rows']:,}", "Total Records"),
    kpi_card("🏷️", str(summary['total_columns']), "Features"),
    kpi_card("⚠️", f"{missing_count:,}", "Missing Values", f"{len(summary['missing_values'])} columns affected" if missing_count else "Clean"),
    kpi_card("👥", f"{dup_count:,}", "Duplicates", "0 duplicate rows" if dup_count == 0 else f"{dup_count} duplicate rows"),
    kpi_card("💾", f"{summary['memory_mb']:.1f} MB", "Memory Usage"),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📋  Data Preview",
    "🔍  Schema & Anomaly Profiler",
    "🧹  Data Cleaning & Database Sync"
])

with tab1:
    st.markdown(section_header("📋", "Raw Dataset Snapshot", f"Showing first 15 records from {st.session_state.get('current_file_name')}"), unsafe_allow_html=True)
    st.dataframe(df_raw.head(15), width="stretch")

with tab2:
    st.markdown(section_header("🔍", "Data Hygiene & Anomaly Inspection"), unsafe_allow_html=True)
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.4rem;'>Missing Values Table</p>", unsafe_allow_html=True)
        if summary["missing_values"]:
            missing_df = pd.DataFrame([
                {"Column": col, "Missing Count": count, "Missing %": round((count / summary['total_rows']) * 100, 2)}
                for col, count in summary["missing_values"].items()
            ])
            st.dataframe(missing_df, width="stretch", hide_index=True)
            st.warning("⚠️ **Income column contains nulls.** Our pipeline implements education-stratified median imputation to preserve demographic relationships.")
        else:
            st.success("✅ No missing values detected in the dataset!")

    with c_p2:
        st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.4rem;'>Schema & Types</p>", unsafe_allow_html=True)
        schema_df = pd.DataFrame([{"Feature": k, "Type": v} for k, v in summary["dtypes"].items()])
        st.dataframe(schema_df, width="stretch", height=280, hide_index=True)

with tab3:
    st.markdown(section_header("🧹", "Automated Data Cleaning Pipeline", "Applies median imputation, anomaly normalization, and KPI feature engineering"), unsafe_allow_html=True)

    st.markdown("""
<div style='background:white;border-radius:12px;padding:1.2rem;border:1px solid #E2E8F0;box-shadow:0 2px 10px rgba(0,0,0,0.03);margin-bottom:1rem;'>
    <h4 style='margin:0 0 0.5rem;color:#1E3A8A;'>Pipeline Operations</h4>
    <ol style='margin:0;padding-left:1.2rem;color:#475569;font-size:0.85rem;line-height:1.6;'>
        <li><b>Education-Stratified Median Imputation:</b> Missing Income records are imputed using the median income of the customer's specific education group.</li>
        <li><b>Chronological Outlier Capping:</b> Detects birth years &lt; 1920 (Age &gt; 100) and caps them to median demographic cohort age.</li>
        <li><b>Categorical Normalization:</b> Converts anomalous marital entries (<code>Alone</code>, <code>Absurd</code>, <code>YOLO</code>) into standard <code>Single</code> category.</li>
        <li><b>Domain Feature Engineering:</b> Calculates <code>Total_Spending</code>, <code>Total_Purchases</code>, <code>Children</code>, <code>Is_Parent</code>, and <code>Customer_Tenure_Days</code>.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

    if st.button("🚀  Execute Data Cleaning & Synchronize to Database", type="primary", width="stretch"):
        with st.spinner("Processing records and syncing with database engine..."):
            df_cleaned, report = clean_marketing_data(df_raw)
            st.session_state["cleaned_df"] = df_cleaned
            st.session_state["clean_report"] = report

            file_name = st.session_state.get("current_file_name", "dataset.csv")
            log_upload(file_name, len(df_cleaned), status="Processed")
            ok_sync, msg_sync = sync_processed_data_to_db(df_cleaned)

            st.success("🎉 Data cleaning successfully executed and synchronized!")

            st.markdown(kpi_grid(
                kpi_card("🛠️", str(report.get("missing_income_imputed", 0)), "Income Imputed"),
                kpi_card("🎯", str(report.get("outliers_adjusted", 0)), "Age Outliers Capped"),
                kpi_card("🔄", str(report.get("marital_status_normalized", 0)), "Status Normalized"),
                kpi_card("✨", str(report.get("final_columns", 0) - report.get("initial_columns", 0)), "New Features Added"),
            ), unsafe_allow_html=True)

            if ok_sync:
                st.info(f"💾 {msg_sync}")
            else:
                st.warning(f"Database note: {msg_sync}")

    df_clean_active = st.session_state.get("cleaned_df")
    if df_clean_active is not None:
        st.markdown(divider(), unsafe_allow_html=True)
        st.markdown(section_header("📥", "Export Cleaned Data"), unsafe_allow_html=True)
        csv_data = df_clean_active.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥  Download Cleaned Dataset (CSV)",
            data=csv_data,
            file_name="MARKETIX_Cleaned_Marketing_Dataset.csv",
            mime="text/csv",
            width="stretch"
        )
