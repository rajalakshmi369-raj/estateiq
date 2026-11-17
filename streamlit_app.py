"""
ESTATEIQ - Interactive Cloud Dashboard
AI-Powered House Price Prediction & Real Estate Analytics System for Indian Cities
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.predict_service import (
    predict_property_price, format_inr, format_inr_full, get_dataset
)
from reports.pdf_generator import generate_valuation_pdf

# Page configuration
st.set_page_config(
    page_title="ESTATEIQ - AI Real Estate Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Navy Blue + White + Gold Theme)
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .stApp { font-family: 'Inter', sans-serif; }
    .header-box {
        background: linear-gradient(135deg, #0A192F 0%, #172A45 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #D4AF37;
        color: white;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        border-left: 4px solid #D4AF37;
        box-shadow: 0 2px 6px rgba(10,25,47,0.06);
    }
    .val-banner {
        background: linear-gradient(135deg, #0A192F 0%, #112240 100%);
        border: 2px solid #D4AF37;
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .val-price {
        font-size: 2.8rem;
        font-weight: 800;
        color: #D4AF37;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

df = get_dataset()

# Sidebar Navigation
st.sidebar.markdown("""
<div style="text-align:center; padding: 10px 0;">
    <h2 style="color: #0A192F; font-weight: 800; margin-bottom: 0;">ESTATE<span style="color:#D4AF37;">IQ</span></h2>
    <span style="font-size: 0.75rem; background: #0A192F; color: #D4AF37; padding: 2px 8px; border-radius: 4px; font-weight: 600;">AI REAL ESTATE INTELLIGENCE</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Explore System Modules:",
    [
        "🏠 1. Home & Overview",
        "🎯 2. Smart Price Predictor",
        "🗺️ 3. India Location Intelligence",
        "📊 4. Market Analytics Dashboard",
        "⚖️ 5. Property Comparison Matrix",
        "👍 6. Smart Recommendations",
        "🧠 7. AI Explainability (SHAP)",
        "💰 8. Budget-Based Finder",
        "📑 9. Download Official Reports",
        "⚙️ 10. System Architecture & Info"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**ESTATEIQ Enterprise Platform**  
*AI Real Estate Valuation & Analytics*  
**Production Engine:** Gradient Boosting ($R^2 = 0.9593$)
""")

# ====================================================================
# PAGE 1: HOME & OVERVIEW
# ====================================================================
if page == "🏠 1. Home & Overview":
    st.markdown("""
    <div class="header-box">
        <span style="background: rgba(212,175,55,0.25); color: #D4AF37; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 700;">
            INSTITUTIONAL AI REAL ESTATE VALUATION
        </span>
        <h1 style="color: white; font-weight: 800; margin-top: 10px;">ESTATEIQ – Multi-Metro Real Estate Intelligence</h1>
        <p style="color: #CBD5E1; font-size: 1.05rem; max-width: 850px; margin-bottom: 0;">
            Harnessing supervised ensemble learning (Gradient Boosting, XGBoost, Random Forest) and game-theoretic SHAP 
            interpretability to deliver transparent fair market valuations across 12 Indian metropolitan hubs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600;">CATALOGED INVENTORY</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0A192F;">{len(df):,} Records</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600;">METROS COVERED</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0A192F;">12 Cities (61 Areas)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_p = df['price'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600;">MEAN METRO VALUATION</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0A192F;">{format_inr(avg_p)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 600;">MODEL CONFIDENCE</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #10B981;">95.93% (R²)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Featured Verified Market Inventory")
    sample_view = df[['property_id', 'area_name', 'city', 'state', 'bedrooms', 'area_sqft', 'property_type', 'furnishing', 'price']].head(8).copy()
    sample_view['Valuation'] = sample_view['price'].apply(format_inr)
    sample_view['Rate/sqft'] = (sample_view['price'] / sample_view['area_sqft']).round().astype(int).apply(lambda r: f"₹ {r:,}/sqft")
    st.dataframe(
        sample_view[['property_id', 'area_name', 'city', 'bedrooms', 'area_sqft', 'property_type', 'furnishing', 'Rate/sqft', 'Valuation']],
        use_container_width=True,
        hide_index=True
    )

# ====================================================================
# PAGE 2: SMART HOUSE PRICE PREDICTOR
# ====================================================================
elif page == "🎯 2. Smart Price Predictor":
    st.title("🎯 Smart House Price Predictor")
    st.write("Configure physical, architectural, and locality parameters to obtain an instant ML-powered appraisal with SHAP value drivers.")

    cities_list = sorted(df['city'].unique().tolist())
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. Location & Geography")
        city_sel = st.selectbox("Select Metro City:", cities_list, index=cities_list.index("Bengaluru") if "Bengaluru" in cities_list else 0)
        localities = sorted(df[df['city'] == city_sel]['area_name'].unique().tolist())
        area_sel = st.selectbox("Locality / Micro-Market:", localities)
        
        # Auto-pick state, district, pincode
        loc_row = df[(df['city'] == city_sel) & (df['area_name'] == area_sel)].iloc[0]
        state_val = loc_row['state']
        district_val = loc_row['district']
        pincode_val = int(loc_row['pincode'])
        
        st.caption(f"**State:** {state_val} | **District:** {district_val} | **PIN Code:** {pincode_val}")

        st.subheader("2. Space & Configuration")
        sqft_val = st.slider("Super Built-up Area (Sq.Ft):", min_value=400, max_value=6000, value=1450, step=50)
        bhk_val = st.selectbox("Bedrooms (BHK):", [1, 2, 3, 4, 5], index=2)
        baths_val = st.selectbox("Bathrooms:", [1, 2, 3, 4, 5], index=2)
        balcony_val = st.selectbox("Balconies:", [0, 1, 2, 3, 4], index=2)

    with col_b:
        st.subheader("3. Asset Classification")
        prop_types = ["Apartment", "Independent House", "Villa", "Penthouse", "Builder Floor"]
        pt_val = st.selectbox("Property Type:", prop_types)
        furn_val = st.selectbox("Furnishing Status:", ["Unfurnished", "Semi-Furnished", "Fully Furnished"], index=1)
        age_val = st.slider("Property Age (Years):", 0, 25, 2)
        facing_val = st.selectbox("Vastu Direction Facing:", ["East", "North", "North-East", "West", "North-West", "South"])
        parking_val = st.selectbox("Reserved Parking Bays:", [0, 1, 2, 3], index=2)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            floor_val = st.number_input("Floor Number:", min_value=0, max_value=50, value=7)
        with col_f2:
            total_f_val = st.number_input("Total Floors:", min_value=1, max_value=50, value=18)

        st.subheader("4. Machine Learning Model")
        algo_choice = st.selectbox(
            "Select Regression Algorithm:",
            [
                ("gradient_boosting_regressor", "Gradient Boosting (Recommended - Best R²: 0.9593)"),
                ("xgboost_regressor", "XGBoost Regressor (R²: 0.9562)"),
                ("random_forest_regressor", "Random Forest Regressor (R²: 0.9197)"),
                ("decision_tree_regressor", "Decision Tree Regressor (R²: 0.8528)"),
                ("linear_regression", "Linear Regression (OLS) (R²: 0.7971)")
            ],
            format_func=lambda x: x[1]
        )[0]

    st.subheader("5. Society Amenities")
    all_amenities = ["Gym", "Swimming Pool", "Clubhouse", "24x7 Security", "Power Backup", "Lift", "Children Play Area", "Jogging Track", "Intercom", "CCTV", "Rainwater Harvesting", "Landscaped Garden", "Covered Parking", "Fire Safety"]
    sel_amenities = st.multiselect("Select Amenities:", all_amenities, default=["Gym", "Swimming Pool", "Clubhouse", "24x7 Security", "Lift", "Power Backup"])

    if st.button("🚀 PREDICT FAIR MARKET VALUE NOW", type="primary", use_container_width=True):
        prop_payload = {
            'property_id': 'EQ-LIVE-APPRAISAL',
            'city': city_sel,
            'area_name': area_sel,
            'state': state_val,
            'district': district_val,
            'pincode': pincode_val,
            'area_sqft': sqft_val,
            'bedrooms': bhk_val,
            'bathrooms': baths_val,
            'balcony': balcony_val,
            'property_type': pt_val,
            'property_age': age_val,
            'furnishing': furn_val,
            'parking': parking_val,
            'floor_number': floor_val,
            'total_floors': total_f_val,
            'facing': facing_val,
            'amenities': ";".join(sel_amenities)
        }
        
        with st.spinner("Executing ML Inference & SHAP Local Attribution..."):
            pred_res = predict_property_price(prop_payload, selected_model_name=algo_choice)

        st.markdown(f"""
        <div class="val-banner">
            <span style="color: #CBD5E1; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Estimated Fair Market Value</span>
            <div class="val-price">{pred_res['predicted_price_formatted']}</div>
            <div style="font-size: 1.1rem; color: #E2E8F0; font-family: monospace;">{pred_res['predicted_price_full']}</div>
            <div style="margin-top: 10px;">
                <span style="background: rgba(212,175,55,0.2); padding: 4px 12px; border-radius: 20px; font-weight: 600; color: #D4AF37; margin-right: 8px;">
                    Rate: {pred_res['price_per_sqft_formatted']}
                </span>
                <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; color: #E2E8F0;">
                    90% Confidence Interval: {pred_res['uncertainty_range']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_sh1, col_sh2 = st.columns([3, 2])
        with col_sh1:
            st.subheader("AI Price Explanation (SHAP Value Drivers)")
            shap_df = pd.DataFrame(pred_res['shap_breakdown'])
            shap_df['Impact (Lakhs)'] = shap_df['impact_inr'] / 100000
            
            fig = px.bar(
                shap_df,
                x='Impact (Lakhs)',
                y='factor',
                orientation='h',
                color='is_positive',
                color_discrete_map={True: '#10B981', False: '#EF4444'},
                title="Marginal Monetary Impact Against Baseline Metro Average (₹ in Lakhs)"
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'}, height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col_sh2:
            st.subheader("Certified Appraisal Dossier")
            st.write("Generate a formal institutional appraisal dossier containing full architectural specifications, SHAP drivers, and market benchmark comps.")
            
            pdf_path = generate_valuation_pdf(prop_payload, pred_res)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Certified Valuation PDF Report",
                    data=f.read(),
                    file_name=f"ESTATEIQ_Valuation_{city_sel}_{area_sel}.pdf",
                    mime="application/pdf",
                    type="primary"
                )

        st.subheader("Similar Locality Market Comps")
        sims = pd.DataFrame(pred_res['similar_properties'])
        if not sims.empty:
            st.dataframe(sims[['property_id', 'area_name', 'bedrooms', 'area_sqft', 'price_per_sqft', 'price_formatted']], hide_index=True, use_container_width=True)

# ====================================================================
# PAGE 3: INDIA LOCATION INTELLIGENCE
# ====================================================================
elif page == "🗺️ 3. India Location Intelligence":
    st.title("🗺️ India Spatial Location Intelligence")
    st.write("Explore average price per square foot across 61+ micro-market corridors in 12 Indian metropolitan hubs.")

    loc_df = df.groupby(['city', 'state', 'area_name']).agg(
        avg_price=('price', 'mean'),
        avg_rate=('price', lambda p: (p / df.loc[p.index, 'area_sqft']).mean()),
        lat=('latitude', 'mean'),
        lon=('longitude', 'mean'),
        count=('property_id', 'count')
    ).reset_index()

    loc_df['avg_rate'] = loc_df['avg_rate'].round().astype(int)
    loc_df['Tier'] = loc_df['avg_rate'].apply(lambda r: "Super-Luxury (> ₹20k)" if r > 20000 else ("Premium (₹11k-20k)" if r > 11000 else "Mid-Affordable (< ₹11k)"))

    # Map visualization via Plotly Scatter Map
    fig = px.scatter_map(
        loc_df,
        lat="lat",
        lon="lon",
        hover_name="area_name",
        hover_data={"city": True, "state": True, "avg_rate": True, "count": True, "lat": False, "lon": False},
        color="Tier",
        size="count",
        color_discrete_map={
            "Super-Luxury (> ₹20k)": "#8B5CF6",
            "Premium (₹11k-20k)": "#0A192F",
            "Mid-Affordable (< ₹11k)": "#10B981"
        },
        zoom=4.5,
        center={"lat": 21.5, "lon": 78.5},
        height=580,
        title="Indian Micro-Markets Capital Concentration Map"
    )
    fig.update_layout(map_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Micro-Market Directory & Rate Card")
    st.dataframe(
        loc_df[['city', 'state', 'area_name', 'avg_rate', 'Tier', 'count']].sort_values('avg_rate', ascending=False),
        use_container_width=True,
        hide_index=True
    )

# ====================================================================
# PAGE 4: MARKET ANALYTICS DASHBOARD
# ====================================================================
elif page == "📊 4. Market Analytics Dashboard":
    st.title("📊 Indian Real Estate Market Analytics Dashboard")
    st.write("Exploratory Data Analysis (EDA) and econometric distributions derived from 3,200 verified property transactions.")

    c1, c2 = st.columns(2)
    with c1:
        city_grp = df.groupby('city')['price'].mean().reset_index().sort_values('price', ascending=False)
        city_grp['price_lakhs'] = (city_grp['price'] / 100000).round(2)
        fig1 = px.bar(city_grp, x='city', y='price_lakhs', title="Average Property Valuation by Indian Metro (₹ in Lakhs)", color_discrete_sequence=['#0A192F'])
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        df['rate_sqft'] = df['price'] / df['area_sqft']
        rate_grp = df.groupby('city')['rate_sqft'].mean().reset_index().sort_values('rate_sqft', ascending=False)
        fig2 = px.bar(rate_grp, x='city', y='rate_sqft', title="Average Rate Per Square Foot by Metro (₹ / sq.ft)", color_discrete_sequence=['#D4AF37'])
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        bhk_grp = df.groupby('bedrooms')['price'].mean().reset_index()
        bhk_grp['price_lakhs'] = (bhk_grp['price'] / 100000).round(2)
        fig3 = px.bar(bhk_grp, x='bedrooms', y='price_lakhs', title="Configuration (BHK) vs. Mean Outlay (₹ in Lakhs)", color_discrete_sequence=['#2563EB'])
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.pie(df, names='property_type', title="Asset Class Breakdown", hole=0.45, color_discrete_sequence=['#0A192F', '#D4AF37', '#10B981', '#3B82F6', '#8B5CF6'])
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Feature Correlation Matrix (Pearson's r)")
    corr = df[['area_sqft', 'bedrooms', 'bathrooms', 'property_age', 'parking', 'price']].corr().round(2)
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale=[(0, "#3B82F6"), (0.5, "#F1F5F9"), (1, "#D4AF37")])
    st.plotly_chart(fig_corr, use_container_width=True)

# ====================================================================
# PAGE 5: PROPERTY COMPARISON MATRIX
# ====================================================================
elif page == "⚖️ 5. Property Comparison Matrix":
    st.title("⚖️ Multi-Property Comparison Matrix")
    st.write("Benchmark up to three properties side-by-side on pricing, area efficiency, and architectural metrics.")

    prop_ids = df['property_id'].tolist()
    c1, c2, c3 = st.columns(3)
    with c1:
        p1 = st.selectbox("Slot 1 Property:", prop_ids, index=0)
    with c2:
        p2 = st.selectbox("Slot 2 Property:", prop_ids, index=14)
    with c3:
        p3 = st.selectbox("Slot 3 Property (Optional):", ["None"] + prop_ids, index=0)

    selected = [p1, p2]
    if p3 != "None":
        selected.append(p3)

    comp_df = df[df['property_id'].isin(selected)].copy()
    comp_df['Valuation'] = comp_df['price'].apply(format_inr)
    comp_df['Rate/sqft'] = (comp_df['price'] / comp_df['area_sqft']).round().astype(int).apply(lambda r: f"₹ {r:,}/sqft")

    # Bar chart
    fig = px.bar(
        comp_df,
        x='property_id',
        y=['area_sqft', 'price'],
        barmode='group',
        title="Comparison Metrics (Area & Price)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        comp_df[['property_id', 'city', 'area_name', 'bedrooms', 'bathrooms', 'area_sqft', 'property_type', 'furnishing', 'Rate/sqft', 'Valuation']],
        hide_index=True,
        use_container_width=True
    )

# ====================================================================
# PAGE 6: SMART RECOMMENDATIONS
# ====================================================================
elif page == "👍 6. Smart Recommendations":
    st.title("👍 Smart Property Recommendations")
    st.write("Algorithmic multi-criteria property matching constrained to your preferences.")

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        rec_city = st.selectbox("Target City:", ["All"] + sorted(df['city'].unique().tolist()))
    with col_r2:
        rec_bhk = st.selectbox("Configuration:", ["All", 1, 2, 3, 4, 5])
    with col_r3:
        rec_max_p = st.selectbox("Budget Limit:", [
            ("All", "Any Budget"),
            (6000000, "Up to ₹ 60 Lakhs"),
            (12000000, "Up to ₹ 1.2 Crores"),
            (25000000, "Up to ₹ 2.5 Crores"),
            (50000000, "Up to ₹ 5.0 Crores")
        ], format_func=lambda x: x[1])[0]

    filtered = df.copy()
    if rec_city != "All":
        filtered = filtered[filtered['city'] == rec_city]
    if rec_bhk != "All":
        filtered = filtered[filtered['bedrooms'] == int(rec_bhk)]
    if rec_max_p != "All":
        filtered = filtered[filtered['price'] <= int(rec_max_p)]

    st.write(f"Found **{len(filtered)}** Matching Properties:")
    filtered['Valuation'] = filtered['price'].apply(format_inr)
    st.dataframe(filtered[['property_id', 'area_name', 'city', 'bedrooms', 'area_sqft', 'property_type', 'furnishing', 'Valuation']].head(20), hide_index=True, use_container_width=True)

# ====================================================================
# PAGE 7: AI EXPLAINABILITY (SHAP)
# ====================================================================
elif page == "🧠 7. AI Explainability (SHAP)":
    st.title("🧠 AI Explainability & 5-Model Benchmark")
    st.write("Game-theoretic SHAP interpretability and comparative evaluation across all 5 regression algorithms.")

    meta_path = os.path.join(BASE_DIR, 'models', 'model_metrics.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)

        m_dict = meta.get('models_evaluated', {})
        eval_rows = []
        for name, m in m_dict.items():
            eval_rows.append({
                "Algorithm": name,
                "R² Score": m['R2_Score'],
                "RMSE (₹)": f"₹ {m['RMSE']:,}",
                "MAE (₹)": f"₹ {m['MAE']:,}",
                "MAPE (%)": f"{m['MAPE']}%",
                "Train R²": m['Train_R2'],
                "Status": "👑 Best Model" if name == meta.get('best_model_name') else "Evaluated"
            })
        st.subheader("5-Model Quantitative Benchmark (Holdout Test Samples)")
        st.dataframe(pd.DataFrame(eval_rows), hide_index=True, use_container_width=True)

        st.subheader("Global Feature Importance Rankings (Gradient Boosting Engine)")
        top_f = meta.get('top_feature_importances', [])[:10]
        f_df = pd.DataFrame(top_f)
        f_df['Feature'] = f_df['feature'].str.replace('cat__', '').str.replace('city_', 'City: ').str.replace('area_name_', 'Locality: ')
        fig = px.bar(f_df, x='importance', y='Feature', orientation='h', title="Top Feature Importance Weights", color_discrete_sequence=['#0A192F'])
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

# ====================================================================
# PAGE 8: BUDGET-BASED FINDER
# ====================================================================
elif page == "💰 8. Budget-Based Finder":
    st.title("💰 Budget-Calibrated Property Finder")
    st.write("Discover lowest-priced bargains, maximum space, and best rate-per-sqft within your budget ceiling.")

    bud_val = st.slider("Select Maximum Budget Ceiling (INR):", min_value=2500000, max_value=60000000, value=15000000, step=1000000)
    st.write(f"Current Filter: **{format_inr(bud_val)}** ({format_inr_full(bud_val)})")

    b_match = df[df['price'] <= bud_val].copy()
    b_match['rate_sqft'] = b_match['price'] / b_match['area_sqft']
    b_match['Valuation'] = b_match['price'].apply(format_inr)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Lowest-Priced Bargains (Maximum Savings)")
        low_p = b_match.sort_values('price', ascending=True).head(5)
        st.dataframe(low_p[['property_id', 'area_name', 'city', 'bedrooms', 'area_sqft', 'Valuation']], hide_index=True, use_container_width=True)

    with c2:
        st.subheader("2. Maximum Living Space (Largest Sq.Ft)")
        max_s = b_match.sort_values('area_sqft', ascending=False).head(5)
        st.dataframe(max_s[['property_id', 'area_name', 'city', 'bedrooms', 'area_sqft', 'Valuation']], hide_index=True, use_container_width=True)

# ====================================================================
# PAGE 9: DOWNLOAD OFFICIAL REPORTS
# ====================================================================
elif page == "📑 9. Download Official Reports":
    st.title("📑 Download System Documentation & Reports")
    st.write("Download comprehensive valuation documentation, reports, and dataset assets.")

    pdf_doc = os.path.join(BASE_DIR, 'docs', 'ESTATEIQ_Comprehensive_Project_Report.pdf')
    docx_doc = os.path.join(BASE_DIR, 'docs', 'ESTATEIQ_Comprehensive_Project_Report.docx')
    csv_doc = os.path.join(BASE_DIR, 'data', 'indian_housing_dataset.csv')
    sql_doc = os.path.join(BASE_DIR, 'database', 'estateiq_schema.sql')

    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists(pdf_doc):
            with open(pdf_doc, "rb") as f:
                st.download_button(
                    label="📕 Download Comprehensive Valuation Report (PDF)",
                    data=f.read(),
                    file_name="ESTATEIQ_Comprehensive_Project_Report.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
        if os.path.exists(docx_doc):
            with open(docx_doc, "rb") as f:
                st.download_button(
                    label="📘 Download Comprehensive Valuation Report (DOCX)",
                    data=f.read(),
                    file_name="ESTATEIQ_Comprehensive_Project_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

    with col2:
        if os.path.exists(csv_doc):
            with open(csv_doc, "rb") as f:
                st.download_button(
                    label="📊 Download Indian Housing Dataset (CSV - 3,200 Records)",
                    data=f.read(),
                    file_name="indian_housing_dataset.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        if os.path.exists(sql_doc):
            with open(sql_doc, "rb") as f:
                st.download_button(
                    label="🗄️ Download MySQL Database DDL Schema (SQL)",
                    data=f.read(),
                    file_name="estateiq_schema.sql",
                    mime="application/sql",
                    use_container_width=True
                )

# ====================================================================
# PAGE 10: SYSTEM ARCHITECTURE & INFO
# ====================================================================
elif page == "⚙️ 10. System Architecture & Info":
    st.title("⚙️ System Architecture & Engineering")
    st.markdown("""
    ### 🏛️ Modular Design
    1. **Data Layer:** 3,200 records across 12 Indian metros in `indian_housing_dataset.csv`.
    2. **Preprocessing Pipeline:** 97-dimensional transformation (`StandardScaler` + `OneHotEncoder`).
    3. **Ensemble ML Core:** Gradient Boosting Regressor ($R^2 = 0.9593$), XGBoost, Random Forest, Decision Tree, Linear Regression.
    4. **Explainability Engine:** SHAP (SHapley Additive exPlanations) TreeExplainer.
    5. **Database:** MySQL 8.0 schema with automatic SQLite failover.
    6. **Web Tier:** Dual deployment in Python Flask and Streamlit.
    """)
