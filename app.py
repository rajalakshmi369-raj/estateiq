"""
ESTATEIQ - Flask Application Main Controller
AI-Powered House Price Prediction & Real Estate Analytics System for Indian Cities
"""

import os
import sys
import json
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, send_file, make_response
)
from werkzeug.security import check_password_hash

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from database.db import (
    init_db, create_user, get_user_by_email, get_user_by_id, update_user_profile,
    save_prediction, get_user_predictions, get_recent_predictions,
    toggle_save_property, get_user_saved_properties, get_properties,
    get_property_by_id, get_locations_intelligence, get_distinct_locations,
    get_admin_dashboard_stats, delete_property_by_id
)
from ml.predict_service import (
    predict_property_price, format_inr, format_inr_full, get_dataset
)
from reports.pdf_generator import generate_valuation_pdf

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'frontend', 'static')
)
app.config.from_object(Config)

# Ensure database tables exist
init_db()

# --- Auth Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access your account dashboard.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Administrator privilege is required to access the control panel.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for templates
@app.context_processor
def inject_global_data():
    return {
        'logged_in': 'user_id' in session,
        'user_name': session.get('user_name', ''),
        'user_role': session.get('role', 'user'),
        'user_email': session.get('email', ''),
        'format_inr': format_inr,
        'format_inr_full': format_inr_full
    }

# ====================================================================
# 1. HOME & SEARCH (Feature 1)
# ====================================================================
@app.route('/')
def index():
    distinct_locs = get_distinct_locations()
    states = sorted(list(set(l['state'] for l in distinct_locs if l['state'])))
    cities = sorted(list(set(l['city'] for l in distinct_locs if l['city'])))
    
    # Featured properties
    featured_props = get_properties(limit=6)
    
    # Metrics preview
    df = get_dataset()
    stats = {
        'total_properties': f"{len(df):,}",
        'cities_covered': len(cities),
        'avg_price': format_inr(df['price'].mean()),
        'top_city': df.groupby('city')['price'].mean().idxmax()
    }
    
    return render_template('index.html', states=states, cities=cities, featured_props=featured_props, stats=stats)

# ====================================================================
# 2. SMART HOUSE PRICE PREDICTION (Feature 2 & 7)
# ====================================================================
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    distinct_locs = get_distinct_locations()
    states = sorted(list(set(l['state'] for l in distinct_locs if l['state'])))
    
    # Location map mapping state -> cities -> areas
    loc_hierarchy = {}
    for l in distinct_locs:
        s = l['state']
        c = l['city']
        a = l['area_name']
        p = l['pincode']
        if s not in loc_hierarchy:
            loc_hierarchy[s] = {}
        if c not in loc_hierarchy[s]:
            loc_hierarchy[s][c] = []
        loc_hierarchy[s][c].append({'area': a, 'pincode': p})
        
    if request.method == 'POST':
        try:
            # Extract form inputs
            state = request.form.get('state', 'Maharashtra')
            city = request.form.get('city', 'Mumbai')
            district = request.form.get('district', f"{city} District")
            area_name = request.form.get('area_name', 'Bandra West')
            pincode = int(request.form.get('pincode', 400050))
            area_sqft = float(request.form.get('area_sqft', 1200))
            bedrooms = int(request.form.get('bedrooms', 2))
            bathrooms = int(request.form.get('bathrooms', 2))
            balcony = int(request.form.get('balcony', 1))
            property_type = request.form.get('property_type', 'Apartment')
            property_age = int(request.form.get('property_age', 3))
            furnishing = request.form.get('furnishing', 'Semi-Furnished')
            parking = int(request.form.get('parking', 1))
            floor_number = int(request.form.get('floor_number', 4))
            total_floors = int(request.form.get('total_floors', 14))
            facing = request.form.get('facing', 'East')
            
            # Amenities multiselect
            amenities_list = request.form.getlist('amenities')
            amenities_str = ";".join(amenities_list) if amenities_list else "Gym;Lift;24x7 Security;Power Backup"
            
            # Selected model algorithm
            selected_algo = request.form.get('algorithm', 'best_model')
            
            prop_data = {
                'property_id': f"EQ-TEMP-{hash(f'{city}{area_name}{area_sqft}') % 10000}",
                'state': state,
                'city': city,
                'district': district,
                'area_name': area_name,
                'pincode': pincode,
                'area_sqft': area_sqft,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'balcony': balcony,
                'property_type': property_type,
                'property_age': property_age,
                'furnishing': furnishing,
                'parking': parking,
                'floor_number': floor_number,
                'total_floors': total_floors,
                'facing': facing,
                'amenities': amenities_str
            }
            
            # Predict
            pred_res = predict_property_price(prop_data, selected_model_name=selected_algo)
            
            # If user logged in, persist to history
            user_id = session.get('user_id')
            pred_id = save_prediction(user_id, prop_data, pred_res)
            
            # Store in session for immediate PDF generation
            session['latest_prediction'] = {
                'id': pred_id,
                'property_data': prop_data,
                'prediction_result': pred_res
            }
            
            return render_template(
                'prediction_result.html',
                prop_data=prop_data,
                result=pred_res,
                pred_id=pred_id
            )
            
        except Exception as e:
            flash(f"Prediction Error: {str(e)}", "danger")
            return redirect(url_for('predict'))
            
    return render_template('predict.html', states=states, loc_hierarchy=loc_hierarchy)

