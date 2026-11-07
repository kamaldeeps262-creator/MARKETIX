"""
MARKETIX Customer Segmentation Module
Performs unsupervised customer grouping using K-Means Clustering,
StandardScaler feature normalization, and automated persona profiling.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import logging

logger = logging.getLogger("marketix.ml.segmentation")

SEGMENT_FEATURES = [
    "Income",
    "Total_Spending",
    "Total_Purchases",
    "NumWebVisitsMonth",
    "Recency",
    "Age"
]


def calculate_elbow_and_silhouette(df: pd.DataFrame, max_k: int = 7) -> dict:
    """
    Computes inertia (elbow method) and silhouette scores for K ranging from 2 to max_k.
    Assists data analysts and students in selecting the optimal cluster count.
    """
    valid_features = [f for f in SEGMENT_FEATURES if f in df.columns]
    X = df[valid_features].dropna()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    inertias = []
    silhouette_scores = []
    k_range = list(range(2, min(max_k + 1, len(X))))

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(float(km.inertia_))
        score = silhouette_score(X_scaled, km.labels_)
        silhouette_scores.append(float(score))

    return {
        "k_range": k_range,
        "inertias": inertias,
        "silhouette_scores": silhouette_scores,
        "optimal_k_by_silhouette": k_range[int(np.argmax(silhouette_scores))]
    }


def perform_kmeans_clustering(df: pd.DataFrame, n_clusters: int = 4) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Executes K-Means clustering on the dataset and assigns interpretable persona labels.
    Returns:
    - df_with_clusters: original DataFrame enriched with 'Cluster' and 'Segment_Name'
    - cluster_profile: summary table with cluster-level mean metrics
    - metrics: dictionary containing inertia and silhouette score
    """
    df_work = df.copy()
    valid_features = [f for f in SEGMENT_FEATURES if f in df_work.columns]
    
    # Handle missing values if any
    X = df_work[valid_features].copy()
    for col in X.columns:
        X[col] = X[col].fillna(X[col].median())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=15)
    clusters = kmeans.fit_predict(X_scaled)
    df_work["Cluster"] = clusters

    # Silhouette score
    sil_score = float(silhouette_score(X_scaled, clusters)) if len(df_work) > n_clusters else 0.0

    # Calculate cluster profile
    agg_dict = {
        "ID": "count",
        "Income": "mean",
        "Total_Spending": "mean",
        "Total_Purchases": "mean",
        "NumWebVisitsMonth": "mean",
        "Age": "mean",
    }
    if "Response" in df_work.columns:
        agg_dict["Response"] = lambda s: round(s.mean() * 100, 2)

    cluster_profile = df_work.groupby("Cluster").agg(
        {k: v for k, v in agg_dict.items() if k in df_work.columns}
    ).reset_index()

    cluster_profile = cluster_profile.rename(columns={"ID": "Customer_Count", "Response": "Response_Rate_%"})
    cluster_profile["Income"] = cluster_profile["Income"].round(0)
    cluster_profile["Total_Spending"] = cluster_profile["Total_Spending"].round(0)
    cluster_profile["Total_Purchases"] = cluster_profile["Total_Purchases"].round(1)
    cluster_profile["Age"] = cluster_profile["Age"].round(1)

    # Dynamic Persona Naming based on relative Spending and Income ranks
    mean_spend_overall = df_work["Total_Spending"].mean()
    mean_inc_overall = df_work["Income"].mean()
    
    persona_names = {}
    for _, row in cluster_profile.iterrows():
        c = int(row["Cluster"])
        inc = row["Income"]
        spd = row["Total_Spending"]
        
        if spd > mean_spend_overall and inc > mean_inc_overall:
            persona_names[c] = "Affluent Champions"
        elif spd > mean_spend_overall and inc <= mean_inc_overall:
            persona_names[c] = "High-Value Enthusiasts"
        elif spd <= mean_spend_overall and inc > mean_inc_overall:
            persona_names[c] = "Cautious Savers"
        else:
            persona_names[c] = "Budget Seekers"

    # Ensure unique names if multiple fall in same category
    used = set()
    for c in list(persona_names.keys()):
        base_name = persona_names[c]
        if base_name in used:
            persona_names[c] = f"{base_name} ({c})"
        used.add(persona_names[c])

    df_work["Segment_Name"] = df_work["Cluster"].map(persona_names)
    cluster_profile["Segment_Name"] = cluster_profile["Cluster"].map(persona_names)

    metrics = {
        "n_clusters": n_clusters,
        "inertia": float(kmeans.inertia_),
        "silhouette_score": round(sil_score, 4),
        "persona_map": persona_names
    }

    return df_work, cluster_profile, metrics
