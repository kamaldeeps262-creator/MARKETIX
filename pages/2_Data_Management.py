"""
MARKETIX Module 2: Data Upload & Management
Handles dataset ingestion (CSV/Excel), schema profiling, missing value detection,
anomalous record identification, automated data cleaning, and database persistence.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_loader import load_dataset, get_dataset_summary
from src.data_cleaning import clean_marketing_data
from database.queries import sync_processed_data_to_db, log_upload
from database.connection import get_db_status

st.set_page_config(page_title="Data Management | MARKETIX", page_icon="📁", layout="wide")

st.title("📁 Data Upload & Management")
st.caption("Upload marketing datasets, inspect data hygiene, identify anomalies, and apply data engineering.")

# File Uploader
uploaded_file = st.file_uploader(
    "Choose a marketing dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
    help="Upload your campaign performance or customer personality analysis dataset."
)

# Load Data logic
if uploaded_file is not None:
    df_raw, msg = load_dataset(uploaded_file)
    st.session_state["raw_df"] = df_raw
    st.session_state["current_file_name"] = uploaded_file.name
    st.success(f"✓ {msg}")
else:
    if "raw_df" not in st.session_state or st.session_state["raw_df"] is None:
        df_raw, msg = load_dataset() # load default marketing_campaign.csv
        st.session_state["raw_df"] = df_raw
        st.session_state["current_file_name"] = "marketing_campaign.csv (Default)"
        st.info(f"Loaded default dataset: {msg}")

df_raw = st.session_state.get("raw_df")

if df_raw is None:
    st.error("Failed to load dataset. Please check the file format.")
    st.stop()

# Profiling Summary
summary = get_dataset_summary(df_raw)

# Overview Badges
b1, b2, b3, b4 = st.columns(4)
with b1:
    st.metric("Total Records", f"{summary['total_rows']:,}")
with b2:
    st.metric("Total Features", f"{summary['total_columns']}")
with b3:
    missing_count = sum(summary["missing_values"].values())
    st.metric("Missing Values", f"{missing_count:,}", delta=f"{len(summary['missing_values'])} columns affected", delta_color="inverse")
with b4:
    dup_count = summary["duplicate_rows"]
    st.metric("Duplicate Rows", f"{dup_count:,}", delta="No duplicates" if dup_count == 0 else "Duplicates detected", delta_color="inverse")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "🔍 Schema & Data Quality Profiler", "🧹 Data Cleaning & Preprocessing"])

with tab1:
    st.subheader("Raw Dataset Preview")
    st.dataframe(df_raw.head(15), use_container_width=True)

with tab2:
    st.subheader("Quality Profiler & Anomaly Detection")
    col_prof1, col_prof2 = st.columns(2)
    
    with col_prof1:
        st.markdown("**Missing Value Breakdown**")
        if summary["missing_values"]:
            missing_df = pd.DataFrame([
                {"Column": col, "Missing Count": count, "Missing %": round((count / summary['total_rows']) * 100, 2)}
                for col, count in summary["missing_values"].items()
            ])
            st.dataframe(missing_df, use_container_width=True, hide_index=True)
            st.warning("⚠️ Income has missing records. In industrial analytics, median imputation conditioned on Education level preserves demographic fidelity.")
        else:
            st.success("✓ No missing values detected in the raw dataset.")

    with col_prof2:
        st.markdown("**Column Schema & Data Types**")
        schema_df = pd.DataFrame([
            {"Column Name": col, "Data Type": dtype}
            for col, dtype in summary["dtypes"].items()
        ])
        st.dataframe(schema_df, use_container_width=True, height=280, hide_index=True)

with tab3:
    st.subheader("Automated Data Cleaning Pipeline")
    st.markdown("""
    The automated cleaning pipeline performs:
    1. **Education-Stratified Median Imputation** for missing Income values.
    2. **Demographic Outlier Capping** for abnormal birth years (Ages > 100).
    3. **Categorical Normalization** for non-standard marital statuses ('Alone', 'Absurd', 'YOLO' → 'Single').
    4. **Feature Engineering** for domain KPIs: `Total_Spending`, `Total_Purchases`, `Children`, and `Customer_Tenure_Days`.
    """)

    if st.button("🚀 Execute Data Cleaning & Sync to Database", type="primary"):
        with st.spinner("Processing dataset and synchronizing with database..."):
            df_cleaned, report = clean_marketing_data(df_raw)
            st.session_state["cleaned_df"] = df_cleaned
            st.session_state["clean_report"] = report

            # Sync to Database
            file_name = st.session_state.get("current_file_name", "dataset.csv")
            log_upload(file_name, len(df_cleaned), status="Processed")
            ok_sync, msg_sync = sync_processed_data_to_db(df_cleaned)

            st.success("🎉 Data cleaning successfully executed!")
            
            # Display report
            rep_col1, rep_col2, rep_col3, rep_col4 = st.columns(4)
            with rep_col1:
                st.metric("Income Values Imputed", report.get("missing_income_imputed", 0))
            with rep_col2:
                st.metric("Age Outliers Adjusted", report.get("outliers_adjusted", 0))
            with rep_col3:
                st.metric("Marital Status Normalized", report.get("marital_status_normalized", 0))
            with rep_col4:
                st.metric("Engineered Features Added", report.get("final_columns", 0) - report.get("initial_columns", 0))

            if ok_sync:
                st.info(f"💾 Database Sync: {msg_sync}")
            else:
                st.warning(f"Database Notice: {msg_sync}")

    # Download Cleaned Data
    df_clean_active = st.session_state.get("cleaned_df")
    if df_clean_active is not None:
        st.markdown("---")
        st.subheader("📥 Export Cleaned Dataset")
        csv_data = df_clean_active.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Cleaned CSV Dataset",
            data=csv_data,
            file_name="MARKETIX_Cleaned_Marketing_Dataset.csv",
            mime="text/csv",
            type="secondary"
        )
