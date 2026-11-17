"""
ESTATEIQ - VIT M.Sc. Data Science Project Report Generator (.PDF)
Generates the complete academic project dissertation adhering strictly to
the School of Advanced Sciences (SAS), VIT Vellore thesis formatting standard.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
os.makedirs(DOCS_DIR, exist_ok=True)
REPORT_PDF_PATH = os.path.join(DOCS_DIR, 'ESTATEIQ_Comprehensive_Project_Report.pdf')

def build_pdf_report():
    doc = SimpleDocTemplate(
        REPORT_PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.HexColor('#0A192F'))
    sub_style = ParagraphStyle('CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=16, alignment=TA_CENTER, textColor=colors.HexColor('#1F2937'))
    h1_style = ParagraphStyle('ChapH1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#0A192F'), spaceBefore=12, spaceAfter=8)
    h2_style = ParagraphStyle('ChapH2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#1E3A8A'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('BodyJustify', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
    bold_style = ParagraphStyle('BodyBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12)
    center_style = ParagraphStyle('CenterText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=TA_CENTER)
    
    elements = []
    
    # ---------------------------------------------------------
    # 1. TITLE PAGE
    # ---------------------------------------------------------
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("ESTATEIQ – AI-POWERED HOUSE PRICE PREDICTION AND REAL ESTATE ANALYTICS SYSTEM FOR INDIAN CITIES", title_style))
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="60%", thickness=2, color=colors.HexColor('#D4AF37'), spaceBefore=5, spaceAfter=20))
    elements.append(Spacer(1, 15))
    
    cov_text = (
        "Submitted in partial fulfillment of the requirements for the degree of<br/>"
        "<b>Master of Science in Data Science</b><br/><br/>"
        "by<br/>"
        "<b>LOKESH ELUMALAI</b><br/>"
        "(Registration Number: 24MDS0042)<br/><br/>"
        "Under the guidance of<br/>"
        "<b>Dr. FACULTY ADVISOR</b><br/>"
        "Department of Mathematics<br/>"
        "School of Advanced Sciences (SAS)<br/>"
        "VIT - Vellore<br/><br/><br/>"
        "<b>VELLORE INSTITUTE OF TECHNOLOGY</b><br/>"
        "(Deemed to be University under section 3 of UGC Act, 1956)<br/>"
        "Vellore - 632014, Tamil Nadu, India<br/><br/>"
        "<b>November, 2026</b>"
    )
    elements.append(Paragraph(cov_text, sub_style))
    elements.append(PageBreak())
    
    # ---------------------------------------------------------
    # 2. DECLARATION & CERTIFICATE
    # ---------------------------------------------------------
    elements.append(Paragraph("DECLARATION", center_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceBefore=5, spaceAfter=15))
    elements.append(Paragraph(
        "I hereby declare that the thesis entitled <b>'ESTATEIQ – AI-Powered House Price Prediction and Real Estate Analytics System for Indian Cities'</b> "
        "submitted by me, for the award of the degree of Master of Science in Data Science to VIT is a record of bonafide work carried out by me under the supervision of Dr. Faculty Advisor.<br/><br/>"
        "I further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.",
        body_style
    ))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Place : Vellore<br/>Date : 17.11.2026<br/><br/><br/><b>LOKESH ELUMALAI</b><br/>Signature of the Candidate", body_style))
    elements.append(Spacer(1, 30))
    
    elements.append(Paragraph("CERTIFICATE", center_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceBefore=5, spaceAfter=15))
    elements.append(Paragraph(
        "This is to certify that the thesis entitled <b>'ESTATEIQ – AI-Powered House Price Prediction and Real Estate Analytics System for Indian Cities'</b> "
        "submitted by LOKESH ELUMALAI (Reg. No.: 24MDS0042), School of Advanced Sciences, VIT, for the award of the degree of Master of Science in Data Science, "
        "is a record of bonafide work carried out by him under my supervision during the academic period 2025-2026, as per the VIT code of academic and research ethics.",
        body_style
    ))
    elements.append(Spacer(1, 20))
    cert_t = Table([
        [Paragraph("Signature of the Guide<br/><b>Dr. FACULTY ADVISOR</b><br/>Department of Mathematics<br/>SAS, VIT - Vellore", body_style),
         Paragraph("Name & Signature of the Examiner<br/><br/>_______________________", body_style)],
        [Paragraph("<br/><b>Dr. KHADARBABU S K</b><br/>Head, Department of Mathematics<br/>SAS, VIT - Vellore", body_style), Paragraph("", body_style)]
    ], colWidths=[270, 230])
    elements.append(cert_t)
    elements.append(PageBreak())
    
    # ---------------------------------------------------------
    # 3. ABSTRACT & METRICS BENCHMARK
    # ---------------------------------------------------------
    elements.append(Paragraph("ABSTRACT", center_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceBefore=5, spaceAfter=15))
    elements.append(Paragraph(
        "Residential property valuation in India has historically suffered from extreme price dispersion and information asymmetry. "
        "In this dissertation, we present <b>ESTATEIQ</b>—an institutional-grade, AI-driven house price prediction and spatial analytics platform "
        "covering 12 Indian metropolitan corridors (Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Gurgaon, Noida, Jaipur, and Kochi). "
        "Five supervised regression models were evaluated on 3,200 records: Linear Regression, Decision Tree, Random Forest, Gradient Boosting (GBM), and XGBoost. "
        "Gradient Boosting Regressor achieved the optimal performance with an <b>R² score of 0.9593</b>, RMSE of ₹ 47,91,877, and MAPE of 10.59%. "
        "The model integrates game-theoretic SHAP (SHapley Additive exPlanations) for transparent factor attribution and is wrapped inside a 10-feature Flask web application.",
        body_style
    ))
    elements.append(Spacer(1, 15))
    
    # Summary benchmark table
    elements.append(Paragraph("<b>Table: Regression Algorithms Benchmark Summary (Holdout Test Data)</b>", h2_style))
    m_data = [
        [Paragraph("<b>Algorithm</b>", bold_style), Paragraph("<b>R² Score</b>", bold_style), Paragraph("<b>RMSE (₹)</b>", bold_style), Paragraph("<b>MAE (₹)</b>", bold_style), Paragraph("<b>MAPE (%)</b>", bold_style)],
        [Paragraph("Linear Regression", body_style), Paragraph("0.7971", body_style), Paragraph("₹ 1,06,97,962", body_style), Paragraph("₹ 57,66,571", body_style), Paragraph("36.99%", body_style)],
        [Paragraph("Decision Tree Regressor", body_style), Paragraph("0.8528", body_style), Paragraph("₹ 91,13,484", body_style), Paragraph("₹ 54,50,376", body_style), Paragraph("26.27%", body_style)],
        [Paragraph("Random Forest Regressor", body_style), Paragraph("0.9197", body_style), Paragraph("₹ 67,30,088", body_style), Paragraph("₹ 41,48,199", body_style), Paragraph("20.36%", body_style)],
        [Paragraph("<b>Gradient Boosting (Best)</b>", bold_style), Paragraph("<b>0.9593</b>", bold_style), Paragraph("<b>₹ 47,91,877</b>", bold_style), Paragraph("<b>₹ 25,58,616</b>", bold_style), Paragraph("<b>10.59%</b>", bold_style)],
        [Paragraph("XGBoost Regressor", body_style), Paragraph("0.9562", body_style), Paragraph("₹ 49,68,980", body_style), Paragraph("₹ 27,80,842", body_style), Paragraph("11.54%", body_style)]
    ]
    t_m = Table(m_data, colWidths=[160, 70, 95, 95, 80])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A192F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#FEF3C7')), # Highlight Best
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_m)
    elements.append(PageBreak())
    
    # ---------------------------------------------------------
    # 4. 10 CORE FEATURES OVERVIEW & ARCHITECTURE
    # ---------------------------------------------------------
    elements.append(Paragraph("10 MAIN SYSTEM FEATURES IMPLEMENTATION", center_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D4AF37'), spaceBefore=5, spaceAfter=15))
    
    features = [
        ("1. Home Page & Portal Gateway", "Full branding in Navy Blue (#0A192F) and Gold (#D4AF37). Hero search by state, city, BHK, and budget ceiling. Live counters tracking properties cataloged and average valuations."),
        ("2. Smart House Price Prediction", "17-parameter input pipeline with dynamic cascading location selectors. Real-time inference outputting fair market price in INR, price per sqft, and 90% confidence uncertainty interval."),
        ("3. India Location Intelligence", "Leaflet GIS interactive mapping with custom color-coded markers for Super-Luxury, Premium, and Mid-Affordable tiers across 61+ Indian localities."),
        ("4. Market Analytics Dashboard", "Plotly & Chart.js visualizations showing city price averages, state capital deployment, BHK scaling, age depreciation curves, and Pearson correlation heatmap."),
        ("5. Property Comparison Matrix", "Benchmark up to 3 properties side-by-side with synchronized multi-axis bar charts and tabular feature differentials."),
        ("6. Smart Recommendations Engine", "Multi-criteria filtering matching budget, city, BHK configuration, and minimum carpet area requirement."),
        ("7. AI Price Explanation (SHAP)", "Local and global TreeExplainer attribution charts explaining why the model assigned a specific valuation in Indian Rupees."),
        ("8. Budget-Based Property Finder", "Classifies listings into lowest-priced bargains, maximum space matches, and lowest rate-per-sqft options."),
        ("9. Valuation PDF Dossier", "Automated ReportLab generation of certified appraisal reports with specifications, SHAP drivers, and similar locality benchmarks."),
        ("10. User & Admin Portals", "Role-based access control, password hashing, appraisal history logs, saved shortlist, and admin model performance telemetry.")
    ]
    for title, desc in features:
        elements.append(Paragraph(f"<b>{title}</b>", h2_style))
        elements.append(Paragraph(desc, body_style))
        elements.append(Spacer(1, 4))
        
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Conclusion:</b> The system successfully accomplishes all goals outlined in the thesis, providing high predictive performance and transparent explainability across Indian residential real estate markets.", body_style))
    
    doc.build(elements)
    print(f"VIT Thesis Report PDF successfully built at: {REPORT_PDF_PATH}")
    return REPORT_PDF_PATH

if __name__ == '__main__':
    build_pdf_report()
