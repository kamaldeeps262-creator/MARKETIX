# MARKETIX: Viva Defense Questions & Answers Guide

This guide prepares you for questions commonly asked by external examiners, faculty supervisors, and technical reviewers during your B.Tech 3rd-year industrial training viva.

---

## 1. Architecture & Technology Stack Questions

### Q1: Why did you choose Streamlit instead of React + FastAPI?
**Answer:**
> *"In marketing analytics and data science, rapid iteration and unified state management are critical. Building separate React frontend and FastAPI backend applications would introduce unnecessary network serialization latency, redundant boilerplate code, and CORS complexities without improving analytical fidelity. Streamlit allowed us to write end-to-end Python code that connects directly to Pandas, Scikit-learn, SQLAlchemy, and Plotly, resulting in an industrial-grade, interactive application that is maintainable, responsive, and easy to deploy."*

### Q2: How does your database layer handle connectivity issues?
**Answer:**
> *"The database layer in `database/connection.py` implements a resilient dual-mode pattern. It first attempts to connect to the production PostgreSQL server specified in `.env`. If PostgreSQL is offline or running in a sandboxed/restricted environment, it gracefully falls back to an embedded SQLite database (`database/marketix.db`). The web interface displays a live status badge informing the user whether PostgreSQL or SQLite is currently active. This ensures the platform never crashes during live demonstrations while maintaining strict relational schema integrity across all 6 tables."*

---

## 2. Data Engineering & Preprocessing Questions

### Q3: How did you handle missing values in the dataset? Why not just drop them?
**Answer:**
> *"The raw dataset had 24 missing values in the `Income` column. In commercial marketing, dropping records reduces sample size and introduces demographic bias (for instance, if high-income or younger customers systematically skip reporting income). Instead of basic mean imputation—which distorts the variance—we implemented **Education-stratified median imputation**. We computed the median income for each education tier (`PhD`, `Master`, `Graduation`, etc.) and imputed missing values based on the customer's specific group. This preserves the underlying demographic relationship between education level and earning potential."*

### Q4: What feature engineering did you perform, and why?
**Answer:**
> *"We engineered several domain-specific marketing KPIs:
> 1. `Total_Spending`: Aggregated spend across the 6 individual product lines (Wines, Fruits, Meat, Fish, Sweets, Gold).
> 2. `Total_Purchases`: Summed transactions across Store, Web, Catalog, and Deal purchases.
> 3. `Children` & `Is_Parent`: Combined `Kidhome` and `Teenhome` into household composition flags.
> 4. `Customer_Tenure_Days`: Calculated the number of days a customer has been enrolled relative to the dataset reference date.
> These engineered features significantly enhanced the explanatory power and ROC-AUC of our predictive models."*

---

## 3. Machine Learning Questions

### Q5: Why did you choose Logistic Regression for campaign response prediction instead of a complex ensemble like XGBoost or Random Forest?
**Answer:**
> *"For a B.Tech 3rd-year industrial training project, model interpretability, coefficient explainability, and regulatory compliance are paramount. Logistic Regression provides:
> 1. Direct mathematical odds ratios (coefficients) that explain *why* a customer is predicted to respond.
> 2. Calibrated probability estimates rather than arbitrary tree scores.
> 3. Fast execution without hyperparameter overfitting on a dataset of 2,240 records.
> Furthermore, with balanced class weighting and standard scaling, our Logistic Regression model achieved an outstanding **ROC-AUC of 0.901** and a **Recall of 77.6%**, proving that a well-engineered linear model often outperforms complex black-box models on tabular customer data."*

### Q6: Marketing campaign responses are heavily imbalanced (~14.9% positive). How did you address this class imbalance?
**Answer:**
> *"If an unweighted model is trained on this data, it will achieve ~85% accuracy by simply predicting that nobody will respond, which is useless for a marketing team. We addressed this by:
> 1. Using a **stratified train/test split** (80/20) to ensure identical class distributions in training and validation sets.
> 2. Setting `class_weight='balanced'` in `LogisticRegression`, which inversely weights errors in the minority class proportional to class frequencies.
> 3. Evaluating the model using **Recall (Sensitivity)** and **ROC-AUC** rather than accuracy alone, ensuring high detection of true positive responders."*

### Q7: How does K-Means determine the number of clusters, and how did you prevent arbitrary labeling?
**Answer:**
> *"Instead of picking an arbitrary number of clusters, our platform executes diagnostic evaluation using two quantitative metrics:
> 1. **The Elbow Method (WCSS Inertia):** Identifies the point of diminishing returns where adding more clusters no longer significantly reduces within-cluster variance.
> 2. **Silhouette Score:** Measures intra-cluster cohesion versus inter-cluster separation across $K = 2 \dots 6$.
> After selecting the optimal $K=4$, our algorithm automatically calculates each cluster's centroid relative to the dataset averages and assigns meaningful business personas: *Affluent Champions*, *Budget Seekers*, *Cautious Savers*, and *High-Value Enthusiasts*."*

---

## 4. Business & Certifications Alignment Questions

### Q8: How does MARKETIX connect to your BCG X, IBM, and Deloitte certificates?
**Answer:**
> *"MARKETIX was built specifically to synthesize the skills acquired from these certifications:
> - **BCG X (Introduction to Data for Decision Makers):** Implemented in Module 3 (Campaign Benchmarking) and Module 7 (Strategic Recommendations), where we communicate analytical findings through executive frameworks and distinguish correlation from causation.
> - **IBM (Data Analysis with Python):** Implemented in Module 2 (Data Management) and Module 4 (Customer Insights) through advanced Pandas data cleaning, groupby operations, and demographic analysis.
> - **Deloitte (Data Analytics Job Simulation):** Implemented in Modules 5, 6, and 8 via unsupervised segmentation, supervised response propensity scoring, and ReportLab executive PDF brief generation."*

### Q9: Can this platform calculate ROI (Return on Investment)?
**Answer:**
> *"In the Customer Personality Analysis dataset, columns `Z_CostContact` (constant value 3) and `Z_Revenue` (constant value 11) are static placeholders rather than true variable marketing costs and product margins. Following ethical data analytics standards (emphasized in BCG X), we do not display speculative ROI calculations without verified campaign spend and revenue data. Instead, we measure true empirical metrics: **Response Rate**, **Conversion Share**, and **Category Spend Premium**."*
