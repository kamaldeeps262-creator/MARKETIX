"""
MARKETIX: An Intelligent Marketing Analytics and Customer Insights Platform
Main Application Entry Point
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Ensure MARKETIX root is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.connection import get_db_status, init_db
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.analytics import compute_kpis

# Page configuration
st.set_page_config(
    page_title="MARKETIX - Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-online { background-color: #DCFCE7; color: #166534; }
    .status-fallback { background-color: #FEF3C7; color: #92400E; }
    .status-offline { background-color: #FEE2E2; color: #991B1B; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_cached_data():
    """Loads and cleans the default marketing dataset once."""
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        return df_clean, report
    return None, None


# Session State Management
if "cleaned_df" not in st.session_state:
    df_clean, rep = get_cached_data()
    st.session_state["cleaned_df"] = df_clean
    st.session_state["clean_report"] = rep

# Sidebar
with st.sidebar:
    logo_path = ROOT_DIR / "assets" / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.title("📊 MARKETIX")
    
    st.markdown("---")
    st.subheader("System Infrastructure")
    
    # Live Database Health Indicator
    db_status = get_db_status()
    if db_status.get("is_postgres"):
        st.markdown(f'<span class="status-badge status-online">● PostgreSQL Active</span>', unsafe_allow_html=True)
        st.caption(f"Host: localhost:5432 | DB: marketix")
    elif db_status.get("connected"):
        st.markdown(f'<span class="status-badge status-fallback">● Local SQLite Active</span>', unsafe_allow_html=True)
        st.caption("PostgreSQL daemon inactive; running seamlessly on local SQLite engine.")
    else:
        st.markdown(f'<span class="status-badge status-offline">● DB Disconnected</span>', unsafe_allow_html=True)
        st.error(db_status.get("message", "Database connection failed."))

    st.markdown("---")
    st.markdown("### Industrial Alignment")
    st.markdown("""
    - **BCG X:** Marketing Decision Analytics
    - **IBM:** Data Analysis with Python
    - **Deloitte:** Business Simulation & Insights
    """)
    st.caption("B.Tech 3rd-Year Industrial Training Project")


# Header Banner
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 800;">MARKETIX</h1>
    <h3 style="margin-top:0.3rem; font-weight: 400; color: #93C5FD; font-size: 1.15rem;">
        An Intelligent Marketing Analytics and Customer Insights Platform
    </h3>
    <p style="margin-top:0.8rem; font-size: 0.95rem; color: #E2E8F0; max-width: 900px;">
        Empowering organizations to evaluate multi-channel marketing campaigns, decode customer purchasing patterns, 
        cluster customer personas with unsupervised Machine Learning, and predict individual campaign conversion likelihoods.
    </p>
</div>
""", unsafe_allow_html=True)

# Overview Metrics Glance
df_active = st.session_state.get("cleaned_df")
if df_active is not None:
    kpis = compute_kpis(df_active)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.metric("Total Customers", f"{kpis['total_customers']:,}")
    with c2:
        st.metric("Campaigns Analyzed", f"{kpis['total_campaigns']}")
    with c3:
        st.metric("Positive Responses", f"{kpis['positive_responses']:,}")
    with c4:
        st.metric("Acceptance Rate", f"{kpis['response_rate']:.2f}%")
    with c5:
        st.metric("Average Income", f"${kpis['average_income']:,.0f}")
    with c6:
        st.metric("Average Spending", f"${kpis['average_spending']:,.0f}")

st.markdown("---")

# Navigation & Architecture
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Platform Architecture & Modules")
    st.markdown("""
    MARKETIX is engineered following a clean **Layered Enterprise Architecture**:
    
    1. **📊 Module 1: Dashboard** - High-level executive KPIs, conversion benchmarks, and spend patterns.
    2. **📁 Module 2: Data Management** - Dataset ingestion (CSV/Excel), schema validation, and missing value imputation.
    3. **📈 Module 3: Campaign Performance** - Detailed comparison across marketing campaigns and purchase channels.
    4. **🔍 Module 4: Customer Insights** - Demographic distributions, spending tiers, and product affinity analysis.
    5. **🎯 Module 5: Customer Segmentation** - Unsupervised K-Means clustering, elbow curves, and persona profiles.
    6. **🤖 Module 6: Campaign Response Prediction** - Supervised Logistic Regression model with interactive inference & ROC evaluation.
    7. **💡 Module 7: Business Recommendations** - Rule-based consulting suggestions distinguishing correlation from causation.
    8. **📑 Module 8: Reports & Downloads** - PDF executive summary generation and CSV dataset exports.
    """)

with col_right:
    st.subheader("Quick System Health")
    with st.container(border=True):
        st.markdown("**Data Engine Status**")
        if df_active is not None:
            st.success(f"✓ Active Dataset: {len(df_active)} records loaded & preprocessed.")
        else:
            st.warning("No dataset loaded. Upload via Module 2.")
            
        st.markdown("**Database Synchronization**")
        st.info(f"Database Type: **{db_status.get('type', 'Unknown')}**")
        
        st.markdown("**Machine Learning Status**")
        from ml.evaluate import get_model_status
        ml_stat = get_model_status()
        if ml_stat.get("trained"):
            st.success(f"✓ Model: Logistic Regression ({ml_stat.get('version')}) | AUC: {ml_stat.get('metrics', {}).get('roc_auc', 0.90):.3f}")
        else:
            st.warning("Model ready to train from Module 6.")

    st.markdown("👉 *Select any module from the left navigation sidebar to explore.*")
