"""
MARKETIX Module 6: Campaign Response Prediction (Supervised Machine Learning)
Predicts customer response propensities using Logistic Regression.
Features interactive single-customer inference, batch propensity scoring,
and comprehensive model evaluation (Confusion Matrix, ROC Curve, Feature Importance).
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_loader import load_dataset
from src.data_cleaning import clean_marketing_data
from ml.train_model import train_logistic_regression
from ml.predict import predict_single_customer, predict_batch_customers, load_model
from ml.evaluate import get_model_status
from src.visualizations import plot_confusion_matrix, plot_roc_curve
from database.queries import save_prediction_to_db

st.set_page_config(page_title="Response Prediction | MARKETIX", page_icon="🤖", layout="wide")

st.title("🤖 Campaign Response Prediction (Logistic Regression)")
st.caption("Supervised Machine Learning model estimating the likelihood of individual prospects converting on upcoming marketing campaigns.")

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

# Ensure model is trained
artifacts = load_model()
if artifacts is None:
    with st.spinner("Training baseline Logistic Regression model..."):
        train_res = train_logistic_regression(df)
        st.session_state["train_results"] = train_res
        artifacts = load_model()

tab_single, tab_batch, tab_eval = st.tabs([
    "🎯 Interactive Single Customer Prediction",
    "📊 Batch Customer Scoring",
    "📈 Model Evaluation & Diagnostics"
])

# ----------------- TAB 1: SINGLE PREDICTION -----------------
with tab_single:
    st.subheader("Predict Campaign Response for a Specific Prospect")
    st.markdown("Enter customer attributes to compute conversion probability in real time.")

    with st.form("customer_prediction_form"):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            cust_id = st.number_input("Customer ID", min_value=1, value=105, step=1)
            age = st.slider("Customer Age", min_value=18, max_value=90, value=45)
            education = st.selectbox("Education Level", ["Graduation", "PhD", "Master", "2n Cycle", "Basic"])
            marital = st.selectbox("Marital Status", ["Married", "Together", "Single", "Divorced", "Widow"])
        
        with col_f2:
            income = st.number_input("Annual Income ($)", min_value=5000, max_value=250000, value=75000, step=1000)
            recency = st.slider("Days Since Last Purchase (Recency)", min_value=0, max_value=100, value=15)
            mnt_wines = st.number_input("Spend on Wine ($)", min_value=0, max_value=2000, value=500, step=25)
            mnt_meat = st.number_input("Spend on Meat ($)", min_value=0, max_value=2000, value=350, step=25)

        with col_f3:
            prev_cmp1 = st.checkbox("Accepted Campaign 1", value=True)
            prev_cmp5 = st.checkbox("Accepted Campaign 5", value=True)
            prev_cmp3 = st.checkbox("Accepted Campaign 3", value=False)
            catalog_purch = st.number_input("Catalog Purchases", min_value=0, max_value=30, value=4, step=1)
            store_purch = st.number_input("Store Purchases", min_value=0, max_value=30, value=8, step=1)
            web_visits = st.number_input("Monthly Web Visits", min_value=0, max_value=30, value=3, step=1)

        threshold = st.slider("Decision Threshold (Cutoff Probability)", min_value=0.20, max_value=0.80, value=0.50, step=0.05)
        submit_btn = st.form_submit_button("⚡ Predict Campaign Response", type="primary")

    if submit_btn:
        customer_payload = {
            "ID": cust_id,
            "Age": age,
            "Income": income,
            "Recency": recency,
            "Education": education,
            "Marital_Status": marital,
            "MntWines": mnt_wines,
            "MntMeatProducts": mnt_meat,
            "AcceptedCmp1": int(prev_cmp1),
            "AcceptedCmp5": int(prev_cmp5),
            "AcceptedCmp3": int(prev_cmp3),
            "NumCatalogPurchases": catalog_purch,
            "NumStorePurchases": store_purch,
            "NumWebVisitsMonth": web_visits,
            "Customer_Tenure_Days": 500
        }

        result = predict_single_customer(customer_payload, threshold=threshold)
        
        # Save to database
        save_prediction_to_db(
            customer_id=cust_id,
            predicted_response=result["predicted_response"],
            probability=result["probability_positive"] / 100.0,
            model_version=result.get("model_version", "1.0-logreg")
        )

        st.markdown("---")
        st.subheader("📋 Prediction Result")
        
        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            with st.container(border=True):
                st.markdown(f"#### Customer ID: `{result['customer_id']}`")
                if result["predicted_response"]:
                    st.success("✅ **Result: LIKELY TO RESPOND**")
                else:
                    st.error("❌ **Result: UNLIKELY TO RESPOND**")
                
                st.markdown(f"**Positive Response Probability:** `{result['probability_positive']}%`")
                st.markdown(f"**Negative Response Probability:** `{result['probability_negative']}%`")
                st.caption(f"Decision Threshold: `{threshold * 100:.0f}%` | Model: `{result['model_version']}`")

        with res_col2:
            st.progress(result["probability_positive"] / 100.0)
            if result["predicted_response"]:
                st.markdown("""
                **Marketing Strategy Recommendation for this Customer:**
                - Include in VIP automated email campaign sequence.
                - Deliver personalized high-margin product recommendations (Wine & Meat focus).
                - Expected ROI is significantly positive given historical category spend and campaign responsiveness.
                """)
            else:
                st.markdown("""
                **Marketing Strategy Recommendation for this Customer:**
                - Exclude from high-cost direct print mail or outbound tele-campaigns to avoid wasted spend.
                - Place in low-cost digital retargeting or seasonal newsletter workflows.
                """)

# ----------------- TAB 2: BATCH SCORING -----------------
with tab_batch:
    st.subheader("Batch Scoring & Prospect Selection")
    st.markdown("Scores all customers in the active dataset to generate an optimized target prospect list.")

    batch_thresh = st.slider("Select Marketing Conversion Cutoff", min_value=0.20, max_value=0.80, value=0.50, step=0.05, key="batch_slider")
    
    if st.button("🚀 Score Active Dataset", type="primary"):
        with st.spinner("Scoring customer database..."):
            scored_df = predict_batch_customers(df, threshold=batch_thresh)
            st.session_state["scored_df"] = scored_df
            st.success("✓ Batch scoring completed!")

    scored_df = st.session_state.get("scored_df")
    if scored_df is not None:
        target_count = (scored_df["Predicted_Response"] == 1).sum()
        target_pct = (target_count / len(scored_df)) * 100

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Total Contacts Scored", f"{len(scored_df):,}")
        with sc2:
            st.metric("High-Probability Targets", f"{target_count:,}")
        with sc3:
            st.metric("Target Audience Share", f"{target_pct:.1f}%")

        st.dataframe(
            scored_df[["ID", "Income", "Total_Spending", "Predicted_Probability", "Response_Likelihood"]].head(25),
            use_container_width=True,
            hide_index=True
        )

        csv_scored = scored_df[["ID", "Income", "Total_Spending", "Predicted_Probability", "Predicted_Response"]].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Scored Prospects CSV", data=csv_scored, file_name="MARKETIX_Scored_Prospects.csv", mime="text/csv")

# ----------------- TAB 3: MODEL EVALUATION -----------------
with tab_eval:
    st.subheader("Supervised Model Diagnostics & Academic Rigour")
    st.markdown("""
    Evaluated on a **stratified 20% holdout test dataset**.
    Class imbalance is managed through **balanced loss weighting** to ensure high recall for positive responders.
    """)

    if "train_results" not in st.session_state:
        st.session_state["train_results"] = train_logistic_regression(df)
    
    eval_res = st.session_state["train_results"]
    m = eval_res["metrics"]

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Accuracy", f"{m['accuracy'] * 100:.1f}%")
    with m2:
        st.metric("Precision", f"{m['precision'] * 100:.1f}%")
    with m3:
        st.metric("Recall (Sensitivity)", f"{m['recall'] * 100:.1f}%")
    with m4:
        st.metric("F1-Score", f"{m['f1_score']:.3f}")
    with m5:
        st.metric("ROC-AUC", f"{m['roc_auc']:.3f}")

    st.markdown("---")
    
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        fig_cm = plot_confusion_matrix(eval_res["confusion_matrix"])
        st.plotly_chart(fig_cm, use_container_width=True)

    with diag_col2:
        roc_data = eval_res["roc_curve"]
        fig_roc = plot_roc_curve(roc_data["fpr"], roc_data["tpr"], roc_data["auc"])
        st.plotly_chart(fig_roc, use_container_width=True)

    st.subheader("Top Predictive Feature Drivers (Coefficients)")
    coef_df = eval_res["coefficients"]
    st.dataframe(coef_df.head(10), use_container_width=True, hide_index=True)

    if st.button("🔄 Retrain Logistic Regression Model"):
        with st.spinner("Retraining model..."):
            new_train_res = train_logistic_regression(df)
            st.session_state["train_results"] = new_train_res
            st.success("✓ Model retrained and updated on disk!")
            st.rerun()
