"""
MARKETIX PDF Report Generator
Produces executive-ready PDF analytics summaries using ReportLab.
"""

from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
import pandas as pd
import datetime


def generate_pdf_report(metrics: dict, campaign_summary: pd.DataFrame, recommendations: list[dict]) -> bytes:
    """
    Generates a formal, professional PDF executive analytics brief.
    Returns bytes suitable for Streamlit download_button.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1E3A8A")   # Navy
    c_secondary = colors.HexColor("#0D9488") # Teal
    c_dark = colors.HexColor("#1F2937")
    c_light = colors.HexColor("#F3F4F6")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=c_dark
    )

    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    story = []

    # Title & Header
    story.append(Paragraph("MARKETIX Executive Analytics Report", title_style))
    today_str = datetime.datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Platform: MARKETIX Marketing Intelligence | Generated: {today_str} | Status: Industrial-Grade", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=12))

    # 1. Executive Summary KPIs Table
    story.append(Paragraph("1. Core Performance Indicators", h2_style))
    
    kpi_data = [
        ["Total Customers", "Analyzed Campaigns", "Positive Responses", "Response Rate", "Avg Income", "Avg Spending"],
        [
            f"{metrics.get('total_customers', 0):,}",
            f"{metrics.get('total_campaigns', 5)}",
            f"{metrics.get('positive_responses', 0):,}",
            f"{metrics.get('response_rate', 0.0):.2f}%",
            f"${metrics.get('average_income', 0.0):,.0f}",
            f"${metrics.get('average_spending', 0.0):,.0f}"
        ]
    ]
    t_kpis = Table(kpi_data, colWidths=[90, 90, 90, 85, 90, 90])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 1), c_light),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 12))

    # 2. Campaign Benchmark Table
    story.append(Paragraph("2. Campaign Conversion Comparison", h2_style))
    if campaign_summary is not None and not campaign_summary.empty:
        cmp_table_data = [["Campaign Name", "Contacted", "Responses", "Response Rate (%)"]]
        for _, row in campaign_summary.iterrows():
            cmp_table_data.append([
                str(row.get("Campaign_Name", "")),
                f"{int(row.get('Customers_Contacted', 0)):,}",
                f"{int(row.get('Positive_Responses', 0)):,}",
                f"{float(row.get('Response_Rate', 0)):.2f}%"
            ])
        t_cmp = Table(cmp_table_data, colWidths=[200, 110, 110, 120])
        t_cmp.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_cmp)
    story.append(Spacer(1, 12))

    # 3. Strategic Recommendations
    story.append(Paragraph("3. Executive Recommendations (BCG X / Deloitte Framework)", h2_style))
    if recommendations:
        for idx, rec in enumerate(recommendations[:4], 1):
            story.append(Paragraph(f"<b>Recommendation {idx}: {rec.get('category', 'Strategy')}</b> [Priority: {rec.get('priority', 'Normal')}]", bold_body))
            story.append(Paragraph(f"• <b>Finding:</b> {rec.get('finding', '')}", body_style))
            story.append(Paragraph(f"• <b>Strategic Action:</b> {rec.get('recommendation', '')}", body_style))
            story.append(Paragraph(f"• <b>Expected Impact:</b> {rec.get('expected_impact', '')}", body_style))
            story.append(Spacer(1, 6))

    # Build document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
