"""
MARKETIX: Main Application Entry Point — Redesigned with animations & modern UI
"""

import streamlit as st
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.connection import get_db_status, init_db
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.analytics import compute_kpis
from src.styles import (inject_styles, kpi_card, kpi_grid, hero_banner,
                         module_card, health_row, status_pill, divider)

st.set_page_config(
    page_title="MARKETIX – Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_styles()


@st.cache_data
def get_cached_data():
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, report = clean_marketing_data(df_raw)
        return df_clean, report
    return None, None


if "cleaned_df" not in st.session_state:
    df_clean, rep = get_cached_data()
    st.session_state["cleaned_df"] = df_clean
    st.session_state["clean_report"] = rep

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = ROOT_DIR / "assets" / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width="stretch")
    else:
        st.markdown("<h2 style='color:#0F172A;margin:0;'>📊 MARKETIX</h2>", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #E2E8F0;margin:1rem 0;'>", unsafe_allow_html=True)

    db_status = get_db_status()
    if db_status.get("is_postgres"):
        kind, label = "success", "PostgreSQL Connected"
        dot, db_desc = "green", "localhost:5432 · marketix"
    elif db_status.get("connected"):
        kind, label = "warning", "SQLite Fallback Active"
        dot, db_desc = "yellow", "PostgreSQL offline – local embedded DB"
    else:
        kind, label = "danger", "No Database"
        dot, db_desc = "red", "Check configuration"

    from ml.evaluate import get_model_status
    ml_stat = get_model_status()
    auc_val  = ml_stat.get("metrics", {}).get("roc_auc", 0.0)
    ml_color = "green" if ml_stat.get("trained") else "yellow"
    ml_label = f"Model Trained · AUC {auc_val:.3f}" if ml_stat.get("trained") else "Model not trained yet"

    df_active = st.session_state.get("cleaned_df")
    data_color = "green" if df_active is not None else "yellow"
    data_label = f"{len(df_active):,} records active" if df_active is not None else "No data loaded"

    st.markdown(
        health_row(dot, label, db_desc) +
        health_row(data_color, "Data Engine", data_label) +
        health_row(ml_color, "ML Pipeline", ml_label),
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border:none;border-top:1px solid #E2E8F0;margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
<div style='background:white;border-radius:10px;padding:0.9rem;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.02);'>
<p style='color:#64748B;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin:0 0 0.5rem;'>
Certificate Alignment
</p>
<p style='color:#334155;font-size:0.8rem;line-height:1.7;margin:0;'>
🔵 <b style='color:#1E40AF;'>BCG X</b> — Decision Analytics<br>
🟣 <b style='color:#7C3AED;'>IBM</b> — Data Analysis · Python<br>
🟢 <b style='color:#059669;'>Deloitte</b> — Business Simulation
</p>
<p style='color:#94A3B8;font-size:0.72rem;margin:0.6rem 0 0;'>B.Tech 3rd-Year · Industrial Training</p>
</div>
""", unsafe_allow_html=True)

# ── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown(hero_banner(
    title="MARKETIX",
    subtitle="An Intelligent Marketing Analytics & Customer Insights Platform",
    description=(
        "Empowering marketing teams to benchmark multi-wave campaign performance, uncover customer behaviour patterns, "
        "cluster customer personas with K-Means, and predict individual campaign conversion likelihoods with Logistic Regression — "
        "all in one unified, real-time intelligence platform."
    ),
    badges=["Python 3.13", "Streamlit", "Scikit-Learn", "PostgreSQL", "ReportLab",
            "Plotly", "Pandas", "NumPy", "SQLAlchemy"]
), unsafe_allow_html=True)

# ── KPI OVERVIEW ─────────────────────────────────────────────────────────────
if df_active is not None:
    kpis = compute_kpis(df_active)
    st.markdown(kpi_grid(
        kpi_card("👥", f"{kpis['total_customers']:,}",    "Total Customers",    "2,240 analysed"),
        kpi_card("📣", f"{kpis['total_campaigns']}",      "Campaigns Analysed", "5 historical waves"),
        kpi_card("✅", f"{kpis['positive_responses']:,}", "Positive Responses", "Latest campaign"),
        kpi_card("📈", f"{kpis['response_rate']:.2f}%",  "Acceptance Rate",    "Industry avg: 10–12%"),
        kpi_card("💰", f"${kpis['average_income']:,.0f}", "Average Income",     "Across all segments"),
        kpi_card("🛒", f"${kpis['average_spending']:,.0f}","Avg Spending",      "6 product categories"),
    ), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── MODULE NAVIGATION GRID ───────────────────────────────────────────────────
st.markdown("""
<p style='font-size:1.1rem;font-weight:800;color:#0F172A;margin-bottom:0.3rem;'>Platform Modules</p>
<p style='font-size:0.82rem;color:#64748B;margin-bottom:0.8rem;'>Select any module from the left sidebar to begin your analysis.</p>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="module-grid">' +
    module_card("1", "📊", "Dashboard",          "Live KPIs, campaign acceptance charts, and product spend breakdowns.") +
    module_card("2", "📁", "Data Management",    "Upload CSV/Excel, detect anomalies, clean data, and sync to database.") +
    module_card("3", "📈", "Campaign Analysis",  "Compare conversion rates across all campaigns and purchase channels.") +
    module_card("4", "🔍", "Customer Insights",  "Age cohorts, income tiers, education, and product affinity drivers.") +
    module_card("5", "🎯", "Segmentation",       "K-Means clustering with Elbow & Silhouette diagnostics and personas.") +
    module_card("6", "🤖", "Response Prediction","Logistic Regression predictor with batch scoring and ROC evaluation.") +
    module_card("7", "💡", "Recommendations",    "Data-driven consulting actions distinguishing correlation from causation.") +
    module_card("8", "📑", "Reports",            "One-click executive PDF briefs and structured CSV data exports.") +
    '</div>',
    unsafe_allow_html=True
)

st.markdown(divider(), unsafe_allow_html=True)

# ── SYSTEM HEALTH DETAIL ─────────────────────────────────────────────────────
h1, h2 = st.columns([3, 2])
with h1:
    st.markdown("""
<p style='font-size:1.05rem;font-weight:800;color:#0F172A;margin-bottom:0.3rem;'>
Five-Layer Enterprise Architecture
</p>
<p style='font-size:0.82rem;color:#64748B;margin-bottom:0.8rem;'>
Clean decoupled design ensures maintainability, testability, and presentation resilience.
</p>
""", unsafe_allow_html=True)
    layers = [
        ("#3B82F6", "Presentation",    "Streamlit multi-page web app · 8 specialized modules"),
        ("#0D9488", "Application",     "Python analytics engine · data validation · business logic"),
        ("#8B5CF6", "Database",        "PostgreSQL schema · SQLite offline fallback · 6 relational tables"),
        ("#F59E0B", "Machine Learning","K-Means clustering · Logistic Regression · Joblib artifacts"),
        ("#EC4899", "Output",          "Plotly charts · ReportLab PDF · CSV exports"),
    ]
    for color, name, desc in layers:
        st.markdown(f"""
<div style='display:flex;align-items:center;gap:0.75rem;padding:0.65rem 0.9rem;
background:white;border-radius:10px;border:1px solid #E2E8F0;
margin-bottom:0.5rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);
animation:floatUp 0.5s ease both;'>
<div style='width:10px;height:36px;border-radius:5px;background:{color};flex-shrink:0;'></div>
<div>
<div style='font-size:0.82rem;font-weight:700;color:#0F172A;'>{name} Layer</div>
<div style='font-size:0.74rem;color:#64748B;'>{desc}</div>
</div>
</div>""", unsafe_allow_html=True)

with h2:
    st.markdown("""
<p style='font-size:1.05rem;font-weight:800;color:#0F172A;margin-bottom:0.3rem;'>
Live System Status
</p>
""", unsafe_allow_html=True)
    # ML metrics if available
    if ml_stat.get("trained"):
        m = ml_stat.get("metrics", {})
        for metric, val, color in [
            ("ROC-AUC",   m.get("roc_auc", 0)*100,   "#3B82F6"),
            ("Accuracy",  m.get("accuracy", 0)*100,   "#10B981"),
            ("Recall",    m.get("recall", 0)*100,     "#8B5CF6"),
            ("F1-Score",  m.get("f1_score", 0)*100,   "#F59E0B"),
        ]:
            from src.styles import animated_progress
            st.markdown(animated_progress(metric, val, color), unsafe_allow_html=True)
    else:
        st.info("Train the model in Module 6 to view live ML metrics here.")
