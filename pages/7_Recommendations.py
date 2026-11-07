"""
MARKETIX Module 7: Strategic Business Recommendations — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, insight_card, kpi_card, kpi_grid
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from src.campaign_analysis import analyze_campaign_performance
from src.recommendations import generate_recommendations

st.set_page_config(page_title="Recommendations | MARKETIX", page_icon="💡", layout="wide")
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
        💡 Strategic Business Recommendations
    </h1>
    <p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
        Consulting-grade strategic action steps grounded in empirical analytics and statistical evidence.
    </p>
</div>
""", unsafe_allow_html=True)

# Generate recommendations
camp_results = analyze_campaign_performance(df)
recommendations = generate_recommendations(df, campaign_summary=camp_results)

high_count = sum(1 for r in recommendations if r.get("priority") == "High")
med_count = sum(1 for r in recommendations if r.get("priority") != "High")

# ── KPI METRICS CARDS ─────────────────────────────────────────────────────────
st.markdown(kpi_grid(
    kpi_card("💡", str(len(recommendations)), "Strategic Actions"),
    kpi_card("🚨", str(high_count), "High Priority"),
    kpi_card("⚡", str(med_count), "Medium Priority"),
    kpi_card("🏛️", "BCG X / Deloitte", "Decision Framework"),
), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── RECOMMENDATION CARDS ─────────────────────────────────────────────────────
st.markdown(section_header("🎯", "Prioritized Strategic Initiatives", "Derived directly from empirical customer dataset patterns"), unsafe_allow_html=True)

for rec in recommendations:
    st.markdown(insight_card(
        title=rec.get("category", "Strategy"),
        finding=rec.get("finding", ""),
        evidence=rec.get("evidence", ""),
        recommendation=rec.get("recommendation", ""),
        impact=rec.get("expected_impact", ""),
        priority=rec.get("priority", "Medium")
    ), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── METHODOLOGY CALLOUT ──────────────────────────────────────────────────────
st.markdown(section_header("🔬", "Academic & Consulting Governance: Correlation vs Causation"), unsafe_allow_html=True)
st.markdown("""
<div style='background:white;border-radius:14px;padding:1.4rem;border:1px solid #E2E8F0;box-shadow:0 2px 12px rgba(0,0,0,0.04);animation:floatUp 0.6s ease both;'>
    <div style='display:flex;gap:1.5rem;flex-wrap:wrap;'>
        <div style='flex:1;min-width:260px;'>
            <div style='font-weight:700;color:#1E3A8A;margin-bottom:0.4rem;'>1. Empirical Association vs True Causality</div>
            <div style='color:#475569;font-size:0.85rem;line-height:1.5;'>
                Observed correlations (such as high Wine/Meat spend associating with higher campaign acceptance) represent <b>historical customer affinity</b>. They do not guarantee that increasing customer wine consumption will trigger campaign conversion.
            </div>
        </div>
        <div style='flex:1;min-width:260px;'>
            <div style='font-weight:700;color:#0D9488;margin-bottom:0.4rem;'>2. Recommended Next Step: A/B Experimentation</div>
            <div style='color:#475569;font-size:0.85rem;line-height:1.5;'>
                Before scaling major marketing budgets into the proposed initiatives, the organization should run a <b>randomized controlled trial (RCT)</b> with a 10% uncontacted holdout group to measure true incremental sales lift.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