# ====================================================================
# 3. INDIA LOCATION INTELLIGENCE (Feature 3)
# ====================================================================
@app.route('/location-intelligence')
def location_intelligence():
    locations = get_locations_intelligence()
    distinct_locs = get_distinct_locations()
    states = sorted(list(set(l['state'] for l in distinct_locs if l['state'])))
    cities = sorted(list(set(l['city'] for l in distinct_locs if l['city'])))
    
    return render_template(
        'location_intelligence.html',
        locations=locations,
        states=states,
        cities=cities
    )

# ====================================================================
# 4. MARKET ANALYTICS DASHBOARD (Feature 4)
# ====================================================================
@app.route('/analytics')
def analytics():
    df = get_dataset()
    
    # 1. City-wise average price & sqft rate
    city_group = df.groupby('city').agg(
        avg_price=('price', 'mean'),
        avg_rate=('price', lambda p: (p / df.loc[p.index, 'area_sqft']).mean()),
        count=('property_id', 'count')
    ).reset_index().sort_values('avg_price', ascending=False)
    
    # 2. State-wise comparison
    state_group = df.groupby('state').agg(
        avg_price=('price', 'mean'),
        count=('property_id', 'count')
    ).reset_index().sort_values('avg_price', ascending=False)
    
    # 3. BHK vs Average Price
    bhk_group = df.groupby('bedrooms')['price'].mean().reset_index()
    
    # 4. Property Type distribution
    type_counts = df['property_type'].value_counts().to_dict()
    
    # 5. Age vs Price trend
    age_group = df.groupby('property_age')['price'].mean().reset_index()
    
    # Correlation numbers
    numeric_df = df[['area_sqft', 'bedrooms', 'bathrooms', 'property_age', 'parking', 'price']]
    corr_matrix = numeric_df.corr().round(2).to_dict()
    
    analytics_data = {
        'cities': city_group['city'].tolist(),
        'city_avg_prices': [round(p / 100000, 2) for p in city_group['avg_price'].tolist()], # In Lakhs
        'city_avg_rates': [round(r) for r in city_group['avg_rate'].tolist()],
        'states': state_group['state'].tolist(),
        'state_avg_prices': [round(p / 100000, 2) for p in state_group['avg_price'].tolist()],
        'bhks': [f"{int(b)} BHK" for b in bhk_group['bedrooms'].tolist()],
        'bhk_prices': [round(p / 100000, 2) for p in bhk_group['price'].tolist()],
        'types': list(type_counts.keys()),
        'type_counts': list(type_counts.values()),
        'ages': age_group['property_age'].tolist(),
        'age_prices': [round(p / 100000, 2) for p in age_group['price'].tolist()],
        'corr_matrix': corr_matrix
    }
    
    return render_template('analytics.html', data=analytics_data)

