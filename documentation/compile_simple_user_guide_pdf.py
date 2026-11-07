"""
Generate a clean, simple, beautifully styled PDF for MARKETIX:
'MARKETIX — Practical User Guide & Core Concept'
Focuses strictly on:
- What it is in plain words
- The 4 main practical uses
- Step-by-step practical usage guide with concrete test examples
- The 30-second teacher explanation (Saving $35,000 on a campaign)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "MARKETIX — Practical User Guide & Core Concept")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 32, "Confidential — Prepared for B.Tech Industrial Project Submission")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def build_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom palette
    NAVY = colors.HexColor("#0F172A")
    BLUE = colors.HexColor("#2563EB")
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER = colors.HexColor("#CBD5E1")
    TEXT = colors.HexColor("#1E293B")
    MUTED = colors.HexColor("#475569")
    TEAL = colors.HexColor("#0D9488")
    GREEN = colors.HexColor("#16A34A")
    AMBER = colors.HexColor("#D97706")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=BLUE,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14.5,
        textColor=TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_text = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=15,
        textColor=NAVY
    )

    story = []

    # Title Banner Block
    banner_data = [
        [
            Paragraph("MARKETIX", title_style),
            Paragraph("<b>Status:</b> Ready for Submission<br/><b>Topic:</b> Practical App Guide", ParagraphStyle("Meta", parent=body_style, fontSize=8.5, leading=12, textColor=MUTED, alignment=2))
        ],
        [
            Paragraph("<b>Practical User Guide & Core Concept (Easy Language)</b>", subtitle_style),
            ""
        ]
    ]
    banner_table = Table(banner_data, colWidths=[360, 144])
    banner_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(banner_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceBefore=4, spaceAfter=12))

    # Section 1: What is MARKETIX
    story.append(Paragraph("1. What is MARKETIX? (In Plain Words)", h1_style))
    summary_box_text = (
        "<b>MARKETIX</b> is an intelligent software app created for retail stores and businesses to stop wasting "
        "money on useless marketing.<br/><br/>"
        "Instead of blindly sending email blasts, text messages, or paper flyers to <i>all</i> customers, "
        "MARKETIX analyzes your customer data to tell you:<br/>"
        "• <b>Who your best customers are</b> and what products they actually purchase.<br/>"
        "• <b>Which group they belong to</b> (e.g. affluent high spenders vs bargain deal hunters).<br/>"
        "• <b>Whether a specific customer will actually buy</b> from your next campaign or ignore it (before spending any money)."
    )
    summary_table = Table(
        [[Paragraph(summary_box_text, body_style)]],
        colWidths=[504]
    )
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Section 2: The 4 Main Uses
    story.append(Paragraph("2. The 4 Main Practical Uses of MARKETIX", h1_style))
    uses_data = [
        [
            Paragraph("<b>Use Case</b>", ParagraphStyle("TH1", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>What It Does</b>", ParagraphStyle("TH2", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>Business Benefit</b>", ParagraphStyle("TH3", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY))
        ],
        [
            Paragraph("<b>1. Spending & Channel Analytics</b>", body_style),
            Paragraph("Analyzes sales across 6 product types (Wines, Meat, Fruits, etc.) and 3 channels (Web, Catalog, Physical Stores).", body_style),
            Paragraph("Shows which channels drive the most revenue so companies know where to invest.", body_style)
        ],
        [
            Paragraph("<b>2. Automatic Customer Segmentation</b>", body_style),
            Paragraph("Uses Machine Learning (K-Means) to divide 2,240 customers into 4 clear customer personas.", body_style),
            Paragraph("Stops one-size-fits-all marketing. Tailors products to each customer's budget and lifestyle.", body_style)
        ],
        [
            Paragraph("<b>3. Campaign Response Predictor</b>", body_style),
            Paragraph("Allows staff to enter customer details and get an instant AI probability score (0% to 100%) of buying.", body_style),
            Paragraph("Saves up to 40% in campaign costs by filtering out people who will never buy.", body_style)
        ],
        [
            Paragraph("<b>4. 1-Click PDF Executive Reports</b>", body_style),
            Paragraph("Compiles all metrics, charts, and recommendations into a formatted PDF file at the click of a button.", body_style),
            Paragraph("Saves hours of manual Excel reporting for team leads and executives.", body_style)
        ]
    ]
    uses_table = Table(uses_data, colWidths=[130, 204, 170])
    uses_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(uses_table)
    story.append(Spacer(1, 12))

    # Section 3: Step-by-Step Practical Usage Guide
    story.append(Paragraph("3. How to Use the App (Step-by-Step Practical Guide)", h1_style))
    story.append(Paragraph("Here is how anyone uses MARKETIX from start to finish with concrete examples:", body_style))
    story.append(Spacer(1, 4))

    # Step 1
    story.append(Paragraph("<b>Step 1: Open the Application</b>", h2_style))
    story.append(Paragraph("• Run the app in your browser at <code>http://localhost:8501</code>.<br/>• The landing page immediately shows 6 primary KPI cards: <b>2,240 Total Customers</b>, <b>5 Historical Campaigns</b>, <b>334 Positive Responses (14.91% rate)</b>, <b>$52,243 Average Income</b>, and <b>$606 Average Spend</b>.", bullet_style))

    # Step 2
    story.append(Paragraph("<b>Step 2: Check Overall Performance (Click 'Dashboard')</b>", h2_style))
    story.append(Paragraph("• Click <b>Dashboard</b> in the sidebar to view revenue distribution.<br/>• <i>Practical Discovery:</i> You will observe that <b>Wine ($304 avg)</b> and <b>Meat ($167 avg)</b> make up over 75% of total sales, and customers make twice as many purchases in <b>Physical Stores</b> compared to online.<br/>• <i>Decision:</i> Keep premium wine and meat prominently displayed in physical store entrances.", bullet_style))

    # Step 3
    story.append(Paragraph("<b>Step 3: Group Your Customers (Click 'Customer Segmentation')</b>", h2_style))
    story.append(Paragraph("• Click <b>Customer Segmentation</b> on the sidebar, keep clusters at 4, and click <b>Run Clustering</b>.<br/>• The AI groups all 2,240 customers into 4 distinct groups:", bullet_style))

    # Persona mini table
    persona_data = [
        [
            Paragraph("<b>Persona Group</b>", ParagraphStyle("P1", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>Income / Profile</b>", ParagraphStyle("P2", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>What They Buy</b>", ParagraphStyle("P3", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>Action to Take</b>", ParagraphStyle("P4", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY))
        ],
        [
            Paragraph("<b>Affluent Connoisseurs</b>", body_style),
            Paragraph("Income: $78,000+<br/>No young children", body_style),
            Paragraph("Wines ($600+) & Meats ($400+)", body_style),
            Paragraph("Send invitations to VIP premium wine tastings (no discount needed).", body_style)
        ],
        [
            Paragraph("<b>Family Value Seekers</b>", body_style),
            Paragraph("Income: $35k - $55k<br/>1 to 3 children", body_style),
            Paragraph("Groceries, sweets, mid-tier items", body_style),
            Paragraph("Send family-pack grocery bundles and school season promotions.", body_style)
        ],
        [
            Paragraph("<b>Digital Natives</b>", body_style),
            Paragraph("Income: $40k - $65k<br/>Younger demographic", body_style),
            Paragraph("Frequent web & catalogue purchases", body_style),
            Paragraph("Target with online app flash sales and fast delivery perks.", body_style)
        ],
        [
            Paragraph("<b>Budget Deal Shoppers</b>", body_style),
            Paragraph("Income: Below $35,000", body_style),
            Paragraph("Purchases only with promo deals", body_style),
            Paragraph("Send clearance deal notifications to move unsold inventory.", body_style)
        ]
    ]
    persona_table = Table(persona_data, colWidths=[120, 105, 125, 154])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(persona_table)
    story.append(Spacer(1, 10))

    # Step 4
    story.append(Paragraph("<b>Step 4: Test a Customer Before Spending Money (Click 'Response Predictor')</b>", h2_style))
    story.append(Paragraph("This is the core predictive engine. Instead of guessing, staff can test customer profiles:", body_style))

    # Test Scenarios Table
    tests_data = [
        [
            Paragraph("<b>Scenario</b>", ParagraphStyle("T1", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>Inputs Entered</b>", ParagraphStyle("T2", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>AI Prediction</b>", ParagraphStyle("T3", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY)),
            Paragraph("<b>Action Taken</b>", ParagraphStyle("T4", parent=body_style, fontName="Helvetica-Bold", textColor=NAVY))
        ],
        [
            Paragraph("<b>Customer A<br/>(Active Buyer)</b>", body_style),
            Paragraph("• Income: <b>$82,000</b><br/>• Recency: <b>12 days</b><br/>• Past accepted: <b>2</b><br/>• Web visits/mo: <b>3</b>", body_style),
            Paragraph("<font color='#16A34A'><b>87.2% Likelihood</b><br/>HIGH PROPENSITY</font>", body_style),
            Paragraph("<b>SEND OFFER</b><br/>High probability of conversion and strong profit.", body_style)
        ],
        [
            Paragraph("<b>Customer B<br/>(Dormant Buyer)</b>", body_style),
            Paragraph("• Income: <b>$24,000</b><br/>• Recency: <b>85 days</b><br/>• Past accepted: <b>0</b><br/>• Web visits/mo: <b>8</b>", body_style),
            Paragraph("<font color='#DC2626'><b>4.1% Likelihood</b><br/>LOW PROPENSITY</font>", body_style),
            Paragraph("<b>SUPPRESS OFFER</b><br/>Save print/postage cost. Do not spend budget.", body_style)
        ]
    ]
    tests_table = Table(tests_data, colWidths=[110, 140, 114, 140])
    tests_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tests_table)
    story.append(Spacer(1, 10))

    # Step 5
    story.append(Paragraph("<b>Step 5: Export Professional Report (Click 'Reports')</b>", h2_style))
    story.append(Paragraph("• Click <b>Reports</b> in the sidebar.<br/>• Click <b>Generate PDF Report</b>.<br/>• Download the file to present to managers, executives, or examiners.", bullet_style))
    story.append(Spacer(1, 10))

    # Section 4: Real-Life Example (30-second explanation)
    story.append(Paragraph("4. Real-Life Example: How MARKETIX Saves $35,000 on a Campaign", h1_style))
    story.append(Paragraph("<b>(You can say this exact 30-second explanation to your teacher):</b>", ParagraphStyle("SubEx", parent=body_style, textColor=MUTED, fontName="Helvetica-Bold")))

    callout_html = (
        "<i>\"Teacher, imagine a store wants to mail 10,000 printed promotional catalogs. "
        "Printing and mailing each catalog costs $5, so the campaign costs <b>$50,000</b>.<br/><br/>"
        "Without MARKETIX, they mail to everyone. Usually only 5% respond, meaning <b>$47,500 is completely wasted</b> "
        "on 9,500 people who threw the catalog straight in the trash.<br/><br/>"
        "With MARKETIX, we run our customer list through our Machine Learning model first. "
        "The model identifies the 7,000 people who have almost zero chance of responding and filters them out. "
        "We only print and mail catalogs to the 3,000 high-probability customers.<br/><br/>"
        "<b>The Result:</b> Marketing costs drop from <b>$50,000 down to $15,000 (saving $35,000)</b>, "
        "while still capturing almost all the sales!\"</i>"
    )
    callout_table = Table(
        [[Paragraph(callout_html, callout_text)]],
        colWidths=[504]
    )
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 14))

    # Summary strip
    story.append(Paragraph("<b>Key Takeaway:</b> MARKETIX transforms marketing from blind guessing into data-driven, profitable decision-making.", ParagraphStyle("Ending", parent=body_style, fontName="Helvetica-Bold", textColor=BLUE, alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Simple Guide PDF successfully built at: {output_path}")

if __name__ == "__main__":
    target = os.path.abspath("MARKETIX/documentation/MARKETIX_Simple_Practical_Guide.pdf")
    build_pdf(target)
