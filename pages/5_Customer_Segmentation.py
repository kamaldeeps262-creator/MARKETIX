"""
MARKETIX Module 5: Customer Segmentation (Unsupervised Machine Learning)
Groups customers based on behavioural similarities using K-Means Clustering,
StandardScaler normalization, Elbow method, and Silhouette analysis.
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
from ml.segmentation import calculate_elbow_and_silhouette, perform_kmeans_clustering
from src.visualizations import plot_segment_scatter
from database.queries import save_customer_segments_to_db
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Customer Segmentation | MARKETIX", page_icon="🎯", layout="wide")

st.title("🎯 Customer Segmentation (K-Means Clustering)")
st.caption("Group customers by purchasing behaviors, income, and engagement using Unsupervised Machine Learning.")

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

# Sidebar / Expander controls for Hyperparameters
with st.expander("⚙️ Clustering Configuration & Optimal K Diagnostics", expanded=False):
    st.markdown("**Elbow Method & Silhouette Score Evaluation**")
    diag_res = calculate_elbow_and_silhouette(df, max_k=7)
    
    col_elbow, col_sil = st.columns(2)
    with col_elbow:
        fig_elbow = go.Figure()
        fig_elbow.add_trace(go.Scatter(x=diag_res["k_range"], y=diag_res["inertias"], mode="lines+markers", line=dict(color="#1E3A8A", width=2)))
        fig_elbow.update_layout(title="<b>Elbow Curve (Inertia vs K)</b>", xaxis_title="Number of Clusters (K)", yaxis_title="Inertia (WCSS)", template="plotly_white", height=300)
        st.plotly_chart(fig_elbow, use_container_width=True)

    with col_sil:
        fig_sil = go.Figure()
        fig_sil.add_trace(go.Bar(x=diag_res["k_range"], y=diag_res["silhouette_scores"], marker_color="#0D9488"))
        fig_sil.update_layout(title="<b>Silhouette Scores by K</b>", xaxis_title="Number of Clusters (K)", yaxis_title="Silhouette Score", template="plotly_white", height=300)
        st.plotly_chart(fig_sil, use_container_width=True)
        
    st.info(f"Optimal cluster count suggested by Silhouette Analysis: **K = {diag_res['optimal_k_by_silhouette']}**")

# Interactive Cluster Selector
k_col1, k_col2 = st.columns([1, 3])
with k_col1:
    n_clusters = st.slider("Select Number of Clusters (K)", min_value=2, max_value=6, value=4)

# Execute Clustering
df_segmented, profile_df, ml_metrics = perform_kmeans_clustering(df, n_clusters=n_clusters)
st.session_state["segmented_df"] = df_segmented

with k_col2:
    st.metric(
        "Clustering Quality",
        f"Silhouette Score: {ml_metrics['silhouette_score']}",
        delta=f"{n_clusters} Distinct Personas Identified",
        help="Silhouette score measures how similar an object is to its own cluster compared to other clusters."
    )

st.markdown("---")

# Visualizations: 2D Scatter & 3D Interactive
col_viz, col_prof = st.columns([3, 2])

with col_viz:
    fig_scatter = plot_segment_scatter(df_segmented)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_prof:
    st.subheader("Segment Persona Profiles")
    st.dataframe(
        profile_df.style.format({
            "Customer_Count": "{:,}",
            "Income": "${:,.0f}",
            "Total_Spending": "${:,.0f}",
            "Total_Purchases": "{:.1f}",
            "Age": "{:.1f} yrs",
            "Response_Rate_%": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# Persona Descriptions
st.subheader("Customer Persona Summary")
cols = st.columns(n_clusters)
for idx, (_, row) in enumerate(profile_df.iterrows()):
    with cols[idx]:
        with st.container(border=True):
            st.markdown(f"### {row['Segment_Name']}")
            st.markdown(f"**Size:** {int(row['Customer_Count']):,} customers")
            st.markdown(f"**Avg Income:** ${row['Income']:,.0f}")
            st.markdown(f"**Avg Spend:** ${row['Total_Spending']:,.0f}")
            st.markdown(f"**Response Rate:** {row.get('Response_Rate_%', 0):.1f}%")
            
            # Action strategy based on persona
            if "Affluent" in row["Segment_Name"]:
                st.caption("Strategy: Premium VIP rewards, luxury bundles, concierge engagement.")
            elif "Budget" in row["Segment_Name"]:
                st.caption("Strategy: High-discount clearance coupons, value-oriented flash deals.")
            elif "Cautious" in row["Segment_Name"]:
                st.caption("Strategy: Trust-building communications, product guarantees, educational drip campaigns.")
            else:
                st.caption("Strategy: Seasonal promotions, catalog marketing, multi-channel reminders.")

# Database Save & Download
col_act1, col_act2 = st.columns(2)
with col_act1:
    if st.button("💾 Persist Customer Segments to Database", type="primary"):
        ok, msg = save_customer_segments_to_db(df_segmented)
        if ok:
            st.success(f"✓ {msg}")
        else:
            st.warning(f"Database notice: {msg}")

with col_act2:
    csv_segments = df_segmented[["ID", "Cluster", "Segment_Name", "Income", "Total_Spending", "Total_Purchases"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Segmented Customers CSV",
        data=csv_segments,
        file_name="MARKETIX_Customer_Segments.csv",
        mime="text/csv"
    )
