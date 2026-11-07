# MARKETIX: Project Presentation Slide Deck (8–10 Slides)

**Official Title:** MARKETIX: An Intelligent Marketing Analytics and Customer Insights Platform Using Python and Machine Learning  
**Target:** B.Tech 3rd-Year Industrial Training Project Presentation / Viva Defense  
**Author:** Kamandeep Singh  

---

## Slide 1: Title & Overview
- **Header:** MARKETIX
- **Sub-header:** An Intelligent Marketing Analytics and Customer Insights Platform Using Python and Machine Learning
- **Student Details:** Kamandeep Singh | B.Tech Computer Science & Engineering (3rd Year)
- **Industry Training Alignment:** BCG X (Decision Analytics), IBM (Data Analysis with Python), Deloitte (Data Analytics Simulation)
- **Key Visual:** System architecture badge, Python & Streamlit logos.

> **Presenter Notes (Viva):**
> *"Good morning, respected professors and evaluation committee. Today, I am presenting MARKETIX, an industrial-grade marketing intelligence platform designed to bridge the gap between complex machine learning pipelines and actionable business decision-making. This project consolidates my industrial training learnings with practical business use cases."*

---

## Slide 2: Problem Statement & Motivation
- **The Challenge in Marketing Today:**
  1. **Marketing Budget Wastage:** Organizations send blanket promotional campaigns to entire customer bases with low conversion (<15%).
  2. **Fragmented Customer Data:** Inability to isolate demographic and behavioral patterns across multiple product lines (Wines, Meat, Gold, etc.).
  3. **Lack of Predictive Propensity:** Difficulty in anticipating which prospects are likely to respond before committing campaign funds.
  4. **Complex Dashboards:** Many enterprise tools require heavy, slow web stacks (React/FastAPI) that add engineering overhead without extra analytical value.
- **Project Goal:** Build a unified, data-driven analytics and ML platform that provides multi-wave campaign benchmarking, customer segmentation, and response prediction.

> **Presenter Notes (Viva):**
> *"Businesses spend heavily on marketing, yet response rates often stay below 15%. Without predictive analytics, companies waste capital on low-intent prospects. MARKETIX addresses this by providing end-to-end data cleaning, unsupervised segmentation, and supervised conversion likelihood scoring."*

---

## Slide 3: System Architecture (Layered Design)
- **Five-Layer Enterprise Architecture:**
  1. **Presentation Layer:** Multi-page Streamlit web application (8 specialized functional modules).
  2. **Application & Analytics Layer:** Python modules for data loading, validation, median imputation, and domain feature engineering.
  3. **Database Layer:** Dual-mode persistence—PostgreSQL schema with automatic local SQLite fallback for offline resilience.
  4. **Machine Learning Layer:** Unsupervised K-Means clustering + Supervised Logistic Regression.
  5. **Output Layer:** Interactive Plotly visualisations, CSV exports, and automated ReportLab PDF reports.

> **Presenter Notes (Viva):**
> *"I chose a decoupled layered architecture. Rather than introducing separate frontend and backend servers, Streamlit connects directly with our Python analytics and ML modules. This eliminates latency, simplifies deployment, and adheres strictly to corporate data engineering principles."*

---

## Slide 4: Dataset & Data Engineering Pipeline
- **Dataset Source:** Customer Personality Analysis (2,240 customers, 29 attributes).
- **Data Quality Issues Resolved:**
  - **Income Nulls:** 24 missing values resolved via *Education-stratified median imputation*.
  - **Chronological Outliers:** Birth years < 1920 (ages > 100) detected and capped.
  - **Categorical Anomalies:** Normalized non-standard marital statuses (`Alone`, `Absurd`, `YOLO` $\to$ `Single`).
- **Domain Feature Engineering:**
  - $\text{Total Spending} = \text{Wines} + \text{Fruits} + \text{Meat} + \text{Fish} + \text{Sweets} + \text{Gold}$
  - $\text{Total Purchases} = \text{Deals} + \text{Web} + \text{Catalog} + \text{Store}$
  - $\text{Customer Tenure} = \text{Days active relative to latest cohort date}$

> **Presenter Notes (Viva):**
> *"Real-world data is inherently imperfect. In our pipeline, we did not simply drop rows with missing income; we applied median imputation conditioned on the customer's education tier. We also engineered domain KPIs that serve as critical features for our machine learning models."*

---

## Slide 5: Multi-Wave Campaign Performance Analysis
- **Benchmark Across 6 Campaigns:**
  - Campaign 1 (Direct Email): 6.43% conversion
  - Campaign 2 (Direct Mail): 1.34% conversion
  - Campaign 3 (Voucher): 7.28% conversion
  - Campaign 4 (Catalog Special): 7.46% conversion
  - Campaign 5 (Premium Club): 7.28% conversion
  - **Latest Campaign (Integrated Multi-Channel):** **14.91% conversion (334 positive responses)**
- **Response Rate Formula:**
  $$\text{Response Rate} = \frac{\text{Positive Responses}}{\text{Customers Contacted}} \times 100$$
