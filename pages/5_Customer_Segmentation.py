"""
MARKETIX Module 5: Customer Segmentation — Animated Redesign
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, persona_card, kpi_card, kpi_grid
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from ml.segmentation import calculate_elbow_and_silhouette, perform_kmeans_clustering
from src.visualizations import plot_segment_scatter
from database.queries import save_customer_segments_to_db
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Segmentation | MARKETIX", page_icon="🎯", layout="wide")
inject_styles()

if "cleaned_df" not in st.session_state or st.session_state["cleaned_df"] is None:
    df_raw, _ = load_dataset()
    if df_raw is not None:
        df_clean, _ = clean_marketing_data(df_raw)
        st.session_state["cleaned_df"] = df_clean

df = st.session_state.get("cleaned_df")
if df is None:
    st.warning("⚠️ No dataset loaded. Please go to Data Management.")
    st.stop()

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='animation:fadeSlideDown 0.5s ease both;'>
    <h1 style='margin:0;font-size:1.9rem;font-weight:900;color:#0F172A;'>
        🎯 Customer Segmentation
    </h1>
    <p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
        Unsupervised K-Means clustering with Elbow Method &amp; Silhouette diagnostics.
    </p>
</div>
""", unsafe_allow_html=True)

# ── ELBOW & SILHOUETTE DIAGNOSTICS ───────────────────────────────────────────
with st.expander("📐  Optimal K Diagnostics — Elbow Curve & Silhouette Scores", expanded=False):
    with st.spinner("Computing cluster quality metrics for K = 2 … 7 …"):
        diag = calculate_elbow_and_silhouette(df, max_k=7)

    d1, d2 = st.columns(2)
    with d1:
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(
            x=diag["k_range"], y=diag["inertias"],
            mode="lines+markers",
            line=dict(color="#1E3A8A", width=3),
            marker=dict(size=9, color="#3B82F6", line=dict(width=2, color="white")),
            name="Inertia (WCSS)"
        ))
        fig_e.update_layout(
            title="<b>Elbow Method — Inertia vs Number of Clusters</b>",
            xaxis_title="K  (Number of Clusters)",
            yaxis_title="Within-Cluster Sum of Squares",
            template="plotly_white", height=300,
            margin=dict(l=20, r=20, t=50, b=30)
        )
        st.plotly_chart(fig_e, width="stretch")

    with d2:
        best_k = diag["optimal_k_by_silhouette"]
        bar_colors = ["#F59E0B" if k == best_k else "#CBD5E1" for k in diag["k_range"]]
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(
            x=diag["k_range"], y=diag["silhouette_scores"],
            marker_color=bar_colors, text=[f"{s:.3f}" for s in diag["silhouette_scores"]],
            textposition="outside"
        ))
        fig_s.update_layout(
            title="<b>Silhouette Score by K — Best K highlighted</b>",
            xaxis_title="K  (Number of Clusters)",
            yaxis_title="Silhouette Score",
            template="plotly_white", height=300,
            margin=dict(l=20, r=20, t=50, b=30)
        )
        st.plotly_chart(fig_s, width="stretch")

    st.info(f"📌 Optimal cluster count by Silhouette analysis: **K = {diag['optimal_k_by_silhouette']}**  "
            f"(highest inter-cluster separation score = **{max(diag['silhouette_scores']):.4f}**)")

st.markdown(divider(), unsafe_allow_html=True)

# ── K SELECTOR + METRICS ──────────────────────────────────────────────────────
st.markdown(section_header("⚙️", "Clustering Configuration", "Drag slider to change the number of personas"),
            unsafe_allow_html=True)

ctrl_a, ctrl_b = st.columns([1, 3])
with ctrl_a:
    n_clusters = st.slider("Number of Clusters (K)", 2, 6, 4)

# Run clustering
with st.spinner("Running K-Means algorithm …"):
    df_seg, profile_df, ml_metrics = perform_kmeans_clustering(df, n_clusters=n_clusters)
