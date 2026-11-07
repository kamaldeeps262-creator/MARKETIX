"""
MARKETIX Module 7: Strategic Business Recommendations
Synthesizes analytical findings into data-driven business suggestions following
consulting frameworks (BCG X / Deloitte), clearly distinguishing correlation from causation.
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
from src.campaign_analysis import analyze_campaign_performance
from src.recommendations import generate_recommendations

st.set_page_config(page_title="Recommendations | MARKETIX", page_icon="💡", layout="wide")

st.title("💡 Strategic Business Recommendations")
st.caption("Actionable business recommendations derived from empirical data analytics and predictive insights.")

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

# Generate recommendations
camp_results = analyze_campaign_performance(df)
recommendations = generate_recommendations(df, campaign_summary=camp_results)

st.markdown("""
> [!NOTE]
> Recommendations below are algorithmically produced based on statistical tests,
> response distributions, and customer purchasing patterns in the current dataset.
""")

for idx, rec in enumerate(recommendations, 1):
    priority_color = "#EF4444" if rec["priority"] == "High" else "#F59E0B"
    with st.container(border=True):
        col_title, col_prio = st.columns([4, 1])
        with col_title:
            st.markdown(f"### Strategy #{idx}: {rec['category']}")
        with col_prio:
            st.markdown(f"<span style='background-color:{priority_color}; color:white; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:12px;'>Priority: {rec['priority']}</span>", unsafe_allow_html=True)
        
        st.markdown(f"**🔍 Analytical Finding:** {rec['finding']}")
        st.markdown(f"**📊 Supporting Evidence:** `{rec['evidence']}`")
        st.markdown(f"**🎯 Strategic Action:** {rec['recommendation']}")
        st.markdown(f"**🚀 Expected Business Impact:** {rec['expected_impact']}")

st.markdown("---")
st.subheader("Methodology: Correlation vs Causation Notice")
st.markdown("""
- **Empirical Association:** Observed correlations (such as high wine spending or previous campaign responsiveness correlating with positive campaign responses) reflect **historical customer affinity**, not necessarily direct causality.
- **Controlled Experimentation Recommendation:** Before broad deployment of high-cost marketing initiatives, implement **A/B split testing** with randomized holdout control groups to measure true incremental lift.
""")
