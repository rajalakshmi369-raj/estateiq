# ESTATEIQ – AI-Powered House Price Prediction and Real Estate Analytics System for Indian Cities

<div align="center">

[![Live Dashboard](https://img.shields.io/badge/🚀_LAUNCH_LIVE_DASHBOARD-0A192F?style=for-the-badge&logo=googlechrome&logoColor=D4AF37)](https://rajalakshmi369-raj.github.io/estateiq/)
[![Download ZIP](https://img.shields.io/badge/📦_DOWNLOAD_PROJECT_ZIP-1E3A8A?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajalakshmi369-raj/estateiq/archive/refs/heads/main.zip)
[![Download PDF Report](https://img.shields.io/badge/📄_FINAL_REPORT_(PDF)-DC2626?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](https://github.com/rajalakshmi369-raj/estateiq/raw/main/docs/ESTATEIQ_Final_Project_Report.pdf)
[![Download DOCX Report](https://img.shields.io/badge/📝_FINAL_REPORT_(DOCX)-2563EB?style=for-the-badge&logo=microsoftword&logoColor=white)](https://github.com/rajalakshmi369-raj/estateiq/raw/main/docs/ESTATEIQ_Final_Project_Report.docx)

### 👉 **[https://rajalakshmi369-raj.github.io/estateiq/](https://rajalakshmi369-raj.github.io/estateiq/)** 👈
*(Anyone can touch or click the link above on mobile or PC to immediately run the live interactive dashboard!)*

</div>

---

**Enterprise Automated Valuation Models (AVM) & Spatial Analytics Platform**

---

## 🏢 Executive Overview

**ESTATEIQ** is an institutional-grade, AI-driven residential real estate valuation and spatial analytics web application engineered specifically for the dynamic property landscape of Indian metropolitan corridors. By synthesizing multi-variable econometric principles with state-of-the-art ensemble machine learning algorithms (Gradient Boosting, XGBoost, Random Forest, Decision Tree, Linear Regression) and game-theoretic SHAP (SHapley Additive exPlanations) interpretability, ESTATEIQ eliminates the traditional black-box opacity of Automated Valuation Models (AVMs).

The system models **21 spatial, architectural, directional (Vastu facing), vertical elevation (floor ratio), and society lifestyle attributes** across **3,200 transaction records** and **61 micro-market localities** spanning 12 Indian metropolitan cities: Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Gurgaon, Noida, Jaipur, and Kochi.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | Python 3.14 / 3.11+, Flask 3.1.3, Jinja2, Werkzeug Security |
| **Machine Learning** | Scikit-Learn 1.9.1, XGBoost 3.4.1, Joblib 1.6.0 |
| **Explainability (XAI)**| SHAP 0.54.1 (TreeExplainer game-theoretic local & global attribution) |
| **Data Engineering** | Pandas 3.0.6, NumPy 2.5.4 |
| **Database Management**| MySQL 8.0 (`estateiq_schema.sql`) with seamless SQLite3 zero-config automatic failover |
| **GIS Mapping** | Leaflet.js 1.9.4, OpenStreetMap Tiles, GeoJSON coordinate spatial mapping |
| **Interactive Analytics**| Plotly.js 2.30.0, Chart.js 4.4.2 |
| **PDF Generation** | ReportLab 5.1.0 (Automated valuation dossiers with confidence intervals) |
| **Frontend UI/UX** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3, FontAwesome 6, Custom Navy/Gold Theme |

---

## 🏛️ System Architecture

```mermaid
graph TD
    Client[Web Browser / User Interface] -->|HTTP / REST API| FlaskApp[Flask Application Controller app.py]
    
    subgraph Presentation Tier
        HTML[Jinja2 HTML5 Templates]
        CSS[Bootstrap 5 + Custom Navy/Gold CSS]
        Charts[Plotly & Chart.js Analytics]
        Maps[Leaflet.js GIS Mapping]
    end
    
    subgraph Application & Business Logic
        FlaskApp --> Auth[Werkzeug Password Auth]
        FlaskApp --> PredictService[Prediction Engine predict_service.py]
        FlaskApp --> PDFGen[ReportLab PDF Compiler pdf_generator.py]
        FlaskApp --> DBService[Database Adapter db.py]
    end
    
    subgraph Machine Learning Tier
        PredictService --> Preproc[97-Dim Preprocessor preprocessor.joblib]
        PredictService --> BestModel[Gradient Boosting Regressor best_model.joblib]
        PredictService --> SHAP[SHAP TreeExplainer Local Attribution]
    end
    
    subgraph Data Persistence Tier
        DBService --> MySQL[(MySQL 8.0 Server estateiq_db)]
        DBService -.->|Auto-Fallback| SQLite[(SQLite3 estateiq.db)]
        DBService --> CSV[(indian_housing_dataset.csv)]
    end
```

---

## 🔄 End-to-End Prediction Flowchart

```mermaid
flowchart TD
    A([User Input Form]) --> B[Extract 17 Physical & Spatial Attributes]
    B --> C[Compute Derived Features: Floor Ratio, Amenity Count]
    C --> D[Transform via EstateIQPreprocessor: StandardScaler + OneHotEncoder]
    D --> E[Inference via Gradient Boosting Regressor R2 = 0.9593]
    E --> F[Compute Valuation in INR, Price/sqft, and 90% Confidence Interval]
    E --> G[Execute SHAP TreeExplainer for Rupee-Denominated Value Drivers]
    E --> H[Locate Top 4 Nearest Similar Market Benchmark Properties]
    F & G & H --> I[Render Dynamic Interactive Valuation Dossier Page]
    I --> J[Generate Downloadable Certified ReportLab PDF Dossier]
```

---

## 🗄️ Relational Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o{ PREDICTIONS : creates
    USERS ||--o{ SAVED_PROPERTIES : shortlists
    PROPERTIES ||--o{ SAVED_PROPERTIES : referenced_by
    LOCATIONS ||--o{ PROPERTIES : encompasses

    USERS {
        int id PK
        string full_name
        string email UK
        string password_hash
        string role
        string phone
        string city
        timestamp created_at
    }

    PROPERTIES {
        int id PK
        string property_id UK
        int area_sqft
        string area_name
        string city
        string district
        string state
        int pincode
        int bedrooms
        int bathrooms
        int balcony
        string property_type
        int property_age
        string furnishing
        int parking
        int floor_number
        int total_floors
        string facing
        text amenities
        decimal latitude
        decimal longitude
        bigint price
        timestamp created_at
    }

    LOCATIONS {
        int id PK
        string city
        string district
        string state
        string area_name
        int pincode
        int avg_price_sqft
        int total_properties
        decimal latitude
        decimal longitude
        string tier
        timestamp updated_at
    }

    PREDICTIONS {
        int id PK
        int user_id FK
        text input_data_json
        string city
        string area_name
        int area_sqft
        int bedrooms
        string property_type
        bigint predicted_price
        int price_per_sqft
        bigint lower_bound
        bigint upper_bound
        string model_used
        timestamp created_at
    }

    SAVED_PROPERTIES {
        int id PK
        int user_id FK
        string property_id FK
        timestamp saved_at
    }

    MODEL_VERSIONS {
        int id PK
        string model_name
        string algorithm
        decimal r2_score
        bigint rmse
        bigint mae
        decimal mape
        boolean is_active
        timestamp trained_at
    }
```

---

## 🏆 Machine Learning Benchmarking Results

All five algorithms were trained on 2,560 records and rigorously validated on 640 unseen holdout test records:

| Regression Algorithm | MAE (₹) | RMSE (₹) | R² Score | Train R² | MAPE (%) | Ranking |
|---|---|---|---|---|---|---|
| **Gradient Boosting Regressor** | **₹ 25,58,616** | **₹ 47,91,877** | **0.9593** | **0.9781** | **10.59%** | 🥇 **Best Model** |
| **XGBoost Regressor** | ₹ 27,80,842 | ₹ 49,68,980 | 0.9562 | 0.9810 | 11.54% | 🥈 Second Best |
| **Random Forest Regressor** | ₹ 41,48,199 | ₹ 67,30,088 | 0.9197 | 0.9654 | 20.36% | 🥉 Third Best |
| **Decision Tree Regressor** | ₹ 54,50,376 | ₹ 91,13,484 | 0.8528 | 0.9312 | 26.27% | Baseline Tree |
| **Linear Regression (OLS)** | ₹ 57,66,571 | ₹ 1,06,97,962| 0.7971 | 0.8142 | 36.99% | Baseline Linear |

---

## ✨ 10 Main Features Summary

1. **Home Page & Portal Gateway (`/`)**: Navy Blue + White + Gold luxury aesthetic, interactive state/city search, live property counters, and featured listing cards.
2. **Smart House Price Prediction (`/predict`)**: Validated 17-attribute input form with dynamic cascading location selector, multi-select society amenities, algorithm chooser, and real-time inference.
3. **India Spatial Location Intelligence (`/location-intelligence`)**: Leaflet.js GIS interactive mapping with custom color-coded markers for Super-Luxury, Premium, and Mid-Affordable tiers across 61+ Indian localities.
4. **Market Analytics Dashboard (`/analytics`)**: Interactive Plotly and Chart.js charts covering city average prices, state capital deployment, BHK scaling, age depreciation curves, and Pearson correlation heatmap.
5. **Property Comparison Matrix (`/comparison`)**: Side-by-side benchmark of up to 3 properties with synchronized dual-axis charts and feature differential highlighting.
6. **Smart Recommendations Engine (`/recommendations`)**: Filter inventory by budget ceiling, city corridor, BHK configuration, asset type, and minimum carpet area.
7. **AI Price Explanation (`/explainability`)**: SHAP TreeExplainer attribution charts explaining why the model assigned a specific valuation in Indian Rupees.
8. **Budget-Based Property Finder (`/budget-finder`)**: Classifies properties into lowest-priced bargains, maximum space matches, and lowest rate-per-sqft options.
9. **Property Valuation PDF Report (`/download-report`)**: Programmatic compilation of downloadable, certified institutional appraisal reports via ReportLab.
10. **User & Admin Management Dashboards (`/dashboard`, `/admin`)**: Role-based access control, user valuation logs, property bookmarks, and admin model performance telemetry.

---

## 🚀 Quick Start & Installation Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14.7)
- Web browser (Chrome, Edge, Firefox)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database & Train Models (Automated)
```bash
# Generate 3,200 property dataset records
python data/generate_dataset.py

# Train all 5 regression models & save artifacts
python ml/train_models.py

# Initialize database schema & seed tables
python database/db.py
```

### Step 3: Run Web Application
```bash
python app.py
```
Or double-click `start_estateiq.bat`.

Open your browser at: **`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials

- **Administrator Account:**
  - Email: `admin@estateiq.in`
  - Password: `admin123`
- **Demo User Account:**
  - Email: `user@estateiq.in`
  - Password: `user123`

*(One-click autofill buttons are built directly into the `/login` interface for instant testing!)*
