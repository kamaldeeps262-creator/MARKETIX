"""
MARKETIX Visualization Module
Provides elegant, interactive Plotly visualizations with professional styling
tailored for executive presentations and academic evaluation.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Professional corporate theme color palette
PRIMARY_COLOR = "#1E3A8A"  # Deep Royal Blue
SECONDARY_COLOR = "#0D9488" # Teal
ACCENT_COLOR = "#F59E0B"    # Amber Gold
DANGER_COLOR = "#EF4444"    # Coral Red
SUCCESS_COLOR = "#10B981"   # Emerald Green
PALETTE = ["#1E3A8A", "#0D9488", "#F59E0B", "#8B5CF6", "#EC4899", "#3B82F6"]


def plot_campaign_comparison(df_summary: pd.DataFrame) -> go.Figure:
    """Creates a stylized bar chart comparing campaign acceptance rates."""
    df_sorted = df_summary.sort_values(by="Response_Rate", ascending=True)
    
    # Highlight highest bar
    colors = [
        ACCENT_COLOR if r == df_sorted["Response_Rate"].max() else PRIMARY_COLOR
        for r in df_sorted["Response_Rate"]
    ]

    fig = go.Figure(go.Bar(
        x=df_sorted["Response_Rate"],
        y=df_sorted["Campaign_Name"],
        orientation="h",
        marker_color=colors,
        text=[f"{r:.1f}% ({p} responses)" for r, p in zip(df_sorted["Response_Rate"], df_sorted["Positive_Responses"])],
        textposition="outside",
        cliponaxis=False
    ))

    fig.update_layout(
        title="<b>Campaign Acceptance Rate Comparison</b>",
        xaxis_title="Acceptance Rate (%)",
        yaxis_title="",
        template="plotly_white",
        height=380,
        margin=dict(l=10, r=40, t=50, b=40),
    )
    return fig


def plot_spend_donut(spend_df: pd.DataFrame) -> go.Figure:
    """Generates an interactive donut chart of spending across product lines."""
    fig = go.Figure(data=[go.Pie(
        labels=spend_df["Category"],
        values=spend_df["Total_Spending"],
        hole=0.45,
        marker=dict(colors=PALETTE),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Total: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title="<b>Product Category Spending Share</b>",
        template="plotly_white",
        height=380,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig


def plot_income_vs_spending(df: pd.DataFrame) -> go.Figure:
    """Creates an interactive scatter plot showing the relationship between income and spend."""
    sample_df = df.sample(min(1000, len(df)), random_state=42) if len(df) > 1000 else df
    
    fig = px.scatter(
        sample_df,
        x="Income",
        y="Total_Spending",
        color="Response",
        color_discrete_map={0: "#94A3B8", 1: "#10B981"},
        labels={"Response": "Accepted Campaign", "Total_Spending": "Total Spending ($)", "Income": "Customer Income ($)"},
        title="<b>Customer Income vs Total Spending (By Campaign Response)</b>",
        hover_data=["Age", "Education", "Total_Purchases"] if "Age" in sample_df.columns else None,
        template="plotly_white",
        opacity=0.75
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=40))
    return fig


def plot_channel_comparison(channel_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart comparing channel transaction shares."""
    x_col = "Total_Purchases" if "Total_Purchases" in channel_df.columns else "Total_Transactions"
    fig = px.bar(
        channel_df,
        x=x_col,
        y="Channel",
        orientation="h",
        color="Channel",
        color_discrete_sequence=PALETTE,
        title="<b>Total Purchases by Acquisition Channel</b>",
        text=x_col,
        template="plotly_white"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, showlegend=False, margin=dict(l=20, r=40, t=50, b=30))
    return fig


def plot_segment_scatter(df_segmented: pd.DataFrame) -> go.Figure:
    """Generates an interactive scatter plot showing K-Means cluster separation."""
    color_col = "Segment_Name" if "Segment_Name" in df_segmented.columns else "Cluster"
    
    fig = px.scatter(
        df_segmented,
        x="Income",
        y="Total_Spending",
        color=color_col,
        color_discrete_sequence=PALETTE,
        title="<b>Customer Segmentation (K-Means Clusters)</b>",
        hover_data=["Total_Purchases", "NumWebVisitsMonth", "Age"] if "Total_Purchases" in df_segmented.columns else None,
        template="plotly_white",
        opacity=0.8
    )
    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig


def plot_confusion_matrix(cm: np.ndarray, labels=["No Response", "Responded"]) -> go.Figure:
    """Generates a styled heatmap for the classification confusion matrix."""
    fig = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Predicted Label", y="Actual Label", color="Count"),
        x=labels,
        y=labels,
        color_continuous_scale="Blues",
        title="<b>Model Evaluation: Confusion Matrix</b>"
    )
    fig.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=30))
    return fig


def plot_roc_curve(fpr, tpr, roc_auc: float) -> go.Figure:
    """Generates the ROC curve with area under the curve annotation."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f"Logistic Regression (AUC = {roc_auc:.3f})", line=dict(color=PRIMARY_COLOR, width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name="Random Chance", line=dict(color="grey", dash="dash")))

    fig.update_layout(
        title="<b>Receiver Operating Characteristic (ROC) Curve</b>",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=50, b=30),
        legend=dict(x=0.55, y=0.1)
    )
    return fig