st.session_state["segmented_df"] = df_seg

sil = ml_metrics["silhouette_score"]
sil_quality = "Excellent" if sil > 0.5 else ("Good" if sil > 0.3 else "Moderate")
with ctrl_b:
    st.markdown(kpi_grid(
        kpi_card("🔢", str(n_clusters), "Customer Clusters"),
        kpi_card("📏", f"{sil:.4f}", "Silhouette Score"),
        kpi_card("⭐", sil_quality, "Cluster Quality"),
        kpi_card("👥", f"{len(df):,}", "Customers Segmented"),
    ), unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── SCATTER PLOT + PROFILE TABLE ─────────────────────────────────────────────
st.markdown(section_header("🗺️", "Cluster Visualisation — Income vs Total Spending"), unsafe_allow_html=True)
sc_col, tbl_col = st.columns([3, 2])

with sc_col:
    st.plotly_chart(plot_segment_scatter(df_seg), width="stretch")

with tbl_col:
    st.markdown("<p style='font-size:0.85rem;font-weight:700;color:#334155;margin-bottom:0.5rem;'>Cluster Profiles</p>",
                unsafe_allow_html=True)
    fmt = {}
    if "Income" in profile_df.columns:         fmt["Income"] = "${:,.0f}"
    if "Total_Spending" in profile_df.columns:  fmt["Total_Spending"] = "${:,.0f}"
    if "Response_Rate_%" in profile_df.columns: fmt["Response_Rate_%"] = "{:.1f}%"
    if "Age" in profile_df.columns:             fmt["Age"] = "{:.0f} yrs"
    st.dataframe(profile_df.style.format(fmt), width="stretch", hide_index=True, height=280)

st.markdown(divider(), unsafe_allow_html=True)

# ── PERSONA CARDS ─────────────────────────────────────────────────────────────
st.markdown(section_header("🎭", "Customer Persona Cards", "Each cluster translated into an actionable marketing persona"),
            unsafe_allow_html=True)

PERSONA_META = {
    "Affluent Champions":      ("🏆", "Premium loyalty rewards, early-access products, concierge engagement."),
    "Budget Seekers":          ("💸", "High-discount flash deals, value bundles, clearance promotions."),
    "Cautious Savers":         ("🔒", "Trust-building content, product guarantees, educational drip campaigns."),
    "High-Value Enthusiasts":  ("🚀", "Seasonal catalog mailings, digital retargeting, multi-channel reminders."),
}

# Build up to 4 columns
p_cols = st.columns(min(n_clusters, 4))
for idx, (_, row) in enumerate(profile_df.iterrows()):
    name   = str(row.get("Segment_Name", f"Cluster {row['Cluster']}"))
    base   = name.split("(")[0].strip()
    emoji, strategy = PERSONA_META.get(base, ("🎯", "Review cluster characteristics to define a targeted strategy."))
    size   = int(row.get("Customer_Count", 0))
    inc    = float(row.get("Income", 0))
    spd    = float(row.get("Total_Spending", 0))
    rr     = float(row.get("Response_Rate_%", 0))

    with p_cols[idx % min(n_clusters, 4)]:
        st.markdown(persona_card(emoji, name, size, inc, spd, rr, strategy, delay=idx*0.1),
                    unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── ACTIONS ───────────────────────────────────────────────────────────────────
act1, act2 = st.columns(2)
with act1:
    if st.button("💾  Save Segments to Database", type="primary", width="stretch"):
        ok, msg = save_customer_segments_to_db(df_seg)
        (st.success if ok else st.warning)(msg)
with act2:
    csv_seg = df_seg[["ID", "Cluster", "Segment_Name", "Income", "Total_Spending", "Total_Purchases"]].to_csv(index=False).encode()
    st.download_button("📥  Download Segments CSV", data=csv_seg,
                       file_name="MARKETIX_Customer_Segments.csv",
                       mime="text/csv", width="stretch")
