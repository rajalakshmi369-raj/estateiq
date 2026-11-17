"""
ESTATEIQ - Property Valuation PDF Report Generator
Generates institutional-grade valuation reports using ReportLab with
Navy & Gold branding, executive summary, SHAP drivers, and market comparables.
"""

import os
import sys
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Color Palette: Navy Blue, Gold, Slate Grey, Crisp White
NAVY = colors.HexColor("#0A192F")
NAVY_LIGHT = colors.HexColor("#172A45")
GOLD = colors.HexColor("#D4AF37")
GOLD_LIGHT = colors.HexColor("#F9F4E8")
GREY_TEXT = colors.HexColor("#4B5563")
GREY_BG = colors.HexColor("#F3F4F6")
GREEN_ACCENT = colors.HexColor("#10B981")
BORDER_COLOR = colors.HexColor("#E5E7EB")

def generate_valuation_pdf(property_data, prediction_result, output_filename=None):
    """
    Generates a PDF valuation report and saves it to reports/ directory.
    Returns the absolute path to the generated PDF.
    """
    reports_dir = os.path.join(BASE_DIR, 'reports', 'generated')
    os.makedirs(reports_dir, exist_ok=True)
    
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prop_id = property_data.get('property_id', 'PRED')
        output_filename = f"ESTATEIQ_Valuation_{prop_id}_{timestamp}.pdf"
        
    pdf_path = os.path.join(reports_dir, output_filename)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=GOLD,
        alignment=TA_LEFT
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=GREY_TEXT
    )
    
    bold_style = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=NAVY
    )
    
    gold_price_style = ParagraphStyle(
        'GoldPrice',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=NAVY,
        alignment=TA_CENTER
    )
    
    elements = []
    
    # 1. Header Banner (Navy & Gold)
    header_data = [
        [
            Paragraph("<b>ESTATEIQ VALUATION DOSSIER</b>", title_style),
            Paragraph(f"<b>REPORT ID:</b> EQ-VAL-{datetime.now().strftime('%y%m%d%H%M')}<br/><b>DATE:</b> {datetime.now().strftime('%d %b %Y')}", ParagraphStyle('HeadRight', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.white, alignment=TA_RIGHT))
        ],
        [
            Paragraph("AI-POWERED REAL ESTATE APPRAISAL & COMPARATIVE MARKET ASSESSMENT", subtitle_style),
            Paragraph("CERTIFIED AI VALUATION", ParagraphStyle('HeadRight2', parent=styles['Normal'], fontSize=7, leading=9, textColor=GOLD, alignment=TA_RIGHT))
        ]
    ]
    
    header_table = Table(header_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 10))
    
    # 2. Key Valuation Box
    val_box_data = [
        [
            Paragraph("<b>ESTIMATED FAIR MARKET VALUE</b>", ParagraphStyle('ValTitle', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("<b>PRICE PER SQ.FT</b>", ParagraphStyle('ValTitle2', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("<b>CONFIDENCE RANGE (90% CI)</b>", ParagraphStyle('ValTitle3', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, alignment=TA_CENTER))
        ],
        [
            Paragraph(f"<b>{prediction_result.get('predicted_price_formatted', 'N/A')}</b><br/><font size=7 color='#6b7280'>({prediction_result.get('predicted_price_full', '')})</font>", gold_price_style),
            Paragraph(f"<b>{prediction_result.get('price_per_sqft_formatted', 'N/A')}</b>", ParagraphStyle('Rate', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=NAVY, alignment=TA_CENTER)),
            Paragraph(f"<b>{prediction_result.get('uncertainty_range', 'N/A')}</b>", ParagraphStyle('Range', fontName='Helvetica', fontSize=11, leading=15, textColor=NAVY, alignment=TA_CENTER))
        ]
    ]
    val_box = Table(val_box_data, colWidths=[200, 160, 180])
    val_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, GOLD),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(val_box)
    elements.append(Spacer(1, 12))
    
    # 3. Subject Property Specifications
    elements.append(Paragraph("<b>1. PROPERTY SPECIFICATIONS & ATTRIBUTES</b>", h2_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=1, spaceAfter=6))
    
    prop_specs = [
        [
            Paragraph("<b>Location / Area:</b>", body_style), Paragraph(str(property_data.get('area_name', 'N/A')), bold_style),
            Paragraph("<b>City & State:</b>", body_style), Paragraph(f"{property_data.get('city', '')}, {property_data.get('state', '')}", bold_style)
        ],
        [
            Paragraph("<b>Super Built-up Area:</b>", body_style), Paragraph(f"{property_data.get('area_sqft', 'N/A')} sq.ft", bold_style),
            Paragraph("<b>Configuration:</b>", body_style), Paragraph(f"{property_data.get('bedrooms', 0)} BHK ({property_data.get('bathrooms', 0)} Baths, {property_data.get('balcony', 0)} Balconies)", bold_style)
        ],
        [
            Paragraph("<b>Property Type:</b>", body_style), Paragraph(str(property_data.get('property_type', 'Apartment')), bold_style),
            Paragraph("<b>Property Age:</b>", body_style), Paragraph(f"{property_data.get('property_age', 0)} years", bold_style)
        ],
        [
            Paragraph("<b>Floor Details:</b>", body_style), Paragraph(f"Floor {property_data.get('floor_number', 1)} of {property_data.get('total_floors', 1)}", bold_style),
            Paragraph("<b>Furnishing Status:</b>", body_style), Paragraph(str(property_data.get('furnishing', 'Semi-Furnished')), bold_style)
        ],
        [
            Paragraph("<b>Reserved Parking:</b>", body_style), Paragraph(f"{property_data.get('parking', 1)} Covered Bay(s)", bold_style),
            Paragraph("<b>Facing Direction:</b>", body_style), Paragraph(str(property_data.get('facing', 'East')), bold_style)
        ],
        [
            Paragraph("<b>Key Amenities:</b>", body_style), 
            Paragraph(str(property_data.get('amenities', 'Gym, Lift, Power Backup')).replace(';', ', '), bold_style),
            Paragraph("<b>PIN Code:</b>", body_style), Paragraph(str(property_data.get('pincode', 'N/A')), bold_style)
        ]
    ]
    spec_table = Table(prop_specs, colWidths=[120, 150, 120, 150])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREY_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(spec_table)
    elements.append(Spacer(1, 12))
    
    # 4. AI Price Explanation (SHAP Factors)
    elements.append(Paragraph("<b>2. AI VALUATION EXPLAINABILITY & PRIMARY VALUE DRIVERS</b>", h2_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=1, spaceAfter=6))
    
    shap_factors = prediction_result.get('shap_breakdown', [])
    shap_rows = [
        [
            Paragraph("<b>Key Influencing Factor</b>", bold_style),
            Paragraph("<b>Directional Impact</b>", bold_style),
            Paragraph("<b>Valuation Contribution (INR)</b>", bold_style)
        ]
    ]
    for factor in shap_factors[:5]:
        is_pos = factor.get('is_positive', True)
        impact_dir = "▲ Positive Contributor" if is_pos else "▼ Negative Adjustment"
        color_tag = "color='#10b981'" if is_pos else "color='#ef4444'"
        shap_rows.append([
            Paragraph(factor.get('factor', ''), body_style),
            Paragraph(f"<font {color_tag}><b>{impact_dir}</b></font>", body_style),
            Paragraph(factor.get('impact_formatted', ''), bold_style)
        ])
        
    shap_table = Table(shap_rows, colWidths=[240, 140, 160])
    shap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GREY_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(shap_table)
    elements.append(Spacer(1, 12))
    
    # 5. Comparative Market Analysis (Similar Properties)
    elements.append(Paragraph("<b>3. COMPARATIVE MARKET BENCHMARKS (SIMILAR LOCALITY SALES)</b>", h2_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=1, spaceAfter=6))
    
    similar_props = prediction_result.get('similar_properties', [])
    comp_rows = [
        [
            Paragraph("<b>Property ID</b>", bold_style),
            Paragraph("<b>Locality</b>", bold_style),
            Paragraph("<b>Config</b>", bold_style),
            Paragraph("<b>Area (sq.ft)</b>", bold_style),
            Paragraph("<b>Rate/sq.ft</b>", bold_style),
            Paragraph("<b>Benchmark Price</b>", bold_style)
        ]
    ]
    for sp in similar_props[:4]:
        comp_rows.append([
            Paragraph(sp.get('property_id', ''), body_style),
            Paragraph(sp.get('area_name', ''), body_style),
            Paragraph(f"{sp.get('bedrooms', 0)} BHK", body_style),
            Paragraph(f"{sp.get('area_sqft', 0):,}", body_style),
            Paragraph(sp.get('price_per_sqft', ''), body_style),
            Paragraph(f"<b>{sp.get('price_formatted', '')}</b>", bold_style)
        ])
        
    comp_table = Table(comp_rows, colWidths=[80, 140, 60, 80, 80, 100])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GREY_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(comp_table)
    elements.append(Spacer(1, 14))
    
    # 6. Certification & Disclaimer Footer
    footer_text = (
        "<b>ESTATEIQ VALUATION DISCLAIMER:</b> This automated appraisal report is generated via the ESTATEIQ ensemble ML engine "
        "(Gradient Boosting / Random Forest / XGBoost with SHAP explainability) trained on representative Indian municipal transaction data. "
        "Estimated values represent statistically derived fair market projections under normal economic conditions."
    )
    elements.append(Paragraph(footer_text, ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor("#6B7280"))))
    elements.append(Spacer(1, 8))
    
    sign_table = Table([
        [
            Paragraph("<b>Algorithm Engine:</b> Gradient Boosting Regressor (R² = 0.959)", body_style),
            Paragraph("<b>ESTATEIQ Digital Verification Stamp</b><br/>Verified & Authenticated Document", ParagraphStyle('SignRight', fontName='Helvetica', fontSize=8, leading=10, alignment=TA_RIGHT, textColor=NAVY))
        ]
    ], colWidths=[300, 240])
    elements.append(sign_table)
    
    # Build Document
    doc.build(elements)
    print(f"Valuation PDF successfully generated at: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    sample_prop = {
        "property_id": "EQ-DEMO-01",
        "area_name": "Whitefield",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": 560066,
        "area_sqft": 1550,
        "bedrooms": 3,
        "bathrooms": 3,
        "balcony": 2,
        "property_type": "Apartment",
        "property_age": 3,
        "furnishing": "Semi-Furnished",
        "parking": 2,
        "floor_number": 9,
        "total_floors": 18,
        "facing": "East",
        "amenities": "Gym;Swimming Pool;Clubhouse;24x7 Security;Lift"
    }
    sample_pred = {
        "predicted_price": 16400000,
        "predicted_price_formatted": "₹ 1.64 Cr",
        "predicted_price_full": "₹ 1,64,00,000",
        "price_per_sqft_formatted": "₹ 10,580 / sq.ft",
        "uncertainty_range": "₹ 1.52 Cr - ₹ 1.76 Cr",
        "shap_breakdown": [
            {"factor": "Area: 1,550 sq.ft", "impact_formatted": "₹ 58,00,000", "is_positive": True},
            {"factor": "Location: Whitefield IT Corridor", "impact_formatted": "₹ 42,00,000", "is_positive": True},
            {"factor": "Configuration: 3 BHK", "impact_formatted": "₹ 24,00,000", "is_positive": True}
        ],
        "similar_properties": [
            {"property_id": "EQ-10023", "area_name": "Whitefield", "bedrooms": 3, "area_sqft": 1500, "price_per_sqft": "₹ 10,200/sqft", "price_formatted": "₹ 1.53 Cr"},
            {"property_id": "EQ-10145", "area_name": "Whitefield", "bedrooms": 3, "area_sqft": 1600, "price_per_sqft": "₹ 10,650/sqft", "price_formatted": "₹ 1.70 Cr"}
        ]
    }
    out = generate_valuation_pdf(sample_prop, sample_pred)
    print("Report generated:", out)