- **Omnichannel Breakdown:** In-store purchases lead overall volume, while direct catalog sales demonstrate high conversion efficiency among affluent segments.

> **Presenter Notes (Viva):**
> *"Analyzing multi-wave campaign performance revealed wide variance: the latest integrated campaign performed over 11x better than Campaign 2. This empirical evidence validates the need for omnichannel alignment."*

---

## Slide 6: Customer Segmentation (Unsupervised K-Means)
- **Algorithm:** K-Means Clustering with `StandardScaler` feature normalization.
- **Hyperparameter Selection:**
  - Evaluated **Elbow Method (Inertia)** and **Silhouette Scores** across $K = 2 \dots 6$.
  - Selected **$K = 4$** clusters yielding the highest intra-cluster cohesion.
- **Identified Customer Personas:**
  1. **Affluent Champions:** High Income ($75k+), High Total Spending ($1,200+), High Campaign Acceptance.
  2. **Budget Seekers:** Low Income (<$35k), Low Spending (<$100), frequent discount deal shoppers.
  3. **Cautious Savers:** Moderate-to-high income with low discretionary category spending.
  4. **High-Value Enthusiasts:** Young cohorts with high digital web visit engagement and catalog affinity.

> **Presenter Notes (Viva):**
> *"For unsupervised segmentation, we used K-Means. Rather than guessing the number of clusters, we ran an automated Elbow Curve and Silhouette evaluation. Each cluster is automatically mapped to an actionable marketing persona with tailored communication strategies."*

---

## Slide 7: Campaign Response Prediction (Supervised ML)
- **Algorithm:** Balanced Logistic Regression (`class_weight='balanced'`).
- **Data Leakage Prevention:** Strict isolation of target response and exclusion of post-campaign attributes.
- **Holdout Validation:** Stratified 80/20 train/test split.
- **Model Performance Metrics:**
  - **ROC-AUC Score:** **0.901** (exceptional discriminatory capability)
  - **Recall (Sensitivity):** **77.6%** on positive responses (captures over $\frac{3}{4}$ of responders)
  - **Overall Accuracy:** **82.4%**
- **Top Feature Drivers:**
  1. Customer Tenure (days enrolled)
  2. Historical response to Campaign 3 & 5
  3. Spending on Meat & Wine products
  4. Advanced Education (PhD / Master)

> **Presenter Notes (Viva):**
> *"Marketing campaign data suffers from natural class imbalance: only 14.9% of customers responded. Standard models often predict all zeros to achieve high accuracy while failing completely at identification. By utilizing balanced class weighting in Logistic Regression, we achieved a 77.6% recall and a 0.901 ROC-AUC score."*

---

## Slide 8: Business Recommendations & ReportLab Exports
- **Consulting Recommendation Framework (BCG X & Deloitte):**
  - **VIP Retention:** Top-quartile spenders convert at 3.2x the baseline rate; recommendations prioritize loyalty concierges over discounts.
  - **Cross-Selling Anchor:** Wine and Meat generate over 75% of catalog revenue; recommendations trigger automated bundle promotions.
  - **Distinguishing Correlation from Causation:** Highlights the necessity of controlled A/B split tests before high-cost mass mailings.
- **Automated Outputs:**
  - Dynamic generation of **official executive PDF reports** using ReportLab.
  - One-click CSV exports of cleaned datasets, segmentation clusters, and scored predictions.

> **Presenter Notes (Viva):**
> *"Data is only valuable if it drives action. MARKETIX includes a rule-based consulting engine that provides prioritized recommendations with expected business impacts, paired with an executive PDF generator for corporate stakeholders."*

---

## Slide 9: Connection with Certifications & Academic Rigour
- **BCG X – Introduction to Data for Decision Makers:**
  - Applied directly in Module 3 & Module 7: Translating data into strategic decisions, computing customer acquisition efficiencies, and communicating findings.
- **IBM – Data Analysis with Python:**
  - Applied in Module 2 & Module 4: Rigorous pandas operations, data validation, median imputation, and demographic exploratory data analysis.
- **Deloitte – Data Analytics Job Simulation:**
  - Applied in Modules 5, 6 & 8: Unsupervised clustering, predictive propensity modeling, and executive-level reporting.

> **Presenter Notes (Viva):**
> *"This project is directly anchored in the skills gained through my BCG X, IBM, and Deloitte certifications, demonstrating theoretical understanding alongside industrial software engineering execution."*

---

## Slide 10: Conclusion & Live Demonstration
- **Summary of Achievements:**
  - Complete full-stack analytics platform built in Python 3.13.
  - Functional PostgreSQL relational schema with offline SQLite resilience.
  - 8 fully functional Streamlit modules.
  - Supervised and unsupervised machine learning models validated with academic rigor.
  - Production-ready PDF report generation.
- **Live Demo Flow:**
  1. Executive Dashboard (live KPIs & Plotly charts)
  2. Data Management (cleaning pipeline & database sync)
  3. Segmentation (interactive K-Means slider & personas)
  4. Response Prediction (interactive form calculation)
  5. Executive PDF Export (one-click download)
- **Questions & Answers:** Thank you! Opening the floor to the evaluation panel.
