# MARKETIX: An Intelligent Marketing Analytics and Customer Insights Platform

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20SQLite-336791.svg)](https://www.postgresql.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![ReportLab](https://img.shields.io/badge/Reports-PDF%20Generation-green.svg)](https://www.reportlab.com/)

MARKETIX is an industrial-grade marketing analytics and customer insights platform developed in Python. Designed for real-world business use cases, academic evaluations (B.Tech 3rd-Year Industrial Training), and viva demonstrations, MARKETIX empowers businesses to analyze multi-wave marketing campaigns, uncover demographic drivers of spending, segment customers using unsupervised Machine Learning (**K-Means**), and predict campaign response probabilities using supervised Machine Learning (**Logistic Regression**).

---

## 1. Project Overview & Business Value

### 1.1 The Business Problem
Modern enterprises spend massive capital across digital, direct mail, email, and catalog marketing campaigns. However, marketing decision-makers face persistent obstacles:
- **Wasted Ad Spend:** Broadcasting offers uniformly to uninterested prospects.
- **Unclear Campaign Efficacy:** Difficulty benchmarking conversion across multi-wave campaigns.
- **Fragmented Insights:** Inability to isolate how customer purchasing habits, income, and household structures influence response propensities.

### 1.2 The MARKETIX Solution
MARKETIX unifies raw marketing data into an end-to-end intelligence pipeline:
1. **Executive Dashboard:** Live metrics for total customers (2,240), campaigns (5), responses (334), response rate (14.91%), average income ($52,243), and spending ($605.80).
2. **Data Management:** File ingestion (CSV/Excel), schema profiling, missing value imputation, and anomaly treatment.
3. **Campaign Analysis:** Multi-wave performance benchmarking and purchase channel breakdown.
4. **Customer Insights:** Demographic distributions, spending tiers, and product category affinities.
5. **Customer Segmentation:** K-Means clustering with Elbow Method and Silhouette diagnostics.
6. **Response Prediction:** Balanced Logistic Regression model with interactive inference, batch scoring, and ROC evaluation (AUC > 0.90).
7. **Business Recommendations:** Rule-based consulting suggestions distinguishing correlation from causation.
8. **Reports & Exports:** Automated PDF executive summaries and CSV exports.

---

## 2. System Architecture

```text
                   USER
                     |
                     v
        +---------------------------+
        |       PRESENTATION        |
        |                           |
        |       Streamlit UI        |
        |                           |
        |  1. Dashboard             |
        |  2. Data Management       |
        |  3. Campaign Analysis     |
        |  4. Customer Insights     |
        |  5. Customer Segmentation |
        |  6. ML Prediction         |
        |  7. Recommendations       |
        |  8. Reports               |
        +---------------------------+
                     |
                     v
        +---------------------------+
        |    APPLICATION LAYER      |
        |                           |
        |  Data Upload              |
        |  Data Validation          |
        |  Data Cleaning            |
        |  Business Logic           |
        |  Analytics Engine         |
        +---------------------------+
                     |
          +----------+----------+
          |                     |
          v                     v
+-------------------+  +----------------------+
|  DATABASE LAYER   |  |  MACHINE LEARNING    |
|                   |  |                      |
|  PostgreSQL       |  |  Logistic Regression |
|  Customer Data    |  |  K-Means Clustering  |
|  Campaign Data    |  |  Model Evaluation    |
|  Response Data    |  |  Predictions         |
+-------------------+  +----------------------+
          |                     |
          +----------+----------+
                     |
                     v
        +---------------------------+
        |   VISUALIZATION LAYER     |
        |                           |
        |  Interactive Charts       |
        |  Plotly Visualizations    |
        |  KPI Summary Cards        |
        +---------------------------+
                     |
                     v
        +---------------------------+
        |     OUTPUT LAYER          |
        |                           |
        |  Business Insights        |
        |  Strategic Action Steps   |
        |  CSV Exports              |
        |  PDF Executive Briefs     |
        +---------------------------+
```

---

## 3. Technology Stack

| Layer | Technology | Role & Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.13 | Core programming language |
| **Web Framework** | Streamlit | Reactive multi-page user interface |
| **Data Processing** | Pandas, NumPy | Data cleaning, imputation, and domain feature engineering |
| **Visualization** | Plotly | Interactive responsive business charts |
| **Machine Learning** | Scikit-learn, Joblib | Unsupervised K-Means and supervised Logistic Regression |
| **Relational Database** | PostgreSQL & SQLite | Relational schema persistence with graceful offline fallback |
| **ORM / Connectivity** | SQLAlchemy, Psycopg2 | Database connection management and connection health checks |
| **Reporting** | ReportLab | High-resolution PDF executive brief generation |

---

## 4. Directory Structure

```text
MARKETIX/
├── app.py                      # Main application entry point & system health
├── pages/
│   ├── 1_Dashboard.py          # Module 1: Executive KPI Dashboard
│   ├── 2_Data_Management.py    # Module 2: Ingestion, Validation & Cleaning
│   ├── 3_Campaign_Analysis.py  # Module 3: Campaign Benchmarking & Channels
│   ├── 4_Customer_Insights.py  # Module 4: Demographics, Tiers & Product Affinity
│   ├── 5_Customer_Segmentation.py # Module 5: K-Means Clustering & Personas
│   ├── 6_Response_Prediction.py# Module 6: Logistic Regression Response Predictor
│   ├── 7_Recommendations.py    # Module 7: Strategic Consulting Action Steps
│   └── 8_Reports.py            # Module 8: PDF Report & CSV Exports
├── database/
│   ├── connection.py           # Robust DB connection manager & fallback
│   ├── schema.sql              # PostgreSQL DDL schema with 6 tables
│   └── queries.py              # SQL queries and synchronization routines
├── src/
│   ├── data_loader.py          # Auto-detecting CSV & Excel loader
│   ├── data_cleaning.py        # Median imputation & domain feature engineering
│   ├── analytics.py            # KPI calculation & breakdown engines
│   ├── campaign_analysis.py    # Campaign metrics & channel analysis
│   ├── customer_analysis.py    # Demographic distributions & tier analysis
│   ├── visualizations.py       # Stylized Plotly charts
│   └── recommendations.py      # Rule-based business recommendation engine
├── ml/
│   ├── train_model.py          # Stratified train/test split & model training
│   ├── predict.py              # Single & batch inference engine
│   ├── segmentation.py         # K-Means clustering & elbow evaluation
│   ├── evaluate.py             # Model performance metrics & ROC calculation
│   └── saved_models/           # Serialized joblib artifacts
├── data/
│   ├── raw/                    # Raw marketing_campaign.csv dataset
│   └── processed/              # Cleaned marketing dataset
├── reports/
│   └── generator.py            # ReportLab PDF executive brief generator
├── assets/
│   └── logo.png                # Platform branding asset
├── requirements.txt            # Python dependencies
├── .env                        # Database connection settings
├── .gitignore                  # Git hygiene configuration
└── README.md                   # Complete documentation
```

---

## 5. Setup & Installation Guide

### Prerequisites
- Python 3.13 installed
- Git installed
- PostgreSQL (optional; local SQLite fallback is built-in)

### 1. Clone & Enter Project Directory
```bash
cd "/Users/kamaldeepsingh/Desktop/summer project/MARKETIX"
```

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database (Optional)
Configure database credentials in `.env`:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=marketix
DB_USER=postgres
DB_PASSWORD=postgres
SQLITE_DB_PATH=database/marketix.db
```
*Note: If PostgreSQL is not active, MARKETIX automatically runs on embedded SQLite without interrupting the application.*

### 5. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 6. Certificate Connections (Viva & Report Ready)

| Certification | Application in MARKETIX |
| :--- | :--- |
| **BCG X – Introduction to Data for Decision Makers** | Module 3 & Module 7: Translating analytical findings into strategic decision-making frameworks, customer lifetime value retention, and distinguishing correlation from causation. |
| **IBM – Data Analysis with Python** | Module 2 & Module 4: Ingesting datasets, handling missing values via median imputation, exploratory data analysis (EDA), and demographic grouping. |
| **Deloitte – Data Analytics Job Simulation** | Module 5 & Module 6: Customer persona segmentation (K-Means), response propensity modeling (Logistic Regression), and executive PDF reporting for corporate stakeholders. |
