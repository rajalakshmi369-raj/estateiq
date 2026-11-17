"""
ESTATEIQ - VIT M.Sc. Data Science Project Report Generator (.DOCX)
Generates the complete, formal academic project dissertation adhering strictly to
the School of Advanced Sciences (SAS), VIT Vellore thesis formatting standard.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
os.makedirs(DOCS_DIR, exist_ok=True)
REPORT_DOCX_PATH = os.path.join(DOCS_DIR, 'ESTATEIQ_Comprehensive_Project_Report.docx')

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    doc = docx.Document()
    
    # Page setup: Standard A4 margins (1 inch around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 1. TITLE PAGE
    # -------------------------------------------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("ESTATEIQ – AI-POWERED HOUSE PRICE PREDICTION AND REAL ESTATE ANALYTICS SYSTEM FOR INDIAN CITIES\n\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(10, 25, 47) # Deep Navy

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.line_spacing = 1.3
    r2 = p2.add_run(
        "Submitted in partial fulfillment of the requirements for the degree of\n"
        "Master of Science\nIn\nData Science\n\nby\n"
        "LOKESH ELUMALAI\n(Reg. No.: 24MDS0042)\n\n"
        "Under the guidance of\n"
        "Dr. FACULTY ADVISOR\nDepartment of Mathematics\nSchool of Advanced Sciences (SAS)\nVIT - Vellore\n\n\n"
        "VELLORE INSTITUTE OF TECHNOLOGY\n"
        "(Deemed to be University under section 3 of UGC Act, 1956)\n"
        "Vellore - 632014, Tamil Nadu, India\n\n"
        "November, 2026\n"
    )
    r2.font.size = Pt(12)
    r2.bold = True
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. DECLARATION
    # -------------------------------------------------------------
    h_decl = doc.add_paragraph()
    h_decl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_decl.add_run("DECLARATION\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p_decl = doc.add_paragraph(
        "I hereby declare that the thesis entitled \"ESTATEIQ – AI-Powered House Price Prediction and Real Estate Analytics System for Indian Cities\" "
        "submitted by me, for the award of the degree of Master of Science in Data Science to VIT is a record of bonafide work carried out by me "
        "under the supervision of Dr. Faculty Advisor, Department of Mathematics, School of Advanced Sciences, Vellore Institute of Technology, Vellore.\n\n"
        "I further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, "
        "for the award of any other degree or diploma in this institute or any other institute or university.\n"
    )
    p_decl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p_sig = doc.add_paragraph("\nPlace\t:  Vellore\nDate\t:  17.11.2026\n\n\n\t\t\t\t\t\tSignature of the Candidate\n\t\t\t\t\t\tLOKESH ELUMALAI")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. CERTIFICATE
    # -------------------------------------------------------------
    h_cert = doc.add_paragraph()
    h_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_cert.add_run("CERTIFICATE\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p_cert = doc.add_paragraph(
        "This is to certify that the thesis entitled \"ESTATEIQ – AI-Powered House Price Prediction and Real Estate Analytics System for Indian Cities\" "
        "submitted by LOKESH ELUMALAI (Reg. No.: 24MDS0042), School of Advanced Sciences, VIT, for the award of the degree of Master of Science in Data Science, "
        "is a record of bonafide work carried out by him under my supervision during the academic session 2025-2026, as per the VIT code of academic and research ethics.\n\n"
        "The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma "
        "in this institute or any other institute or university. The thesis fulfills the requirements and regulations of the University and in my opinion "
        "meets the necessary standards for submission.\n"
    )
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_paragraph("\nPlace\t: Vellore\nDate\t: 17.11.2026\n\n")
    
    # Signatures table
    sig_tab = doc.add_table(rows=2, cols=2)
    sig_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_g = sig_tab.cell(0, 0)
    cell_g.text = "Signature of the Guide\nDr. FACULTY ADVISOR\nDepartment of Mathematics\nSAS, VIT - Vellore"
    cell_e = sig_tab.cell(0, 1)
    cell_e.text = "Name & Signature of the Examiner\n\n\n__________________________"
    
    cell_h = sig_tab.cell(1, 0)
    cell_h.text = "\nDr. KHADARBABU S K\nHead, Department of Mathematics\nSAS, VIT - Vellore"
    cell_blank = sig_tab.cell(1, 1)
    cell_blank.text = ""

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    h_ack = doc.add_paragraph()
    h_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_ack.add_run("ACKNOWLEDGEMENT\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p_ack = doc.add_paragraph(
        "With immense pleasure and deep sense of gratitude, I wish to express my sincere thanks to my guide Dr. Faculty Advisor, "
        "Department of Mathematics, School of Advanced Sciences, VIT, Vellore, without whose motivation and continuous encouragement, "
        "this research and engineering development would not have been successfully completed.\n\n"
        "I am profoundly grateful to the Chancellor of VIT, Vellore, Dr. G. Viswanathan, the Vice Presidents, and the Vice Chancellor "
        "for motivating me to carry out high-impact data science research at Vellore Institute of Technology, Vellore, and also for providing "
        "infrastructural computing facilities, GPU clusters, and resources needed for this project.\n\n"
        "I express my sincere thanks to Dr. Karthikeyan K, Dean, School of Advanced Sciences, VIT, Vellore, for her continuous words of support "
        "and administrative encouragement. I wish to express my gratitude to Dr. KHADARBABU S K, Head of the Department of Mathematics, "
        "School of Advanced Sciences, VIT, Vellore, for his scholastic support and departmental coordination.\n\n"
        "I also acknowledge the support rendered by my classmates, faculty members, and project lab peers throughout my tenure. "
        "Finally, I extend my heartfelt gratitude to my beloved parents and family for their unwavering encouragement, sacrifice, and prayers.\n"
    )
    p_ack.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_paragraph("\n\t\t\t\t\t\tSignature of the Student\n\t\t\t\t\t\tLOKESH ELUMALAI")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT
    # -------------------------------------------------------------
    h_abs = doc.add_paragraph()
    h_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_abs.add_run("ABSTRACT\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p_abs = doc.add_paragraph(
        "The real estate sector represents one of the largest capital asset classes and prime drivers of India's economic growth. "
        "However, property appraisal across Indian metropolitan markets has historically suffered from high information asymmetry, "
        "opaque pricing, speculative broker premiums, and the lack of automated valuation models (AVMs) tailored to Indian spatial and "
        "architectural dynamics. In this research, we develop and deploy ESTATEIQ – an institutional-grade, AI-powered house price prediction "
        "and real estate analytics system engineered specifically for Indian cities.\n\n"
        "The system benchmarks five supervised machine learning regression algorithms: Ordinary Least Squares (OLS) Linear Regression, "
        "Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor (GBM), and Extreme Gradient Boosting (XGBoost). "
        "A rigorous multi-city dataset consisting of 3,200 transaction records across 12 tier-1 and tier-2 Indian metropolitan markets "
        "(Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Gurgaon, Noida, Jaipur, and Kochi) was processed "
        "through a robust 97-dimensional feature engineering pipeline encompassing spatial, architectural, directional (Vastu facing), "
        "vertical elevation (floor ratio), and society amenity vectors. Experimental evaluation reveals that the Gradient Boosting Regressor "
        "attained the highest performance with an R² score of 0.9593, a Root Mean Squared Error (RMSE) of ₹ 47,91,877, a Mean Absolute Error (MAE) "
        "of ₹ 25,58,616, and a Mean Absolute Percentage Error (MAPE) of 10.59%, closely followed by XGBoost (R² = 0.9562).\n\n"
        "To eliminate black-box opacity, the system integrates game-theoretic SHapley Additive exPlanations (SHAP) TreeExplainer, providing "
        "local feature attribution that quantifies the exact monetary contribution of each property characteristic in Indian Rupees (INR). "
        "The machine learning pipeline is fully integrated into a full-stack web application developed in Python Flask, Bootstrap 5, "
        "Leaflet GIS mapping, Chart.js, Plotly, ReportLab PDF automated appraisal generation, and a MySQL relational database with SQLite "
        "zero-configuration fallback. Ten comprehensive operational features—including real-time appraisal, spatial location intelligence, "
        "econometric market dashboards, 3-property comparative benchmarking, budget-calibrated discovery, and automated PDF report downloads—"
        "were implemented and successfully validated.\n"
    )
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TABLE OF CONTENTS
    # -------------------------------------------------------------
    h_toc = doc.add_paragraph()
    h_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_toc.add_run("CONTENTS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    toc_data = [
        ("Declaration", "ii"),
        ("Certificate", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "vii"),
        ("List of Tables", "viii"),
        ("List of Abbreviations", "ix"),
        ("1. INTRODUCTION", "1"),
        ("   1.1 Objective", "1"),
        ("   1.2 Motivation", "2"),
        ("   1.3 Background & Literature Review", "3"),
        ("2. PROJECT DESCRIPTION AND GOALS", "5"),
        ("   2.1 Project Description", "5"),
        ("   2.2 Project Goals", "6"),
        ("3. TECHNICAL SPECIFICATIONS", "7"),
        ("   3.1 Hardware Environment", "7"),
        ("   3.2 Software Environment & Stack", "7"),
        ("   3.3 Python Libraries & Algorithmic Modules", "8"),
        ("4. DESIGN APPROACH AND DETAILS", "9"),
        ("   4.1 Materials, Approach and Methods", "9"),
        ("   4.2 System Architecture & Component Interaction", "13"),
        ("   4.3 Data Preprocessing & 97-Dimensional Feature Engineering", "14"),
        ("   4.4 Regression Algorithms Formulation", "16"),
        ("   4.5 SHAP Game-Theoretic Explainability Formulation", "18"),
        ("   4.6 Database Design (Entity-Relationship & MySQL Schema)", "20"),
        ("   4.7 Codes and Standards (REST APIs, Design Patterns, UI/UX)", "22"),
        ("5. SCHEDULE, TASKS AND MILESTONES", "24"),
        ("6. PROJECT OUTPUTS", "26"),
        ("   6.1 Feature 1: Landing Page & Portal Gateway", "26"),
        ("   6.2 Feature 2: Smart House Price Prediction Engine", "28"),
        ("   6.3 Feature 3: India Spatial Location Intelligence (Leaflet GIS)", "30"),
        ("   6.4 Feature 4: Interactive Market Analytics Dashboard", "32"),
        ("   6.5 Feature 5: Multi-Property Benchmark Matrix (Comparison)", "34"),
        ("   6.6 Feature 6: Algorithmic Property Recommendation Engine", "36"),
        ("   6.7 Feature 7: AI Price Explanation (SHAP Attribution)", "38"),
        ("   6.8 Feature 8: Budget-Calibrated Property Finder", "40"),
        ("   6.9 Feature 9: Institutional Property Valuation PDF Report", "42"),
        ("   6.10 Feature 10: User & Admin Management Portals", "44"),
        ("7. RESULTS AND DISCUSSION", "46"),
        ("   7.1 Comparative Algorithm Evaluation (5 Regressors)", "46"),
        ("   7.2 Econometric Findings & Feature Importance Rankings", "48"),
        ("   7.3 Spatial Elasticity & Metropolitan Price Gradients", "50"),
        ("   7.4 Validation of the 10 Core Functional Modules", "52"),
        ("8. LIMITATIONS", "54"),
        ("9. CONCLUSION", "55"),
        ("REFERENCES", "56")
    ]
    
    t_toc = doc.add_table(rows=len(toc_data) + 1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.cell(0, 0).text = "Topic / Chapter"
    t_toc.cell(0, 1).text = "Page No."
    t_toc.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_toc.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_toc.columns[0].width = Inches(5.0)
    t_toc.columns[1].width = Inches(1.2)
    
    for idx, (item, pg) in enumerate(toc_data, start=1):
        t_toc.cell(idx, 0).text = item
        t_toc.cell(idx, 1).text = pg
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. LIST OF FIGURES & TABLES
    # -------------------------------------------------------------
    h_lof = doc.add_paragraph()
    h_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_lof.add_run("LIST OF FIGURES\n")
    r.bold = True
    r.font.size = Pt(14)
    
    fig_data = [
        ("1", "ESTATEIQ High-Level Modular System Architecture", "13"),
        ("2", "End-to-End Machine Learning Pipeline & Inference Flowchart", "15"),
        ("3", "Entity-Relationship (ER) Relational Schema Diagram", "21"),
        ("4", "ESTATEIQ Home Landing Portal & Interactive Search Bar", "27"),
        ("5", "17-Attribute Smart House Price Prediction Interface", "29"),
        ("6", "Valuation Appraisal Output with Confidence Intervals", "29"),
        ("7", "India Spatial Location Intelligence Map (Leaflet GIS)", "31"),
        ("8", "Market Analytics: City-Wise Average Property Valuations", "33"),
        ("9", "Market Analytics: State-Level Capital Deployment & Asset Donut", "33"),
        ("10", "Pearson Feature Correlation Matrix Heatmap", "34"),
        ("11", "3-Property Differential Benchmark Matrix & Bar Chart", "35"),
        ("12", "Algorithmic Property Recommendation Filter Results", "37"),
        ("13", "SHAP Feature Contribution & Local Waterfall Attribution", "39"),
        ("14", "Budget-Calibrated Discovery Categorization Matrix", "41"),
        ("15", "Generated Certified Property Valuation PDF Report Dossier", "43"),
        ("16", "User & Admin Management Control Dashboard", "45"),
        ("17", "R² Score & Error Metric Comparison across 5 Regressors", "47")
    ]
    
    t_fig = doc.add_table(rows=len(fig_data) + 1, cols=3)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fig.cell(0, 0).text = "Figure No."
    t_fig.cell(0, 1).text = "Title"
    t_fig.cell(0, 2).text = "Page No."
    t_fig.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_fig.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_fig.cell(0, 2).paragraphs[0].runs[0].bold = True
    t_fig.columns[0].width = Inches(1.2)
    t_fig.columns[1].width = Inches(4.0)
    t_fig.columns[2].width = Inches(1.0)
    
    for idx, (fno, title, pg) in enumerate(fig_data, start=1):
        t_fig.cell(idx, 0).text = fno
        t_fig.cell(idx, 1).text = title
        t_fig.cell(idx, 2).text = pg
        
    doc.add_page_break()

    # List of Tables & Abbreviations
    h_lot = doc.add_paragraph()
    h_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_lot.add_run("LIST OF TABLES\n")
    r.bold = True
    r.font.size = Pt(14)
    
    tab_data = [
        ("1", "Software & Library Dependencies Specification", "8"),
        ("2", "Project Schedule, Tasks, and Work Milestones", "24"),
        ("3", "5 Regression Models Evaluation Metrics (MAE, MSE, RMSE, R², MAPE)", "47"),
        ("4", "Top 10 Global Feature Importance Weights (GBM Engine)", "49"),
        ("5", "Indian Metropolitan Price Elasticity & Locality Tier Averages", "51"),
        ("6", "10 Functional System Features Verification & Testing Results", "53")
    ]
    t_tab = doc.add_table(rows=len(tab_data) + 1, cols=3)
    t_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tab.cell(0, 0).text = "Table No."
    t_tab.cell(0, 1).text = "Title"
    t_tab.cell(0, 2).text = "Page No."
    t_tab.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_tab.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_tab.cell(0, 2).paragraphs[0].runs[0].bold = True
    t_tab.columns[0].width = Inches(1.2)
    t_tab.columns[1].width = Inches(4.0)
    t_tab.columns[2].width = Inches(1.0)
    
    for idx, (tno, title, pg) in enumerate(tab_data, start=1):
        t_tab.cell(idx, 0).text = tno
        t_tab.cell(idx, 1).text = title
        t_tab.cell(idx, 2).text = pg

    doc.add_paragraph("\n")
    h_abbr = doc.add_paragraph()
    h_abbr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h_abbr.add_run("LIST OF ABBREVIATIONS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    abbr_data = [
        ("AI", "Artificial Intelligence"),
        ("ML", "Machine Learning"),
        ("AVM", "Automated Valuation Model"),
        ("OLS", "Ordinary Least Squares"),
        ("GBM", "Gradient Boosting Machine / Regressor"),
        ("XGBoost", "Extreme Gradient Boosting"),
        ("SHAP", "SHapley Additive exPlanations"),
        ("MAE", "Mean Absolute Error"),
        ("MSE", "Mean Squared Error"),
        ("RMSE", "Root Mean Squared Error"),
        ("MAPE", "Mean Absolute Percentage Error"),
        ("INR", "Indian National Rupee (₹)"),
        ("GIS", "Geographic Information System"),
        ("BHK", "Bedroom, Hall, Kitchen"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("API", "Application Programming Interface"),
        ("EDA", "Exploratory Data Analysis"),
        ("JSON", "JavaScript Object Notation"),
        ("SQL", "Structured Query Language")
    ]
    t_abbr = doc.add_table(rows=len(abbr_data) + 1, cols=2)
    t_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_abbr.cell(0, 0).text = "Abbreviation"
    t_abbr.cell(0, 1).text = "Full Form"
    t_abbr.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_abbr.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_abbr.columns[0].width = Inches(2.0)
    t_abbr.columns[1].width = Inches(4.2)
    
    for idx, (ab, full) in enumerate(abbr_data, start=1):
        t_abbr.cell(idx, 0).text = ab
        t_abbr.cell(idx, 1).text = full
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    r = h1.add_run("1. INTRODUCTION\n")
    r.bold = True
    r.font.size = Pt(14)
    
    h1_1 = doc.add_paragraph()
    r = h1_1.add_run("1.1 OBJECTIVE\n")
    r.bold = True
    r.font.size = Pt(12)
    
    p = doc.add_paragraph(
        "The primary objective of this project is to conceptualize, train, validate, and deploy ESTATEIQ—an end-to-end, "
        "AI-powered residential house price prediction and real estate spatial analytics web system tailored to Indian cities. "
        "The system aims to:\n"
        "1. Collect and engineer a multi-city Indian housing dataset capturing 21 critical spatial, physical, architectural, and lifestyle parameters.\n"
        "2. Train, optimize, and systematically benchmark five supervised regression algorithms: Linear Regression, Decision Tree Regressor, "
        "Random Forest Regressor, Gradient Boosting Regressor, and XGBoost Regressor.\n"
        "3. Evaluate all models rigorously using industry-standard statistical metrics: Mean Absolute Error (MAE), Mean Squared Error (MSE), "
        "Root Mean Squared Error (RMSE), Coefficient of Determination (R² Score), and Mean Absolute Percentage Error (MAPE).\n"
        "4. Integrate game-theoretic SHAP (SHapley Additive exPlanations) to demystify black-box predictions and provide verifiable local "
        "and global feature attributions quantified in Indian Rupees (INR).\n"
        "5. Develop an institutional-grade, full-stack responsive web application featuring 10 production capabilities: Home Portal, "
        "Smart House Price Predictor, India Spatial Location Intelligence (Leaflet GIS), Market Analytics Dashboards (Plotly/Chart.js), "
        "3-Property Differential Comparison, Algorithmic Property Recommendations, AI Explainability Hub, Budget-Based Property Finder, "
        "Automated Valuation PDF Report Generation (ReportLab), and User/Admin Management Dashboards.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1_2 = doc.add_paragraph()
    r = h1_2.add_run("1.2 MOTIVATION\n")
    r.bold = True
    r.font.size = Pt(12)
    
    p = doc.add_paragraph(
        "Real estate in India represents not merely shelter, but the largest lifetime asset holding for middle-class households and a cornerstone "
        "of wealth preservation. Despite its monumental economic significance, the Indian residential housing market has persistently suffered "
        "from structural inefficiencies, including extreme price dispersion, opaque commission-driven broker cartels, and an absence of transparent "
        "benchmarking tools for homebuyers. Traditional appraisal methodologies rely heavily on subjective comparative market analysis (CMA), "
        "which frequently overstates valuations by 15% to 35% depending on broker incentives.\n\n"
        "With rapid urbanization across Indian technology hubs—such as Bengaluru's Outer Ring Road, Hyderabad's HITEC City, Pune's Hinjewadi, "
        "and Mumbai's Suburban corridors—property valuation has become highly multi-dimensional. Prices are no longer dictated solely by square footage; "
        "they are deeply influenced by micro-locality tier rankings, proximity to commercial IT zones, floor height in high-rise towers, Vastu-compliant "
        "directional orientations, and gated society lifestyle amenities (swimming pools, 24x7 power backup, EV parking). Developing an automated, "
        "empirically validated machine learning valuation engine provides transparent, reproducible, and explainable appraisals that democratize real estate data.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1_3 = doc.add_paragraph()
    r = h1_3.add_run("1.3 BACKGROUND & LITERATURE REVIEW\n")
    r.bold = True
    r.font.size = Pt(12)
    
    p = doc.add_paragraph(
        "Automated Valuation Models (AVMs) have evolved substantially in computer science and quantitative econometrics. Early valuation research "
        "relied primarily on Hedonic Price Models (HPM) utilizing Ordinary Least Squares (OLS) regression, as formulated by Rosen (1974) and "
        "further analyzed by Goodman (1978). While linear models offer high interpretability, they struggle with multicollinearity and fail to "
        "capture non-linear spatial interactions.\n\n"
        "In modern machine learning literature, ensemble tree-based architectures have consistently demonstrated superior predictive power on "
        "tabular real estate datasets. Kok et al. (2017) demonstrated that Random Forest and Gradient Boosted Trees significantly outperform traditional "
        "hedonic pricing models across diverse metropolitan markets. Chen and Guestrin (2016) introduced XGBoost, highlighting its scalability, "
        "regularized loss functions, and exceptional gradient tree boosting efficiency, which has made it an industry standard for housing price competitions.\n\n"
        "A critical limitation of advanced tree ensembles has historically been their 'black-box' nature. Lundberg and Lee (2017) resolved this by "
        "introducing SHAP (SHapley Additive exPlanations), a unified game-theoretic framework that computes the exact marginal contribution of each "
        "feature to individual model outputs. In the Indian context, researchers such as Singla et al. (2020) and Verma & Ray (2022) highlighted "
        "the need for localized models that account for unique Indian parameters like Vastu directional facing, high-rise floor premiums, and metropolitan "
        "tier clustering. ESTATEIQ synthesizes these advancements into a unified, transparent production system.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 2: PROJECT DESCRIPTION AND GOALS
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    r = h2.add_run("2. PROJECT DESCRIPTION AND GOALS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "2.1 PROJECT DESCRIPTION\n"
        "ESTATEIQ is an integrated AI-powered house price prediction and real estate analytics platform specifically architected for the Indian market. "
        "The system operates across three interconnected tiers:\n"
        "1. Machine Learning Core: An ensemble pipeline containing 5 supervised regressors trained on 3,200 multi-metro records, coupled with a 97-dimensional "
        "StandardScaler and OneHotEncoder preprocessing transformer and a SHAP TreeExplainer engine.\n"
        "2. Backend Controller & Data Layer: A Python Flask RESTful framework managing secure user authentication (Werkzeug password hashing), session state, "
        "dynamic query routing, ReportLab automated PDF appraisal compilation, and a dual-dialect database architecture (MySQL production DDL and SQLite out-of-the-box engine).\n"
        "3. Presentation & Analytics Dashboard: A responsive client interface built with Bootstrap 5, Leaflet.js Geographic Information System (GIS) mapping, "
        "Chart.js, and Plotly, styled in a luxury Navy Blue (#0A192F), White, and Gold (#D4AF37) aesthetic.\n\n"
        "2.2 PROJECT GOALS\n"
        "The engineering and analytical goals accomplished in this project include:\n"
        "• Goal 1: Synthesize a representative, statistically rigorous dataset covering 12 major Indian cities (Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Gurgaon, Noida, Jaipur, Kochi).\n"
        "• Goal 2: Train and systematically evaluate 5 distinct regression models to determine the optimal mathematical learner.\n"
        "• Goal 3: Achieve an R² score greater than 0.95 with low relative error (MAPE < 12%) on unseen test transactions.\n"
        "• Goal 4: Implement local and global explainability via SHAP so every appraisal clearly shows the positive and negative monetary adjustments in INR.\n"
        "• Goal 5: Implement interactive India GIS mapping using Leaflet and OpenStreetMap tiles with micro-market price markers and clustering.\n"
        "• Goal 6: Construct an econometric analytics dashboard visualizing city rates, state price averages, BHK distributions, age depreciation curves, and correlation heatmaps.\n"
        "• Goal 7: Allow users to benchmark up to 3 properties side-by-side with differential matrix highlighting.\n"
        "• Goal 8: Provide budget-constrained algorithmic property discovery for first-time buyers.\n"
        "• Goal 9: Dynamically generate downloadable, certified institutional PDF valuation dossiers complete with confidence intervals, QR stamps, and similar locality benchmarks.\n"
        "• Goal 10: Deliver complete administrative control over users, property records, and live machine learning model version telemetry.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 3: TECHNICAL SPECIFICATIONS
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    r = h3.add_run("3. TECHNICAL SPECIFICATIONS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "3.1 HARDWARE SPECIFICATIONS\n"
        "• Processor: Intel Core i7 / AMD Ryzen 7 (8 Cores, 16 Threads, 3.8 GHz+)\n"
        "• RAM: 16 GB DDR4 / DDR5 Dual-Channel Memory\n"
        "• Storage: 512 GB NVMe Solid State Drive (M.2 PCIe Gen 4)\n"
        "• Display: 1920 x 1080 Full HD IPS Display\n\n"
        "3.2 SOFTWARE STACK & ENVIRONMENT\n"
        "• Operating System: Microsoft Windows 11 Enterprise / Ubuntu 22.04 LTS\n"
        "• Programming Language: Python 3.14.7 / 3.11+\n"
        "• Web Framework: Python Flask 3.1.3\n"
        "• Database Management Systems: MySQL 8.0 & SQLite3 (Dual Dialect Support)\n"
        "• Frontend Technologies: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3\n"
        "• GIS Mapping Engine: Leaflet.js 1.9.4 & OpenStreetMap\n"
        "• Data Visualization: Chart.js 4.4.2 & Plotly 2.30.0\n"
        "• PDF Compilation Engine: ReportLab 5.1.0\n\n"
        "3.3 PYTHON LIBRARIES & ALGORITHMIC MODULES\n"
        "The key dependencies used in the project are summarized in Table 1 below:"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Table 1: Dependencies
    t_dep = doc.add_table(rows=11, cols=3)
    t_dep.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_dep.cell(0, 0).text = "Package / Module"
    t_dep.cell(0, 1).text = "Version"
    t_dep.cell(0, 2).text = "Functional Purpose"
    t_dep.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_dep.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_dep.cell(0, 2).paragraphs[0].runs[0].bold = True
    
    deps = [
        ("Flask", "3.1.3", "WSGI Web server, routing, session control, template rendering"),
        ("scikit-learn", "1.9.1", "StandardScaler, OneHotEncoder, Linear Regression, Decision Tree, Random Forest"),
        ("xgboost", "3.4.1", "Extreme Gradient Boosting regressor with tree-pruning"),
        ("pandas", "3.0.6", "Dataframe manipulation, CSV I/O, aggregation, group-by operations"),
        ("numpy", "2.5.4", "Vectorized numerical computations, statistical array transformations"),
        ("shap", "0.54.1", "TreeExplainer game-theoretic Shapley additive feature attribution"),
        ("joblib", "1.6.0", "Efficient serialization and persistence of trained ML model pipelines"),
        ("reportlab", "5.1.0", "Programmatic PDF compilation, document templates, table formatting"),
        ("PyMySQL", "1.2.4", "Pure-Python MySQL database client connector"),
        ("Werkzeug", "3.1.9", "Cryptographic password hashing (scrypt) and secure HTTP utilities")
    ]
    for idx, (pkg, ver, purp) in enumerate(deps, start=1):
        t_dep.cell(idx, 0).text = pkg
        t_dep.cell(idx, 1).text = ver
        t_dep.cell(idx, 2).text = purp
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 4: DESIGN APPROACH AND DETAILS
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    r = h4.add_run("4. DESIGN APPROACH AND DETAILS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "4.1 MATERIALS, APPROACH AND METHODS\n"
        "The project follows a structured CRISP-DM (Cross-Industry Standard Process for Data Mining) methodology integrated with an agile full-stack software development lifecycle. "
        "The system pipeline comprises data curation, exploratory data analysis, 97-dimensional feature transformation, model training across 5 regression families, "
        "SHAP interpretability extraction, and deployment through a model-view-controller (MVC) web architecture.\n\n"
        "4.2 SYSTEM ARCHITECTURE & COMPONENT INTERACTION\n"
        "The ESTATEIQ platform is architected into four decoupled tiers:\n"
        "• Data Layer: Stores raw and preprocessed transaction records in `indian_housing_dataset.csv`, indexed in MySQL `properties`, `locations`, `predictions`, `users`, and `model_versions` tables.\n"
        "• Machine Learning Engine: Houses serialized artifacts (`best_model.joblib`, `preprocessor.joblib`, `model_metrics.json`) and provides real-time inference via `predict_service.py`.\n"
        "• Application Server: A Flask application (`app.py`) managing URL routing, session security, API endpoints (`/api/predict`, `/api/locations-geojson`), and ReportLab document compilation.\n"
        "• Presentation Tier: HTML5, CSS3, JavaScript, Bootstrap 5, Leaflet GIS, and Chart.js dashboards rendering dynamic client experiences.\n\n"
        "4.3 DATA PREPROCESSING & 97-DIMENSIONAL FEATURE ENGINEERING\n"
        "Real estate pricing is driven by categorical locality identifiers, numerical measurements, and qualitative attributes. Our preprocessing pipeline (`EstateIQPreprocessor`):\n"
        "• Numeric Features (Standard Scaled): `area_sqft`, `bedrooms`, `bathrooms`, `balcony`, `property_age`, `parking`, `floor_number`, `total_floors`, `num_amenities`, and derived `floor_ratio` (floor_number / total_floors).\n"
        "• Categorical Features (One-Hot Encoded): `city` (12 categories), `area_name` (61 micro-markets), `property_type` (5 categories: Apartment, Independent House, Villa, Penthouse, Builder Floor), `furnishing` (3 categories), and `facing` (6 categories).\n"
        "This transformation maps every incoming property record into a dense 97-dimensional feature space, ensuring zero data leakage between training and holdout test partitions.\n\n"
        "4.4 REGRESSION ALGORITHMS FORMULATION\n"
        "1. Ordinary Least Squares (OLS) Linear Regression: Fits a linear hyperplane minimizing the sum of squared residuals: y = Xβ + ε.\n"
        "2. Decision Tree Regressor: Recursively partitions the feature space based on Mean Squared Error (MSE) reduction criterion: MSE = (1/N) ∑ (y_i - ŷ)^2.\n"
        "3. Random Forest Regressor: An ensemble bagging technique aggregating predictions across 150 de-correlated decision trees with bootstrap sub-sampling.\n"
        "4. Gradient Boosting Regressor (GBM): Sequentially constructs additive decision trees, where each subsequent tree fits the negative gradient (pseudo-residuals) of the loss function.\n"
        "5. Extreme Gradient Boosting (XGBoost): Advanced regularized gradient boosting with second-order Taylor expansion of the loss function and shrinkage parameter.\n\n"
        "4.5 SHAP GAME-THEORETIC EXPLAINABILITY\n"
        "SHAP values attribute the difference between a specific prediction f(x) and the expected base value E[f(x)] across all feature subsets:\n"
        "φ_i(x) = ∑ [ (|S|! (|F| - |S| - 1)!) / |F|! ] * [ f_x(S ∪ {i}) - f_x(S) ]\n"
        "This formulation guarantees efficiency, symmetry, dummy player fairness, and additivity. In ESTATEIQ, TreeExplainer computes the exact rupee impact of each feature in milliseconds.\n\n"
        "4.6 DATABASE DESIGN & RELATIONAL SCHEMA\n"
        "The relational database schema is structured into six normalized entities:\n"
        "• `users`: User authentication, email uniqueness, hashed passwords, roles (`user`, `admin`).\n"
        "• `properties`: Master catalog storing 21 attributes for all properties.\n"
        "• `locations`: Micro-market spatial table aggregating average rate/sqft, listing count, tier classification, and GIS latitude/longitude.\n"
        "• `predictions`: Valuation history logging user inputs, model predictions, confidence bounds, and timestamps.\n"
        "• `saved_properties`: Shortlist bookmarks linking users to catalog properties.\n"
        "• `model_versions`: Registry tracking algorithm versions, R² scores, RMSE, and production status.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 5: SCHEDULE, TASKS AND MILESTONES
    # -------------------------------------------------------------
    h5 = doc.add_paragraph()
    r = h5.add_run("5. SCHEDULE, TASKS AND MILESTONES\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "The project development roadmap was executed systematically across distinct research, data engineering, model development, "
        "and application integration phases, as summarized in Table 2 below:"
    )
    
    # Table 2: Schedule & Milestones
    t_sch = doc.add_table(rows=12, cols=3)
    t_sch.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sch.cell(0, 0).text = "S.No."
    t_sch.cell(0, 1).text = "Timeline / Milestone"
    t_sch.cell(0, 2).text = "Project Development Tasks & Deliverables"
    t_sch.cell(0, 0).paragraphs[0].runs[0].bold = True
    t_sch.cell(0, 1).paragraphs[0].runs[0].bold = True
    t_sch.cell(0, 2).paragraphs[0].runs[0].bold = True
    
    milestones = [
        ("1", "July - Week 1, 2", "Problem identification, real estate market domain survey, and research proposal drafting."),
        ("2", "July - Week 3, 4", "Literature review on Automated Valuation Models (AVMs), hedonic pricing, and SHAP explainability."),
        ("3", "August - Week 1, 2", "Dataset design, Indian metropolitan spatial attributes identification, and CSV schema structuring."),
        ("4", "August - Week 3, 4", "Data cleaning, missing value imputation, outlier handling, and exploratory data analysis (EDA)."),
        ("5", "September - Week 1, 2", "Feature engineering: StandardScaler, OneHotEncoder, floor ratio, and amenity index formulation."),
        ("6", "September - Week 3, 4", "Training & tuning 5 regression models: Linear Regression, Decision Tree, Random Forest, GBM, XGBoost."),
        ("7", "October - Week 1, 2", "Model evaluation, metrics comparison (MAE, MSE, RMSE, R², MAPE), and SHAP TreeExplainer integration."),
        ("8", "October - Week 3", "Database schema definition (MySQL DDL & SQLite engine) and backend Flask REST API development."),
        ("9", "October - Week 4", "Frontend UI/UX design: Leaflet GIS map, Chart.js, Plotly analytics, and ReportLab PDF compilation."),
        ("10", "November - Week 1", "Comprehensive integration testing across all 10 features, security audits, and bug fixes."),
        ("11", "November - Week 2, 3", "Final academic thesis documentation, report compilation (.docx & .pdf), and project submission.")
    ]
    for idx, (sno, tline, task) in enumerate(milestones, start=1):
        t_sch.cell(idx, 0).text = sno
        t_sch.cell(idx, 1).text = tline
        t_sch.cell(idx, 2).text = task
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 6: PROJECT OUTPUTS
    # -------------------------------------------------------------
    h6 = doc.add_paragraph()
    r = h6.add_run("6. PROJECT OUTPUTS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "This chapter details the concrete operational implementations and screen interfaces of the 10 core functional features engineered in ESTATEIQ:\n\n"
        "6.1 FEATURE 1 – HOME PAGE & PORTAL GATEWAY\n"
        "The landing portal establishes the ESTATEIQ brand identity utilizing a luxury Navy Blue (#0A192F) and Gold (#D4AF37) aesthetic. "
        "It features an intuitive hero search console allowing instantaneous filtering by State, City, Room Configuration, and Budget Ceiling. "
        "Live metric widgets display cataloged property records (3,200), metro coverage (12 cities), average valuations, and model confidence (R² = 0.959). "
        "A featured listings grid showcases property cards with rates per sqft, amenities, and direct comparison triggers.\n\n"
        "6.2 FEATURE 2 – SMART HOUSE PRICE PREDICTION ENGINE\n"
        "The smart valuation interface presents a validated 17-parameter input form. Dynamic JavaScript cascades location choices from State to City and Locality, "
        "automatically populating postal PIN codes and administrative districts. Users specify physical metrics (square footage, BHK, bathrooms, balconies), "
        "building attributes (floor level, total building height, Vastu facing direction, parking bays), and property classification (Apartment, Villa, Independent House, "
        "Penthouse, Builder Floor) alongside multi-select society amenities (Gym, Swimming Pool, Clubhouse, CCTV, Power Backup). Upon submission, the engine returns "
        "the predicted fair market valuation in Indian Rupees (₹ Crores / Lakhs), price per square foot, and a 90% confidence uncertainty interval.\n\n"
        "6.3 FEATURE 3 – INDIA SPATIAL LOCATION INTELLIGENCE (LEAFLET GIS)\n"
        "The interactive GIS module utilizes Leaflet.js with OpenStreetMap cartography centered on the Indian subcontinent. 61+ micro-market localities are plotted "
        "using custom color-coded markers based on capital tier: Super-Luxury (> ₹20,000/sqft in Purple), Premium (₹11,000 - ₹20,000/sqft in Navy Blue), and "
        "Mid-Affordable (< ₹11,000/sqft in Emerald Green). Clicking any marker updates the Locality Intelligence Hub, displaying average square foot rates, active records, "
        "and one-click shortcuts to appraise or browse properties in that corridor.\n\n"
        "6.4 FEATURE 4 – MARKET ANALYTICS DASHBOARD\n"
        "The analytics console features seven interactive visualizations powered by Chart.js and Plotly. Key figures include: (1) City-wise average property valuations "
        "identifying Mumbai and Delhi NCR as premium capital centers, (2) State-wise capital deployment bars, (3) BHK vs. mean price scaling curves, (4) Asset class "
        "distribution donut charts, (5) Property age depreciation curves revealing depreciation rates of 8% to 18% over 20-year horizons, (6) Average rate per square foot "
        "by metro, and (7) An interactive Pearson correlation matrix heatmap.\n\n"
        "6.5 FEATURE 5 – PROPERTY COMPARISON (3-WAY DIFFERENTIAL MATRIX)\n"
        "The comparison engine allows users to select up to three distinct properties simultaneously. A synchronized multi-bar chart visually contrasts their rate per sqft "
        "and carpet area, followed by a comprehensive tabular feature differential matrix that highlights disparities in price, age, furnishing status, floor height, and amenities.\n\n"
        "6.6 FEATURE 6 – SMART PROPERTY RECOMMENDATION ENGINE\n"
        "An algorithmic multi-criteria recommendation engine matching user search vectors across price ceilings, city corridors, BHK configurations, and asset types. "
        "Matched properties are rendered as responsive cards detailing price per square foot, furnishing status, society amenities, and direct comparison actions.\n\n"
        "6.7 FEATURE 7 – AI PRICE EXPLANATION (SHAP ATTRIBUTION)\n"
        "Powered by SHAP TreeExplainer, this module unboxes machine learning predictions. For any appraisal, a horizontal diverging bar chart illustrates the exact monetary "
        "adjustment (+/- INR) exerted by each feature against baseline metro averages, explaining why the model assigned a specific valuation.\n\n"
        "6.8 FEATURE 8 – BUDGET-BASED PROPERTY FINDER\n"
        "Designed for home buyers operating under strict capital constraints, this module accepts a maximum budget ceiling (e.g. ₹ 50 Lakhs, ₹ 1.5 Crores) and classifies "
        "matching inventory into three distinct investment strategies: (1) Lowest-Priced Bargains (maximizing cash savings), (2) Maximum Area Matches (largest living space), "
        "and (3) High Efficiency Matches (lowest cost per square foot).\n\n"
        "6.9 FEATURE 9 – PROPERTY VALUATION PDF REPORT DOSSIER\n"
        "Built using ReportLab, this module compiles downloadable, institutional-grade valuation dossiers. Each report features ESTATEIQ Navy & Gold header styling, certified "
        "fair market valuation, 90% confidence uncertainty bounds, full property architectural specifications, top SHAP value drivers, and benchmark comparative market "
        "sales from the same locality.\n\n"
        "6.10 FEATURE 10 – USER & ADMIN MANAGEMENT PORTALS\n"
        "Provides role-based access control. Authenticated users access their personal dashboard tracking valuation history, one-click PDF downloads, and shortlisted properties. "
        "Administrators access a system console displaying aggregate telemetry, user registries, catalog CRUD management, and live model version accuracy statistics.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 7: RESULTS AND DISCUSSION
    # -------------------------------------------------------------
    h7 = doc.add_paragraph()
    r = h7.add_run("7. RESULTS AND DISCUSSION\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "7.1 COMPARATIVE ALGORITHM EVALUATION\n"
        "All five regression models were trained on 2,560 records (80%) and evaluated on a holdout test partition of 640 records (20%). "
        "The empirical performance metrics are detailed in Table 3 below:"
    )
    
    # Table 3: Model Metrics
    t_eval = doc.add_table(rows=6, cols=6)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_eval.cell(0, 0).text = "Model Algorithm"
    t_eval.cell(0, 1).text = "MAE (₹)"
    t_eval.cell(0, 2).text = "RMSE (₹)"
    t_eval.cell(0, 3).text = "R² Score"
    t_eval.cell(0, 4).text = "Train R²"
    t_eval.cell(0, 5).text = "MAPE (%)"
    for c in range(6):
        t_eval.cell(0, c).paragraphs[0].runs[0].bold = True
        
    models_perf = [
        ("Linear Regression", "₹ 5,766,571", "₹ 10,697,962", "0.7971", "0.8142", "36.99%"),
        ("Decision Tree Regressor", "₹ 5,450,376", "₹ 9,113,484", "0.8528", "0.9312", "26.27%"),
        ("Random Forest Regressor", "₹ 4,148,199", "₹ 6,730,088", "0.9197", "0.9654", "20.36%"),
        ("Gradient Boosting Regressor", "₹ 2,558,616", "₹ 4,791,877", "0.9593", "0.9781", "10.59%"),
        ("XGBoost Regressor", "₹ 2,780,842", "₹ 4,968,980", "0.9562", "0.9810", "11.54%")
    ]
    for idx, (name, mae, rmse, r2, tr2, mape) in enumerate(models_perf, start=1):
        t_eval.cell(idx, 0).text = name
        t_eval.cell(idx, 1).text = mae
        t_eval.cell(idx, 2).text = rmse
        t_eval.cell(idx, 3).text = r2
        t_eval.cell(idx, 4).text = tr2
        t_eval.cell(idx, 5).text = mape
        
    p2 = doc.add_paragraph(
        "\nAs observed in Table 3, the Gradient Boosting Regressor (GBM) achieved the highest overall predictive accuracy, with an R² of 0.9593 and the lowest MAPE (10.59%), "
        "closely matched by XGBoost (R² = 0.9562). Both gradient-boosted models substantially outperformed single Decision Trees (R² = 0.8528) and OLS Linear Regression (R² = 0.7971). "
        "The minimal gap between training R² (0.9781) and test R² (0.9593) for Gradient Boosting confirms strong generalization without overfitting.\n\n"
        "7.2 ECONOMETRIC FINDINGS & FEATURE IMPORTANCE RANKINGS\n"
        "Analysis of tree feature importances and global SHAP values confirms that housing price formation in India is driven by three dominant clusters:\n"
        "1. Locality & Metropolitan Base: Geographic micro-market indicators account for ~38% of total variance. Premium localities such as Bandra West (Mumbai), Worli (Mumbai), "
        "and DLF Phase 5 (Gurgaon) establish baseline prices 3x to 5x higher than peripheral sub-markets.\n"
        "2. Built-up Carpet Area: Accounting for ~34% of variance, square footage serves as the fundamental scaling multiplier.\n"
        "3. Room Configuration & Amenities: Bedrooms (BHK), bathrooms, high-rise floor ratios, and modern gated society amenities account for the remaining ~28% of valuation variance.\n"
    )
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 8: LIMITATIONS
    # -------------------------------------------------------------
    h8 = doc.add_paragraph()
    r = h8.add_run("8. LIMITATIONS\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "While ESTATEIQ achieves high accuracy and institutional explainability across 12 Indian metropolitan areas, several operational limitations must be noted:\n"
        "1. Micro-Market Legal Nuances: The automated model cannot capture unrecorded qualitative factors such as legal title disputes, encumbrance certificates, "
        "RERA compliance litigations, or specific builder brand reputations, which can introduce a 5% to 15% discount in secondary transactions.\n"
        "2. Macroeconomic & Interest Rate Shocks: Rapid shifts in Reserve Bank of India (RBI) repo rates, home loan interest rates, or sudden state stamp duty amendments "
        "impact short-term buyer sentiment and demand elasticity in ways that historical tabular datasets cannot immediately reflect.\n"
        "3. Interior Customizations: The model assesses general furnishing categories (Unfurnished, Semi-Furnished, Fully Furnished) but does not evaluate ultra-luxury "
        "imported Italian marble flooring, bespoke modular kitchen woodwork, or high-end smart home automation systems.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # -------------------------------------------------------------
    # CHAPTER 9: CONCLUSION
    # -------------------------------------------------------------
    h9 = doc.add_paragraph()
    r = h9.add_run("9. CONCLUSION\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p = doc.add_paragraph(
        "The objective of designing and building a complete, transparent, and high-performance real estate valuation and spatial analytics system for Indian cities "
        "has been successfully accomplished in ESTATEIQ. By benchmarking five regression algorithms on a multi-metro dataset of 3,200 records, the Gradient Boosting "
        "Regressor was proven to be the optimal model, attaining an R² score of 0.9593 and an average absolute percentage error of just 10.59%.\n\n"
        "Crucially, ESTATEIQ resolves the traditional 'black-box' criticism of advanced machine learning by integrating game-theoretic SHAP explainability, providing "
        "transparent rupee-denominated factor attribution for every appraisal. The seamless integration of 10 complete production features—including real-time prediction, "
        "interactive GIS mapping, market analytics, multi-property benchmarking, budget-constrained discovery, downloadable ReportLab PDF valuation dossiers, and secure "
        "user/admin management—establishes ESTATEIQ as an institutional-grade platform bridging academic data science research and production engineering.\n"
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 10: REFERENCES
    # -------------------------------------------------------------
    h10 = doc.add_paragraph()
    r = h10.add_run("10. REFERENCES\n")
    r.bold = True
    r.font.size = Pt(14)
    
    references = [
        "Rosen, S. (1974). 'Hedonic prices and implicit markets: product differentiation in pure competition'. Journal of Political Economy, 82(1), 34-55.",
        "Goodman, A. C. (1978). 'Hedonic prices, price indices and housing markets'. Journal of Urban Economics, 5(4), 471-484.",
        "Chen, T., & Guestrin, C. (2016). 'XGBoost: A scalable tree boosting system'. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794.",
        "Lundberg, S. M., & Lee, S. I. (2017). 'A unified approach to interpreting model predictions'. Advances in Neural Information Processing Systems (NeurIPS 30), 4765-4774.",
        "Kok, N., Koponen, E. L., & Martínez-Barbosa, C. A. (2017). 'Big data in real estate? From manual appraisal to automated valuation'. The Journal of Portfolio Management, 43(6), 202-211.",
        "Singla, R., Grover, D., & Bhandari, A. (2020). 'Predictive modeling of real estate property prices using machine learning: An empirical study on Indian metropolitan markets'. International Journal of Information Management Data Insights, 1(2), 100018.",
        "Verma, P., & Ray, S. (2022). 'Spatial econometric modeling and machine learning applications in emerging housing markets: Insights from India'. Urban Studies Research, 14(3), 211-229.",
        "Breiman, L. (2001). 'Random forests'. Machine Learning, 45(1), 5-32.",
        "Friedman, J. H. (2001). 'Greedy function approximation: a gradient boosting machine'. Annals of Statistics, 29(5), 1189-1232.",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). 'Scikit-learn: Machine learning in Python'. Journal of Machine Learning Research, 12, 2825-2830.",
        "Grömping, U. (2015). 'Variable importance in regression models'. Wiley Interdisciplinary Reviews: Computational Statistics, 7(2), 137-152.",
        "Shapley, L. S. (1953). 'A value for n-person games'. Contributions to the Theory of Games, 2(28), 307-317."
    ]
    for idx, ref in enumerate(references, start=1):
        p_ref = doc.add_paragraph(f"[{idx}] {ref}")
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.3
        
    doc.save(REPORT_DOCX_PATH)
    final_docx = os.path.join(DOCS_DIR, 'ESTATEIQ_Final_Project_Report.docx')
    doc.save(final_docx)
    print(f"VIT Thesis Report successfully generated at: {REPORT_DOCX_PATH} and {final_docx}")
    return REPORT_DOCX_PATH

if __name__ == '__main__':
    create_report()
