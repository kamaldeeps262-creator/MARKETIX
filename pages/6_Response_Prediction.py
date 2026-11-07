"""
MARKETIX Module 6: Campaign Response Prediction — Animated Redesign
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.styles import inject_styles, section_header, divider, kpi_card, kpi_grid, animated_progress
from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from ml.train_model import train_logistic_regression
from ml.predict import predict_single_customer, predict_batch_customers, load_model
from ml.evaluate import get_model_status
from src.visualizations import plot_confusion_matrix, plot_roc_curve
from database.queries import save_prediction_to_db

st.set_page_config(page_title="Response Prediction | MARKETIX", page_icon="🤖", layout="wide")
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

# Auto-train if needed
if load_model() is None:
    with st.spinner("Training baseline Logistic Regression model …"):
        st.session_state["train_results"] = train_logistic_regression(df)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='animation:fadeSlideDown 0.5s ease both;'>
    <h1 style='margin:0;font-size:1.9rem;font-weight:900;color:#0F172A;'>
        🤖 Campaign Response Prediction
    </h1>
    <p style='color:#64748B;font-size:0.88rem;margin:0.3rem 0 1.2rem;'>
        Balanced Logistic Regression — stratified training, ROC-AUC-focused evaluation.
    </p>
</div>
""", unsafe_allow_html=True)