# ====================================================================
# 5. PROPERTY COMPARISON (Feature 5)
# ====================================================================
@app.route('/comparison')
def comparison():
    p1_id = request.args.get('p1', 'EQ-10001')
    p2_id = request.args.get('p2', 'EQ-10015')
    p3_id = request.args.get('p3', '')
    
    prop1 = get_property_by_id(p1_id)
    prop2 = get_property_by_id(p2_id)
    prop3 = get_property_by_id(p3_id) if p3_id else None
    
    all_props = get_properties(limit=50)
    
    return render_template(
        'comparison.html',
        prop1=prop1,
        prop2=prop2,
        prop3=prop3,
        all_props=all_props
    )

# ====================================================================
# 6. SMART PROPERTY RECOMMENDATIONS (Feature 6)
# ====================================================================
@app.route('/recommendations')
def recommendations():
    distinct_locs = get_distinct_locations()
    states = sorted(list(set(l['state'] for l in distinct_locs if l['state'])))
    cities = sorted(list(set(l['city'] for l in distinct_locs if l['city'])))
    
    # Filter params
    filters = {
        'city': request.args.get('city', 'All'),
        'state': request.args.get('state', 'All'),
        'bedrooms': request.args.get('bedrooms', 'All'),
        'property_type': request.args.get('property_type', 'All'),
        'max_price': request.args.get('max_price', ''),
        'min_area': request.args.get('min_area', ''),
        'sort_by': request.args.get('sort_by', 'newest')
    }
    
    clean_filters = {k: v for k, v in filters.items() if v and v != 'All'}
    props = get_properties(filters=clean_filters, limit=18)
    
    return render_template(
        'recommendations.html',
        properties=props,
        states=states,
        cities=cities,
        selected=filters
    )

# ====================================================================
# 7. AI PRICE EXPLANATION & SHAP DEEP DIVE (Feature 7)
# ====================================================================
@app.route('/explainability')
def explainability():
    metrics_path = os.path.join(BASE_DIR, 'models', 'model_metrics.json')
    meta = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            meta = json.load(f)
            
    return render_template('explainability.html', meta=meta)

# ====================================================================
# 8. BUDGET-BASED PROPERTY FINDER (Feature 8)
# ====================================================================
@app.route('/budget-finder')
def budget_finder():
    budget_raw = request.args.get('budget', '15000000') # Default 1.5 Cr
    try:
        budget = int(budget_raw)
    except ValueError:
        budget = 15000000
        
    city = request.args.get('city', 'All')
    
    df = get_dataset()
    filtered = df[df['price'] <= budget].copy()
    if city != 'All':
        filtered = filtered[filtered['city'] == city]
        
    # Categorize into: Lowest-Priced, Best Area/Value matches, High-End within Budget
    filtered['rate_sqft'] = filtered['price'] / filtered['area_sqft']
    
    lowest_priced = filtered.sort_values('price', ascending=True).head(4).to_dict('records')
    best_value = filtered.sort_values('rate_sqft', ascending=True).head(4).to_dict('records')
    max_space = filtered.sort_values('area_sqft', ascending=False).head(4).to_dict('records')
    
    distinct_locs = get_distinct_locations()
    cities = sorted(list(set(l['city'] for l in distinct_locs if l['city'])))
    
    return render_template(
        'budget_finder.html',
        budget=budget,
        budget_formatted=format_inr(budget),
        selected_city=city,
        cities=cities,
        total_matches=len(filtered),
        lowest_priced=lowest_priced,
        best_value=best_value,
        max_space=max_space
    )

# ====================================================================
# 9. PROPERTY VALUATION PDF REPORT (Feature 9)
# ====================================================================
@app.route('/download-report')
def download_report_latest():
    latest = session.get('latest_prediction')
    if not latest:
        flash("No recent valuation prediction found in session. Please run a prediction first.", "info")
        return redirect(url_for('predict'))
        
    pdf_path = generate_valuation_pdf(latest['property_data'], latest['prediction_result'])
    filename = os.path.basename(pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name=filename, mimetype='application/pdf')

