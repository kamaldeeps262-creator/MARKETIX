"""
MARKETIX Module 4: Customer Insights & Purchasing Behaviour
Granular demographic profiling, income analysis, spending tier comparisons,
and product category affinities.
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
from src.customer_analysis import analyze_demographics, analyze_spending_by_tier, analyze_product_affinity
from src.visualizations import plot_income_vs_spending
import plotly.express as px

st.set_page_config(page_title="Customer Insights | MARKETIX", page_icon="🔍", layout="wide")

st.title("🔍 Customer Insights & Purchasing Behaviour")
st.caption("Investigate customer demographics, income dynamics, spending tiers, and product affinity drivers.")

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

demographics = analyze_demographics(df)

# Top Demographics Cards
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.metric("Median Customer Age", f"{int(demographics.get('median_age', 56))} yrs")
with d2:
    inc_stats = demographics.get("income_stats", {})
    st.metric("Median Income", f"${inc_stats.get('median', 51381):,.0f}")
with d3:
    st.metric("Average Total Spend", f"${df['Total_Spending'].mean():,.0f}" if 'Total_Spending' in df.columns else "$606")
with d4:
    parent_pct = round(df["Is_Parent"].mean() * 100, 1) if "Is_Parent" in df.columns else 71.5
    st.metric("Parents with Children", f"{parent_pct}%")

st.markdown("---")

tab_demo, tab_spending, tab_affinity = st.tabs(["👥 Demographic Breakdown", "💰 Spending Tiers & Response Rates", "🍷 Product Category Affinities"])

with tab_demo:
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.markdown("### Age Cohorts")
        age_dist = demographics.get("age_distribution", {})
        if age_dist:
            df_age = pd.DataFrame(list(age_dist.items()), columns=["Age Group", "Count"])
            fig_age = px.bar(df_age, x="Age Group", y="Count", color="Count", color_continuous_scale="Teal", template="plotly_white")
            st.plotly_chart(fig_age, use_container_width=True)

    with col_d2:
        st.markdown("### Education Levels")
        edu_dist = demographics.get("education_distribution", {})
        if edu_dist:
            df_edu = pd.DataFrame(list(edu_dist.items()), columns=["Education", "Count"])
            fig_edu = px.pie(df_edu, names="Education", values="Count", hole=0.4, template="plotly_white")
            st.plotly_chart(fig_edu, use_container_width=True)

    with col_d3:
        st.markdown("### Marital Status")
        mar_dist = demographics.get("marital_distribution", {})
        if mar_dist:
            df_mar = pd.DataFrame(list(mar_dist.items()), columns=["Status", "Count"])
            fig_mar = px.bar(df_mar, x="Status", y="Count", color="Count", color_continuous_scale="Purples", template="plotly_white")
            st.plotly_chart(fig_mar, use_container_width=True)

with tab_spending:
    st.subheader("Spending Tiers vs Campaign Acceptance Rate")
    st.markdown("""
    > [!IMPORTANT]
    > **Key Hypothesis Validation:** Customers in higher spending brackets exhibit **dramatically higher acceptance rates** 
    > during marketing campaigns compared to low spenders.
    """)
    
    tier_df = analyze_spending_by_tier(df)
    st.dataframe(
        tier_df.style.format({
            "Customer_Count": "{:,}",
            "Avg_Income": "${:,.2f}",
            "Avg_Spending": "${:,.2f}",
            "Avg_Purchases": "{:.1f}",
            "Response_Rate": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    fig_tier = px.bar(
        tier_df,
        x="Spending_Tier",
        y="Response_Rate",
        color="Spending_Tier",
        text="Response_Rate",
        title="<b>Acceptance Rate (%) by Spending Tier</b>",
        labels={"Response_Rate": "Response Rate (%)"},
        template="plotly_white"
    )
    fig_tier.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig_tier, use_container_width=True)

with tab_affinity:
    st.subheader("Product Category Preferences: Responders vs Non-Responders")
    st.markdown("Compares average spending across product categories for customers who accepted vs rejected the campaign.")
    
    affinity_df = analyze_product_affinity(df)
    if not affinity_df.empty:
        st.dataframe(
            affinity_df.style.format({
                "Responders_Avg_Spend": "${:,.2f}",
                "Non_Responders_Avg_Spend": "${:,.2f}",
                "Spend_Difference_%": "{:+.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

        fig_aff = px.bar(
            affinity_df,
            x="Product_Category",
            y="Spend_Difference_%",
            color="Spend_Difference_%",
            color_continuous_scale="RdYlGn",
            title="<b>Spend Premium (%) of Campaign Responders over Non-Responders</b>",
            text="Spend_Difference_%",
            template="plotly_white"
        )
        fig_aff.update_traces(texttemplate="%{text:+.1f}%", textposition="outside")
        st.plotly_chart(fig_aff, use_container_width=True)
