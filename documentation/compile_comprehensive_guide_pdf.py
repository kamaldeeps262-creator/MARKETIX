"""
MARKETIX PDF Comprehensive Guide Compiler
Generates a formal, beautiful multi-page PDF document covering:
1. Executive Overview & Architecture
2. Function-by-Function Technical Reference
3. Step-by-Step Usage Guide with Concrete Examples
4. Faculty Presentation Script & 7-Minute Viva Guide
5. Viva Defense Q&A & Certificate Connections
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import datetime

OUTPUT_DIR = Path(__file__).resolve().parent
PDF_PATH = OUTPUT_DIR / "MARKETIX_Complete_Project_Guide_and_Viva_Presentation.pdf"


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and page numbers dynamically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            # Header
            self.drawString(40, 755, "MARKETIX: Intelligent Marketing Analytics Platform — Comprehensive Guide & Viva Handbook")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 750, 572, 750)
            # Footer
            self.line(40, 42, 572, 42)
            self.drawString(40, 30, "B.Tech 3rd-Year Industrial Training | Verified with BCG X, IBM, Deloitte")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(572, 30, page_text)
            self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Color definitions
    c_primary = colors.HexColor("#1E3A8A")   # Deep Royal Blue
    c_secondary = colors.HexColor("#0D9488") # Teal
    c_accent = colors.HexColor("#F59E0B")    # Amber
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_body = colors.HexColor("#334155")      # Slate 700
    c_light_bg = colors.HexColor("#F8FAFC")  # Light gray-blue
    c_border = colors.HexColor("#E2E8F0")

    # Typography styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=14
    )

    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        "H1Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "H2Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=c_body,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=body_style,
        leftIndent=14,
        bulletIndent=4,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E40AF")
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.whitesmoke,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell_style,
        fontName="Helvetica-Bold",
        textColor=c_primary
    )

    story = []

    # ══════════════════════════════════════════════════════════
    # COVER / HEADER
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("MARKETIX", title_style))
    story.append(Paragraph("An Intelligent Marketing Analytics and Customer Insights Platform Using Python and Machine Learning", subtitle_style))
    story.append(Paragraph(
        "<b>Student:</b> Kamandeep Singh | <b>Academic Level:</b> B.Tech CSE 3rd Year (Industrial Training Project)<br/>"
        "<b>Certification Integrations:</b> BCG X (Decision Analytics), IBM (Data Analysis with Python), Deloitte (Job Simulation)<br/>"
        f"<b>Generated:</b> {datetime.datetime.now().strftime('%B %d, %Y')} | <b>Platform Architecture:</b> Decoupled Layered Architecture (Streamlit + PostgreSQL + Scikit-Learn)",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=10))

    # ══════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY & REAL-WORLD STORY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(Paragraph(
        "Modern businesses face high customer acquisition costs (CAC). Organizations frequently broadcast promotional offers "
        "across email, SMS, and direct mail indiscriminately. In typical commercial retail datasets, <b>only ~14.9% of prospects convert</b>, "
        "meaning 85% of marketing expenditure is wasted on uninterested prospects. "
        "<b>MARKETIX</b> solves this problem through an end-to-end intelligence engine that unifies data cleaning, unsupervised persona discovery, "
        "and supervised response propensity scoring into a single interactive platform.",
        body_style
    ))

    # Architecture Box Table
    arch_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology Stack", table_header_style), Paragraph("Core Industrial Responsibility", table_header_style)],
        [Paragraph("1. Presentation", table_cell_bold), Paragraph("Streamlit, HTML5, CSS3 Animations", table_cell_style), Paragraph("8 modular interactive web views, KPI cards, real-time filters, Plotly dashboards.", table_cell_style)],
        [Paragraph("2. Application", table_cell_bold), Paragraph("Python 3.13, Pandas, NumPy", table_cell_style), Paragraph("Data ingestion, validation, median imputation, and domain feature engineering.", table_cell_style)],
        [Paragraph("3. Database", table_cell_bold), Paragraph("PostgreSQL 16 & SQLite Fallback", table_cell_style), Paragraph("6 relational tables, transactional sync, foreign keys, and offline resilience.", table_cell_style)],
        [Paragraph("4. Machine Learning", table_cell_bold), Paragraph("Scikit-Learn, Joblib", table_cell_style), Paragraph("Unsupervised K-Means clustering (K=4) + Supervised balanced Logistic Regression (AUC 0.901).", table_cell_style)],
        [Paragraph("5. Output / Delivery", table_cell_bold), Paragraph("ReportLab, Plotly, CSV", table_cell_style), Paragraph("Executive PDF briefs, Plotly charts, prioritized consulting action steps, CSV exports.", table_cell_style)],
    ]
    t_arch = Table(arch_data, colWidths=[80, 160, 292])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════
    # 2. FUNCTION-BY-FUNCTION TECHNICAL REFERENCE
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("2. Function-by-Function Technical Reference", h1_style))
    story.append(Paragraph("Comprehensive documentation of every core function across the codebase:", body_style))

    fn_data = [
        [Paragraph("Module / File", table_header_style), Paragraph("Function Name & Signature", table_header_style), Paragraph("Inputs & Logic", table_header_style), Paragraph("Return Value & Output", table_header_style)],
        # Data Loader
        [Paragraph("src/data_loader.py", table_cell_bold), Paragraph("load_dataset(file_or_path)", table_cell_style), Paragraph("Detects comma, semicolon, tab or Excel formats.", table_cell_style), Paragraph("Tuple: (DataFrame, status_msg)", table_cell_style)],
        [Paragraph("src/data_loader.py", table_cell_bold), Paragraph("get_dataset_summary(df)", table_cell_style), Paragraph("Computes rows, columns, nulls, duplicates, and MBs.", table_cell_style), Paragraph("Dict: data health metrics", table_cell_style)],
        # Data Cleaning
        [Paragraph("src/data_cleaning.py", table_cell_bold), Paragraph("clean_marketing_data(df)", table_cell_style), Paragraph("Imputes Income with education median; caps ages > 100; normalizes status; creates Total_Spending & Tenure.", table_cell_style), Paragraph("Tuple: (Cleaned_DF, report_dict)", table_cell_style)],
        # Analytics
        [Paragraph("src/analytics.py", table_cell_bold), Paragraph("compute_kpis(df)", table_cell_style), Paragraph("Calculates Customers, Campaigns, Responses, Response Rate, Avg Income, Avg Spending.", table_cell_style), Paragraph("Dict: executive dashboard KPIs", table_cell_style)],
        [Paragraph("src/analytics.py", table_cell_bold), Paragraph("compute_category_spend_breakdown(df)", table_cell_style), Paragraph("Aggregates spend across Wines, Meat, Gold, Fish, Sweets, and Fruits.", table_cell_style), Paragraph("DataFrame: category revenue share", table_cell_style)],
        [Paragraph("src/analytics.py", table_cell_bold), Paragraph("compute_purchase_channel_breakdown(df)", table_cell_style), Paragraph("Sums purchases across Store, Web, Catalog, Deals.", table_cell_style), Paragraph("DataFrame: channel volume & shares", table_cell_style)],
        # Campaign Analysis
        [Paragraph("src/campaign_analysis.py", table_cell_bold), Paragraph("analyze_campaign_performance(df)", table_cell_style), Paragraph("Benchmarks Campaign 1..5 vs Target Campaign; flags top-converting wave; counts acceptance multiplicity.", table_cell_style), Paragraph("Dict: summary_table, best_campaign, engagement_dist", table_cell_style)],
        [Paragraph("src/campaign_analysis.py", table_cell_bold), Paragraph("analyze_channel_performance(df)", table_cell_style), Paragraph("Analyzes customer transactions across channels.", table_cell_style), Paragraph("DataFrame: channel stats", table_cell_style)],
        # Customer Analysis
        [Paragraph("src/customer_analysis.py", table_cell_bold), Paragraph("analyze_demographics(df)", table_cell_style), Paragraph("Groups age brackets (<35, 35-50, 50-65, 65+); education counts; marital status breakdown.", table_cell_style), Paragraph("Dict: demographic distributions", table_cell_style)],
        [Paragraph("src/customer_analysis.py", table_cell_bold), Paragraph("analyze_spending_by_tier(df)", table_cell_style), Paragraph("Splits Low, Moderate, High spenders; checks conversion rate across tiers (proves 3x lift).", table_cell_style), Paragraph("DataFrame: tier conversion rates", table_cell_style)],
        [Paragraph("src/customer_analysis.py", table_cell_bold), Paragraph("analyze_product_affinity(df)", table_cell_style), Paragraph("Compares average category spend between campaign responders and non-responders.", table_cell_style), Paragraph("DataFrame: spend premium (%)", table_cell_style)],
        # Segmentation ML
        [Paragraph("ml/segmentation.py", table_cell_bold), Paragraph("calculate_elbow_and_silhouette(df, max_k)", table_cell_style), Paragraph("Executes K-Means for K=2..7; calculates WCSS inertia and silhouette scores.", table_cell_style), Paragraph("Dict: inertias, silhouettes, optimal_k", table_cell_style)],
        [Paragraph("ml/segmentation.py", table_cell_bold), Paragraph("perform_kmeans_clustering(df, n_clusters)", table_cell_style), Paragraph("StandardScaler normalizes features; fits K-Means; automatically assigns business personas.", table_cell_style), Paragraph("Tuple: (DF_with_clusters, profile_df, metrics)", table_cell_style)],
        # Supervised ML
        [Paragraph("ml/train_model.py", table_cell_bold), Paragraph("train_logistic_regression(df)", table_cell_style), Paragraph("Prevents data leakage; stratified 80/20 split; class_weight='balanced'; evaluates AUC, Recall, F1; persists joblib.", table_cell_style), Paragraph("Dict: metrics, confusion_matrix, roc_curve, coefficients", table_cell_style)],
        [Paragraph("ml/predict.py", table_cell_bold), Paragraph("predict_single_customer(data, threshold)", table_cell_style), Paragraph("Encodes single customer vector; transforms with scaler; evaluates probability.", table_cell_style), Paragraph("Dict: positive/negative probabilities, prediction label", table_cell_style)],
        [Paragraph("ml/predict.py", table_cell_bold), Paragraph("predict_batch_customers(df, threshold)", table_cell_style), Paragraph("Scores all 2,240 records; appends Predicted_Probability and Response_Likelihood.", table_cell_style), Paragraph("DataFrame with appended prediction columns", table_cell_style)],
        # Database
        [Paragraph("database/connection.py", table_cell_bold), Paragraph("test_connection()", table_cell_style), Paragraph("Tests PostgreSQL at localhost:5432; on failure silently routes to SQLite marketix.db.", table_cell_style), Paragraph("SQLAlchemy Engine instance", table_cell_style)],
        [Paragraph("database/queries.py", table_cell_bold), Paragraph("sync_processed_data_to_db(df)", table_cell_style), Paragraph("Synchronizes customers, campaigns definitions, and responses into relational tables.", table_cell_style), Paragraph("Tuple: (bool_success, msg)", table_cell_style)],
        # ReportLab Generator
        [Paragraph("reports/generator.py", table_cell_bold), Paragraph("generate_pdf_report(metrics, cmp, recs)", table_cell_style), Paragraph("Builds high-resolution vector PDF in memory with executive KPI and recommendation tables.", table_cell_style), Paragraph("bytes: downloadable PDF buffer", table_cell_style)],
    ]
    t_fn = Table(fn_data, colWidths=[90, 130, 202, 110])
    t_fn.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_fn)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 3. HOW TO USE MARKETIX WITH CONCRETE EXAMPLES
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("3. Step-by-Step Usage Guide with Concrete Examples", h1_style))

    # Example 1
    story.append(Paragraph("Example 1: Ingesting & Cleaning Real Marketing Data", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Navigate to <i>Module 2: Data Management</i>. Upload a marketing CSV or click the default file.<br/>"
        "• <b>Input Data:</b> Raw CSV with 2,240 records, 24 missing values in Income, anomalous marital statuses ('YOLO', 'Absurd'), and birth years in 1893.<br/>"
        "• <b>Action:</b> Click <i>'🚀 Execute Data Cleaning & Sync to Database'</i>.<br/>"
        "• <b>Outcome:</b> Imputes missing incomes based on Education tier median (e.g. Master median = $50,943), normalizes marital status to 'Single', caps age outliers at the cohort median (56 yrs), and adds engineered metrics (<code>Total_Spending</code>, <code>Customer_Tenure_Days</code>). Records are written to database tables.",
        body_style
    ))

    # Example 2
    story.append(Paragraph("Example 2: Benchmarking Multi-Wave Campaigns", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Navigate to <i>Module 3: Campaign Performance Analysis</i>.<br/>"
        "• <b>Data:</b> Multi-wave campaigns (Campaign 1: 6.43%, Campaign 2: 1.34%, Campaign 3: 7.28%, Campaign 4: 7.46%, Campaign 5: 7.28%, Latest Campaign: 14.91%).<br/>"
        "• <b>Business Finding:</b> The Latest Campaign converted at <b>14.91% (334 responses)</b>, outperforming Campaign 2 by more than 11x.<br/>"
        "• <b>Channel Conversion:</b> Reveals that physical store purchases drive total sales volume (5,800+ transactions), but direct catalog mailings produce higher conversion efficiency among affluent households.",
        body_style
    ))

    # Example 3
    story.append(Paragraph("Example 3: Discovering Customer Personas (K-Means)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Navigate to <i>Module 5: Customer Segmentation</i>.<br/>"
        "• <b>Diagnostics:</b> Inspect the Elbow Curve and Silhouette score graph (validating K=4 as optimal).<br/>"
        "• <b>Personas Discovered:</b><br/>"
        "  1. <b>Affluent Champions:</b> Avg Income $75,000+, Total Spend $1,200+, high Wine & Meat spend, 28% campaign response rate.<br/>"
        "  2. <b>Budget Seekers:</b> Avg Income <$35,000, Total Spend <$100, deal-driven, low campaign acceptance (<8%).<br/>"
        "  3. <b>Cautious Savers:</b> Good income ($55k+), moderate spending, requires educational drip email nurturing.<br/>"
        "  4. <b>High-Value Enthusiasts:</b> Frequent website visitors, high web catalog purchases, responsive to multi-channel promotions.",
        body_style
    ))

    # Example 4
    story.append(Paragraph("Example 4: Scoring Prospect Conversion Probability (Logistic Regression)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Navigate to <i>Module 6: Response Prediction</i>.<br/>"
        "• <b>Case A (High-Intent Prospect):</b> Enter Customer ID 105, Age 45, Income $75,000, Wine Spend $500, Meat Spend $350, Accepted Campaign 1 & 5. Click <i>'Predict'</i>.<br/>"
        "  → <b>Result:</b> <b>78.2% Positive Response Probability</b>. System outputs <i>'✅ LIKELY TO RESPOND'</i> and recommends including in high-touch VIP mailings.<br/>"
        "• <b>Case B (Low-Intent Prospect):</b> Enter Customer ID 210, Income $24,000, Wine Spend $10, No previous campaigns accepted.<br/>"
        "  → <b>Result:</b> <b>8.4% Probability</b>. System outputs <i>'❌ UNLIKELY TO RESPOND'</i> and advises excluding from high-cost direct print mailings to eliminate ad waste.",
        body_style
    ))

    # Example 5
    story.append(Paragraph("Example 5: Automated Consulting Recommendations & PDF Brief Export", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Navigate to <i>Module 7: Recommendations</i> and <i>Module 8: Reports</i>.<br/>"
        "• <b>Strategy Cards:</b> Generates prioritized action items adhering to BCG X / Deloitte frameworks, explicitly separating correlation from causation.<br/>"
        "• <b>One-Click Export:</b> Compiles vector PDF executive reports via ReportLab and generates CSV exports of segmented and scored customers.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════
    # 4. HOW TO PRESENT THIS TO YOUR TEACHER (7-MIN SCRIPT)
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("4. Faculty Presentation Guide: 7-Minute Viva Script", h1_style))
    story.append(Paragraph(
        "Deliver this exact structured presentation during your B.Tech 3rd-year industrial training viva:",
        body_style
    ))

    script_data = [
        [Paragraph("Time & Phase", table_header_style), Paragraph("Screen to Show", table_header_style), Paragraph("Verbatim Viva Presenter Script", table_header_style)],
        [
            Paragraph("0:00 - 1:00<br/>Introduction", table_cell_bold),
            Paragraph("Home Portal<br/>(app.py)", table_cell_style),
            Paragraph(
                "<i>'Good morning, respected professors and examiner. Today, I am presenting <b>MARKETIX</b>, an industrial-grade marketing intelligence platform developed using Python and Machine Learning. "
                "This project consolidates my industrial training with certifications from <b>BCG X</b>, <b>IBM</b>, and <b>Deloitte</b>. "
                "The core objective is solving marketing budget wastage: in typical retail datasets, only ~15% of prospects respond, while 85% of ad spend is wasted. MARKETIX provides data cleaning, customer segmentation, and response prediction.'</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("1:00 - 2:15<br/>Architecture & Data Cleaning", table_cell_bold),
            Paragraph("Module 2:<br/>Data Management", table_cell_style),
            Paragraph(
                "<i>'Here in Module 2, our application ingests marketing data and performs automated data cleaning. "
                "The raw dataset has 2,240 records with 24 missing incomes. Rather than deleting rows, we implement <b>Education-stratified median imputation</b> to preserve demographic fidelity. "
                "We also cap birth-year outliers and engineer marketing KPIs like Total Spending and Customer Tenure. The cleaned records synchronize into our 6-table PostgreSQL schema, with resilient SQLite fallback.'</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("2:15 - 3:30<br/>Dashboard & Campaign Analysis", table_cell_bold),
            Paragraph("Module 1 & 3:<br/>Dashboard & Campaigns", table_cell_style),
            Paragraph(
                "<i>'Looking at our executive dashboard, we see 2,240 customers and 334 conversions on the target campaign (14.91% acceptance rate). "
                "In Module 3, our multi-wave campaign analysis reveals that the latest integrated campaign outperformed Campaign 2 by more than 11x. "
                "We also analyze omnichannel distribution, showing physical store transactions lead volume while direct catalog mailings produce higher conversions among affluent households.'</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("3:30 - 4:45<br/>Customer Segmentation (K-Means)", table_cell_bold),
            Paragraph("Module 5:<br/>Segmentation", table_cell_style),
            Paragraph(
                "<i>'In Module 5, we apply Unsupervised Machine Learning. To avoid arbitrary clustering, we execute an automated <b>Elbow Method</b> and <b>Silhouette Score</b> diagnostic for K=2 to 6, confirming K=4 as optimal. "
                "Our algorithm identifies 4 actionable personas: <b>Affluent Champions</b> (high income, high spend, 28% response rate), <b>Budget Seekers</b> (deal hunters), <b>Cautious Savers</b>, and <b>High-Value Enthusiasts</b>. "
                "Each persona receives distinct marketing recommendations.'</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("4:45 - 6:00<br/>Response Prediction (Logistic Regression)", table_cell_bold),
            Paragraph("Module 6:<br/>Prediction & ROC", table_cell_style),
            Paragraph(
                "<i>'In Module 6, we predict customer response likelihood using Supervised Logistic Regression. "
                "We strictly prevent data leakage and handle class imbalance using <code>class_weight=\"balanced\"</code> on a stratified 80/20 train/test split. "
                "Our model achieves an <b>ROC-AUC of 0.901</b> and a <b>Recall of 77.6%</b> on positive responders. "
                "As demonstrated in this interactive form, entering customer ID 105 computes a 78.2% conversion likelihood in real time, validating high-touch targeting.'</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("6:00 - 7:00<br/>Recommendations, Reports & Conclusion", table_cell_bold),
            Paragraph("Module 7 & 8:<br/>Recommendations & PDF", table_cell_style),
            Paragraph(
                "<i>'Finally, in Module 7 and 8, our platform translates analytical findings into prioritized consulting initiatives adhering to BCG X / Deloitte frameworks, explicitly distinguishing correlation from causation. "
                "Stakeholders can compile and download an executive vector PDF brief generated via ReportLab or export CSV datasets with one click. "
                "MARKETIX bridges machine learning theory with industrial business execution. Thank you, and I welcome your questions.'</i>",
                table_cell_style
            )
        ],
    ]
    t_script = Table(script_data, colWidths=[70, 85, 377])
    t_script.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_script)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # 5. VIVA DEFENSE QUESTIONS & ANSWERS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("5. Top 10 Viva Defense Questions & Examiner Answers", h1_style))

    viva_qa = [
        ("Q1: Why did you choose Streamlit instead of React and FastAPI?",
         "In marketing analytics, unified Python execution eliminates serialization latency, boilerplate REST controllers, and CORS overhead. Streamlit binds directly with Pandas, Scikit-Learn, and SQLAlchemy, delivering reactive dashboards without compromising machine learning speed or code maintainability."),

        ("Q2: How did you handle class imbalance in the response prediction task?",
         "Because only 14.9% of prospects responded, an unweighted model could achieve 85% accuracy by predicting zeros for every prospect, rendering it commercially useless. We solved this by using a stratified 80/20 train/test split and configuring class_weight='balanced' in Logistic Regression, penalizing minority false negatives and achieving 77.6% Recall and 0.901 ROC-AUC."),

        ("Q3: Why not delete records with missing Income values?",
         "Deleting rows with missing data reduces sample size and introduces systematic demographic bias. Instead of simple mean imputation (which distorts variance), we implemented Education-stratified median imputation: imputing each missing income using the median income of that customer's specific educational degree."),

        ("Q4: How do you mathematically justify K=4 in K-Means clustering?",
         "Rather than picking an arbitrary number of clusters, our platform executes an automated Elbow Curve (within-cluster sum of squares inertia) and calculates Silhouette Scores across K=2 to 6. K=4 demonstrates the optimal balance of high intra-cluster cohesion and inter-cluster separation."),

        ("Q5: Why choose Logistic Regression over complex black-box models like Random Forest or XGBoost?",
         "For a B.Tech 3rd-year industrial training project, explainability and odds-ratio interpretability are paramount. Logistic Regression provides explicit linear coefficients that explain why a customer is predicted to convert, runs with low latency, and achieves an outstanding ROC-AUC of 0.901 without overfitting."),

        ("Q6: How does the database layer maintain reliability if PostgreSQL is offline?",
         "Our database manager in database/connection.py implements a dual-mode pattern. It tests connection to PostgreSQL at localhost:5432; if the PostgreSQL daemon is offline, it activates an embedded SQLite database (marketix.db) without throwing crashes, ensuring reliable viva demonstrations."),

        ("Q7: How did you prevent data leakage during model training?",
         "We isolated the target response column (Response) and excluded non-predictive attributes (ID) as well as post-campaign indicators. Features are scaled using parameters fitted strictly on the 80% training split, preventing test data leakage into training transformations."),

        ("Q8: Why does MARKETIX avoid claiming an explicit ROI calculation?",
         "The Kaggle dataset contains placeholder columns (Z_CostContact=3, Z_Revenue=11) rather than true variable marketing acquisition costs and product gross margins. Following ethical consulting standards (emphasized in BCG X), we benchmark empirical Response Rates and Category Spend Lift rather than computing speculative ROI."),

        ("Q9: What does the BCG X and Deloitte connection contribute to this project?",
         "BCG X principles are applied in Modules 3 and 7: translating data patterns into decision frameworks, managing customer lifetime value, and separating correlation from causation. Deloitte simulation practices are implemented in Modules 5, 6, and 8: behavioral segmentation, predictive scoring, and executive PDF briefs."),

        ("Q10: What are the primary future enhancements for MARKETIX?",
         "Future iterations can integrate multi-armed bandit algorithms for automated A/B test traffic allocation, containerized cloud deployment on AWS/GCP via Docker, and real-time Kafka event streaming for live e-commerce website browse tracking.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(f"<b>Model Answer:</b> {a}", body_style))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built at: {PDF_PATH}")
    return str(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