@app.route('/download-report/<int:pred_id>')
def download_report_by_id(pred_id):
    # Retrieve prediction from DB
    from database.db import get_connection
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"SELECT * FROM predictions WHERE id = {ph}", (pred_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        flash("Valuation record not found.", "danger")
        return redirect(url_for('dashboard'))
        
    row_dict = dict(row)
    input_data = json.loads(row_dict['input_data_json'])
    pred_res = predict_property_price(input_data)
    
    pdf_path = generate_valuation_pdf(input_data, pred_res)
    return send_file(pdf_path, as_attachment=True, download_name=f"ESTATEIQ_Valuation_EQ{pred_id}.pdf", mimetype='application/pdf')

# ====================================================================
# PROJECT ZIP ARCHIVE DOWNLOAD (Feature for Examiner / Student)
# ====================================================================
@app.route('/download-project-zip')
def download_project_zip():
    zip_path = os.path.join(os.path.dirname(BASE_DIR), 'ESTATEIQ_Complete_Project.zip')
    if not os.path.exists(zip_path):
        # Fallback check in current dir
        zip_path = os.path.join(BASE_DIR, 'ESTATEIQ_Complete_Project.zip')
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name="ESTATEIQ_Complete_Project.zip", mimetype='application/zip')
    flash("Project ZIP package not found on server.", "warning")
    return redirect(url_for('index'))

# ====================================================================
# 10. USER & ADMIN DASHBOARDS & AUTH (Feature 10)
# ====================================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '')
        city = request.form.get('city', '')
        
        if not full_name or not email or not password:
            flash("Please fill in all mandatory fields.", "warning")
            return render_template('register.html')
            
        res = create_user(full_name, email, password, role="user", phone=phone, city=city)
        if res.get('success'):
            flash("Registration successful! You may now sign in.", "success")
            return redirect(url_for('login'))
        else:
            flash(f"Registration failed: {res.get('error', 'Email may already be registered.')}", "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['email'] = user['email']
            session['role'] = user['role']
            flash(f"Welcome back, {user['full_name']}!", "success")
            
            next_url = request.args.get('next')
            if user['role'] == 'admin' and (not next_url or next_url == url_for('login')):
                return redirect(url_for('admin_dashboard'))
            return redirect(next_url or url_for('dashboard'))
        else:
            flash("Invalid email or password credentials.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_id = session['user_id']
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        city = request.form.get('city')
        update_user_profile(user_id, full_name, phone, city)
        session['user_name'] = full_name
        flash("Profile information updated successfully.", "success")
        
    user = get_user_by_id(user_id)
    predictions = get_user_predictions(user_id)
    saved_props = get_user_saved_properties(user_id)
    
    return render_template(
        'user_dashboard.html',
        user=user,
        predictions=predictions,
        saved_props=saved_props
    )

@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = get_admin_dashboard_stats()
    recent_preds = get_recent_predictions(limit=10)
    all_props = get_properties(limit=25)
    return render_template('admin_dashboard.html', stats=stats, recent_preds=recent_preds, properties=all_props)

# ====================================================================
# REST API ENDPOINTS (For Interactive UI components)
# ====================================================================
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json() or {}
    try:
        res = predict_property_price(data, selected_model_name=data.get('algorithm', 'best_model'))
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/toggle-save/<property_id>', methods=['POST'])
@login_required
def api_toggle_save(property_id):
    user_id = session['user_id']
    saved = toggle_save_property(user_id, property_id)
    return jsonify({"success": True, "saved": saved})

@app.route('/api/admin/delete-property/<property_id>', methods=['POST'])
@admin_required
def api_delete_property(property_id):
    delete_property_by_id(property_id)
    return jsonify({"success": True, "message": f"Property {property_id} removed."})

@app.route('/api/locations-geojson')
def api_locations_geojson():
    locations = get_locations_intelligence()
    features = []
    for loc in locations:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(loc['longitude']), float(loc['latitude'])]
            },
            "properties": {
                "area_name": loc['area_name'],
                "city": loc['city'],
                "state": loc['state'],
                "avg_price_sqft": loc['avg_price_sqft'],
                "tier": loc['tier'],
                "total_properties": loc['total_properties'],
                "pincode": loc['pincode']
            }
        })
    return jsonify({"type": "FeatureCollection", "features": features})

if __name__ == '__main__':
    print("Starting ESTATEIQ Server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