tab_single, tab_batch, tab_eval = st.tabs([
    "🎯  Single Customer Prediction",
    "📊  Batch Scoring",
    "📈  Model Diagnostics"
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — SINGLE PREDICTION
# ═══════════════════════════════════════════════════════════
with tab_single:
    st.markdown(section_header("🎯", "Interactive Prospect Scoring",
                "Fill in customer attributes to get a real-time conversion probability."),
                unsafe_allow_html=True)

    with st.form("pred_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            cust_id   = st.number_input("Customer ID", min_value=1, value=105, step=1)
            age       = st.slider("Age", 18, 90, 45)
            education = st.selectbox("Education", ["Graduation", "PhD", "Master", "2n Cycle", "Basic"])
            marital   = st.selectbox("Marital Status", ["Married", "Together", "Single", "Divorced", "Widow"])
        with c2:
            income      = st.number_input("Annual Income ($)", 5000, 250000, 75000, step=1000)
            recency     = st.slider("Days Since Last Purchase", 0, 100, 15)
            mnt_wines   = st.number_input("Wine Spending ($)",  0, 2000, 500,  step=25)
            mnt_meat    = st.number_input("Meat Spending ($)",  0, 2000, 350,  step=25)
        with c3:
            cmp1 = st.checkbox("Accepted Campaign 1", value=True)
            cmp5 = st.checkbox("Accepted Campaign 5", value=True)
            cmp3 = st.checkbox("Accepted Campaign 3", value=False)
            cat_p = st.number_input("Catalog Purchases", 0, 30, 4, step=1)
            sto_p = st.number_input("Store Purchases",   0, 30, 8, step=1)
            web_v = st.number_input("Monthly Web Visits",0, 30, 3, step=1)
        threshold = st.slider("Decision Threshold (Cutoff %)", 20, 80, 50, step=5)
        submitted = st.form_submit_button("⚡  Predict Campaign Response", type="primary")

    if submitted:
        payload = dict(
            ID=cust_id, Age=age, Income=income, Recency=recency,
            Education=education, Marital_Status=marital,
            MntWines=mnt_wines, MntMeatProducts=mnt_meat,
            AcceptedCmp1=int(cmp1), AcceptedCmp5=int(cmp5), AcceptedCmp3=int(cmp3),
            NumCatalogPurchases=cat_p, NumStorePurchases=sto_p,
            NumWebVisitsMonth=web_v, Customer_Tenure_Days=500
        )
        result = predict_single_customer(payload, threshold=threshold/100)
        save_prediction_to_db(cust_id, result["predicted_response"],
                              result["probability_positive"]/100,
                              result.get("model_version","1.0-logreg"))

        st.markdown(divider(), unsafe_allow_html=True)
        r_left, r_right = st.columns([1, 2])

        pos_pct = result["probability_positive"]
        neg_pct = result["probability_negative"]
        is_pos  = result["predicted_response"]
        card_cls = "positive" if is_pos else "negative"
        emoji    = "✅" if is_pos else "❌"
        verdict  = "LIKELY TO RESPOND" if is_pos else "UNLIKELY TO RESPOND"
        color    = "#059669" if is_pos else "#DC2626"

        with r_left:
            st.markdown(f"""
<div class="pred-card {card_cls}">
    <div style='font-size:2.5rem;'>{emoji}</div>
    <div class="pred-verdict" style='color:{color};'>{verdict}</div>
    <div class="pred-pct" style='color:{color};'>{pos_pct:.1f}%</div>
    <div class="pred-label">Positive response probability<br>
        <small>Threshold: {threshold}% | Model: {result.get('model_version','1.0-logreg')}</small>
    </div>
</div>""", unsafe_allow_html=True)

        with r_right:
            st.markdown("<p style='font-weight:700;color:#334155;margin-bottom:0.8rem;'>Probability Breakdown</p>",
                        unsafe_allow_html=True)
            st.markdown(animated_progress("🟢  Positive Response", pos_pct, "#10B981"), unsafe_allow_html=True)
            st.markdown(animated_progress("🔴  Negative Response", neg_pct, "#EF4444"), unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700;color:#334155;margin:1rem 0 0.5rem;'>Marketing Strategy</p>",
                        unsafe_allow_html=True)
            if is_pos:
                st.success(
                    "✅  Include in **premium targeted campaign**. Prioritise personalised Wine & Meat product recommendations. "
                    "Expected conversion efficiency is significantly above baseline."
                )
            else:
                st.warning(
                    "⚠️  Exclude from **high-cost direct mail**. Route to low-cost digital retargeting or seasonal newsletter cadence."
                )

# ═══════════════════════════════════════════════════════════
# TAB 2 — BATCH SCORING
# ═══════════════════════════════════════════════════════════
with tab_batch:
    st.markdown(section_header("📊", "Batch Prospect Scoring",
                "Score the entire dataset and extract high-probability targets."), unsafe_allow_html=True)

    batch_thresh = st.slider("Marketing Cutoff Threshold (%)", 20, 80, 50, step=5, key="b_thresh")

    if st.button("🚀  Score All Customers", type="primary"):
        with st.spinner("Scoring 2,240 customer profiles …"):
            scored_df = predict_batch_customers(df, threshold=batch_thresh/100)
            st.session_state["scored_df"] = scored_df

    scored_df = st.session_state.get("scored_df")
    if scored_df is not None:
        t_count = int((scored_df["Predicted_Response"] == 1).sum())
        t_pct   = round(t_count / len(scored_df) * 100, 1)

        st.markdown(kpi_grid(
            kpi_card("📋", f"{len(scored_df):,}", "Total Scored"),
            kpi_card("🎯", f"{t_count:,}",        "High-Prob Targets"),
            kpi_card("📊", f"{t_pct}%",           "Target Audience %"),
            kpi_card("💡", f"{batch_thresh}%",    "Threshold Used"),
        ), unsafe_allow_html=True)

        st.dataframe(
            scored_df[["ID","Income","Total_Spending",
                        "Predicted_Probability","Response_Likelihood"]].head(30),
            use_container_width=True, hide_index=True
        )
        csv_sc = scored_df[["ID","Income","Total_Spending",
                              "Predicted_Probability","Predicted_Response"]].to_csv(index=False).encode()
        st.download_button("📥  Download Scored CSV", data=csv_sc,
                           file_name="MARKETIX_Scored_Prospects.csv", mime="text/csv")

# ═══════════════════════════════════════════════════════════
# TAB 3 — EVALUATION
# ═══════════════════════════════════════════════════════════
with tab_eval:
    st.markdown(section_header("📈", "Model Evaluation Diagnostics",
                "Confusion Matrix · ROC Curve · Feature Importances"), unsafe_allow_html=True)

    if "train_results" not in st.session_state:
        st.session_state["train_results"] = train_logistic_regression(df)

    res = st.session_state["train_results"]
    m   = res["metrics"]

    # Metric KPI Row
    st.markdown(kpi_grid(
        kpi_card("🎯", f"{m['accuracy']*100:.1f}%",  "Accuracy"),
        kpi_card("🔬", f"{m['precision']*100:.1f}%", "Precision"),
        kpi_card("📡", f"{m['recall']*100:.1f}%",    "Recall"),
        kpi_card("⚖️", f"{m['f1_score']:.3f}",       "F1-Score"),
        kpi_card("📈", f"{m['roc_auc']:.3f}",        "ROC-AUC"),
    ), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    ev1, ev2 = st.columns(2)
    with ev1:
        st.plotly_chart(plot_confusion_matrix(res["confusion_matrix"]), use_container_width=True)
    with ev2:
        roc = res["roc_curve"]
        st.plotly_chart(plot_roc_curve(roc["fpr"], roc["tpr"], roc["auc"]), use_container_width=True)

    st.markdown(section_header("🔑", "Top Predictive Feature Drivers",
                "Logistic Regression coefficients ranked by influence on response probability"),
                unsafe_allow_html=True)

    coef_df = res["coefficients"].head(12)
    colors_pos = ["#10B981" if v >= 0 else "#EF4444" for v in coef_df["Coefficient"]]
    import plotly.graph_objects as go
    fig_coef = go.Figure(go.Bar(
        x=coef_df["Coefficient"], y=coef_df["Feature"],
        orientation="h", marker_color=colors_pos,
        text=[f"{v:+.3f}" for v in coef_df["Coefficient"]], textposition="outside"
    ))
    fig_coef.update_layout(
        title="<b>Logistic Regression Coefficients — Top 12 Features</b>",
        xaxis_title="Coefficient Value", yaxis_title="",
        template="plotly_white", height=400,
        margin=dict(l=20, r=60, t=50, b=30)
    )
    st.plotly_chart(fig_coef, use_container_width=True)

    if st.button("🔄  Retrain Model", use_container_width=True):
        with st.spinner("Retraining …"):
            st.session_state["train_results"] = train_logistic_regression(df)
        st.success("✅ Model retrained and saved!")
        st.rerun()
