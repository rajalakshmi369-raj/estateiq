"""
ESTATEIQ - Unified Database Interface Layer
Supports MySQL database server with seamless SQLite automatic failover
to ensure zero-dependency, out-of-the-box local execution.
"""

import os
import sys
import json
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'database')
SQLITE_PATH = os.path.join(DB_DIR, 'estateiq.db')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'indian_housing_dataset.csv')
METRICS_PATH = os.path.join(BASE_DIR, 'models', 'model_metrics.json')

# MySQL default configuration
MYSQL_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "db": os.environ.get("MYSQL_DB", "estateiq_db")
}

def get_connection():
    """Tries connecting to MySQL, falls back to SQLite seamlessly."""
    try:
        import pymysql
        conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["db"],
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=1
        )
        return conn, "mysql"
    except Exception:
        # Fallback to SQLite
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn, "sqlite"

def init_db():
    """Initializes tables in database."""
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    if db_type == "sqlite":
        # SQLite schema
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            phone TEXT,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL UNIQUE,
            area_sqft INTEGER NOT NULL,
            area_name TEXT NOT NULL,
            city TEXT NOT NULL,
            district TEXT NOT NULL,
            state TEXT NOT NULL,
            pincode INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            balcony INTEGER DEFAULT 1,
            property_type TEXT NOT NULL,
            property_age INTEGER NOT NULL,
            furnishing TEXT NOT NULL,
            parking INTEGER DEFAULT 1,
            floor_number INTEGER DEFAULT 1,
            total_floors INTEGER DEFAULT 1,
            facing TEXT DEFAULT 'East',
            amenities TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            price INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            district TEXT NOT NULL,
            state TEXT NOT NULL,
            area_name TEXT NOT NULL,
            pincode INTEGER NOT NULL,
            avg_price_sqft INTEGER NOT NULL,
            total_properties INTEGER DEFAULT 0,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            tier TEXT DEFAULT 'Standard',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(city, area_name)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            input_data_json TEXT NOT NULL,
            city TEXT NOT NULL,
            area_name TEXT NOT NULL,
            area_sqft INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            property_type TEXT NOT NULL,
            predicted_price INTEGER NOT NULL,
            price_per_sqft INTEGER NOT NULL,
            lower_bound INTEGER NOT NULL,
            upper_bound INTEGER NOT NULL,
            model_used TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            property_id TEXT NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, property_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (property_id) REFERENCES properties(property_id) ON DELETE CASCADE
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            r2_score REAL NOT NULL,
            rmse INTEGER NOT NULL,
            mae INTEGER NOT NULL,
            mape REAL NOT NULL,
            is_active INTEGER DEFAULT 0,
            trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

    # Seed default Admin and Demo user
    create_default_users(conn, db_type)
    # Seed properties and locations if empty
    seed_properties_if_empty(conn, db_type)
    # Seed model metrics
    seed_model_metrics(conn, db_type)
    
    conn.close()
    print(f"Database initialized successfully using {db_type.upper()}.")

def create_default_users(conn, db_type):
    cursor = conn.cursor()
    # Check if admin exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@estateiq.in",) if db_type == "sqlite" else ("admin@estateiq.in",))
    res = cursor.fetchone()
    if not res:
        admin_hash = generate_password_hash("admin123")
        user_hash = generate_password_hash("user123")
        
        ph = "?" if db_type == "sqlite" else "%s"
        cursor.execute(
            f"INSERT INTO users (full_name, email, password_hash, role, phone, city) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})",
            ("System Administrator", "admin@estateiq.in", admin_hash, "admin", "+91 98765 43210", "Bengaluru")
        )
        cursor.execute(
            f"INSERT INTO users (full_name, email, password_hash, role, phone, city) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})",
            ("Demo User", "user@estateiq.in", user_hash, "user", "+91 98111 22334", "Mumbai")
        )
        conn.commit()

def seed_properties_if_empty(conn, db_type):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM properties")
    row = cursor.fetchone()
    cnt = row[0] if isinstance(row, tuple) else row['cnt']
    
    if cnt == 0 and os.path.exists(DATA_PATH):
        print("Seeding properties from dataset...")
        df = pd.read_csv(DATA_PATH)
        
        ph = "?" if db_type == "sqlite" else "%s"
        sql_prop = f"""
        INSERT INTO properties (
            property_id, area_sqft, area_name, city, district, state, pincode,
            bedrooms, bathrooms, balcony, property_type, property_age, furnishing,
            parking, floor_number, total_floors, facing, amenities, latitude, longitude, price
        ) VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})
        """
        
        prop_rows = []
        for _, r in df.iterrows():
            prop_rows.append((
                str(r['property_id']), int(r['area_sqft']), str(r['area_name']), str(r['city']),
                str(r['district']), str(r['state']), int(r['pincode']), int(r['bedrooms']),
                int(r['bathrooms']), int(r['balcony']), str(r['property_type']), int(r['property_age']),
                str(r['furnishing']), int(r['parking']), int(r['floor_number']), int(r['total_floors']),
                str(r['facing']), str(r['amenities']), float(r['latitude']), float(r['longitude']), int(r['price'])
            ))
            
        cursor.executemany(sql_prop, prop_rows)
        conn.commit()
        
        # Populate aggregated locations table
        print("Populating aggregated locations table...")
        df['rate_per_sqft'] = df['price'] / df['area_sqft']
        loc_summary = df.groupby(['city', 'district', 'state', 'area_name', 'pincode']).agg(
            avg_rate=('rate_per_sqft', 'mean'),
            total_props=('property_id', 'count'),
            lat=('latitude', 'mean'),
            lon=('longitude', 'mean')
        ).reset_index()
        
        sql_loc = f"""
        INSERT INTO locations (
            city, district, state, area_name, pincode, avg_price_sqft, total_properties, latitude, longitude, tier
        ) VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})
        """
        loc_rows = []
        for _, l in loc_summary.iterrows():
            avg_rate = int(round(l['avg_rate']))
            tier = "Super-Luxury" if avg_rate > 20000 else ("Premium" if avg_rate > 11000 else "Standard")
            loc_rows.append((
                str(l['city']), str(l['district']), str(l['state']), str(l['area_name']),
                int(l['pincode']), avg_rate, int(l['total_props']),
                round(float(l['lat']), 6), round(float(l['lon']), 6), tier
            ))
        cursor.executemany(sql_loc, loc_rows)
        conn.commit()
        print(f"Seeded {len(prop_rows)} properties and {len(loc_rows)} locations.")

def seed_model_metrics(conn, db_type):
    if not os.path.exists(METRICS_PATH):
        return
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM model_versions")
    row = cursor.fetchone()
    cnt = row[0] if isinstance(row, tuple) else row['cnt']
    
    if cnt == 0:
        with open(METRICS_PATH, 'r') as f:
            meta = json.load(f)
            
        models_dict = meta.get('models_evaluated', {})
        best_name = meta.get('best_model_name', '')
        
        ph = "?" if db_type == "sqlite" else "%s"
        sql = f"""
        INSERT INTO model_versions (model_name, algorithm, r2_score, rmse, mae, mape, is_active)
        VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
        """
        rows = []
        for name, metrics in models_dict.items():
            is_active = 1 if name == best_name else 0
            rows.append((
                name, name, float(metrics['R2_Score']), int(metrics['RMSE']),
                int(metrics['MAE']), float(metrics['MAPE']), is_active
            ))
        cursor.executemany(sql, rows)
        conn.commit()

# --- Auth Helper Methods ---

def create_user(full_name, email, password, role="user", phone="", city=""):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    pwd_hash = generate_password_hash(password)
    ph = "?" if db_type == "sqlite" else "%s"
    try:
        cursor.execute(
            f"INSERT INTO users (full_name, email, password_hash, role, phone, city) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})",
            (full_name, email.strip().lower(), pwd_hash, role, phone, city)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"success": True, "user_id": user_id}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_user_by_email(email):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"SELECT * FROM users WHERE email = {ph}", (email.strip().lower(),))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def get_user_by_id(user_id):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"SELECT * FROM users WHERE id = {ph}", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def update_user_profile(user_id, full_name, phone, city):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(
        f"UPDATE users SET full_name = {ph}, phone = {ph}, city = {ph} WHERE id = {ph}",
        (full_name, phone, city, user_id)
    )
    conn.commit()
    conn.close()
    return True

# --- Prediction & Saved Properties ---

def save_prediction(user_id, input_dict, pred_result):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    
    cursor.execute(
        f"""
        INSERT INTO predictions (
            user_id, input_data_json, city, area_name, area_sqft, bedrooms,
            property_type, predicted_price, price_per_sqft, lower_bound, upper_bound, model_used
        ) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
        """,
        (
            user_id, json.dumps(input_dict), input_dict.get('city', ''),
            input_dict.get('area_name', ''), int(input_dict.get('area_sqft', 0)),
            int(input_dict.get('bedrooms', 0)), input_dict.get('property_type', ''),
            int(pred_result['predicted_price']), int(pred_result['price_per_sqft']),
            int(pred_result['lower_bound']), int(pred_result['upper_bound']),
            pred_result.get('model_used', 'best_model')
        )
    )
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id

def get_user_predictions(user_id, limit=20):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(
        f"SELECT * FROM predictions WHERE user_id = {ph} ORDER BY created_at DESC LIMIT {limit}",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_predictions(limit=10):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT p.*, u.full_name as user_name FROM predictions p LEFT JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC LIMIT {limit}")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def toggle_save_property(user_id, property_id):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"SELECT id FROM saved_properties WHERE user_id = {ph} AND property_id = {ph}", (user_id, property_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute(f"DELETE FROM saved_properties WHERE user_id = {ph} AND property_id = {ph}", (user_id, property_id))
        saved = False
    else:
        cursor.execute(f"INSERT INTO saved_properties (user_id, property_id) VALUES ({ph}, {ph})", (user_id, property_id))
        saved = True
        
    conn.commit()
    conn.close()
    return saved

def get_user_saved_properties(user_id):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(
        f"""
        SELECT p.*, s.saved_at 
        FROM saved_properties s 
        JOIN properties p ON s.property_id = p.property_id 
        WHERE s.user_id = {ph} 
        ORDER BY s.saved_at DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Query & Analytics ---

def get_properties(filters=None, limit=24, offset=0):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    ph = "?" if db_type == "sqlite" else "%s"
    
    if filters:
        if filters.get('city') and filters['city'] != 'All':
            query += f" AND city = {ph}"
            params.append(filters['city'])
        if filters.get('state') and filters['state'] != 'All':
            query += f" AND state = {ph}"
            params.append(filters['state'])
        if filters.get('property_type') and filters['property_type'] != 'All':
            query += f" AND property_type = {ph}"
            params.append(filters['property_type'])
        if filters.get('bedrooms') and filters['bedrooms'] != 'All':
            query += f" AND bedrooms = {ph}"
            params.append(int(filters['bedrooms']))
        if filters.get('max_price'):
            query += f" AND price <= {ph}"
            params.append(int(filters['max_price']))
        if filters.get('min_area'):
            query += f" AND area_sqft >= {ph}"
            params.append(int(filters['min_area']))
        if filters.get('search'):
            s = f"%{filters['search']}%"
            query += f" AND (area_name LIKE {ph} OR city LIKE {ph} OR property_id LIKE {ph})"
            params.extend([s, s, s])
            
    # Sorting
    sort_by = filters.get('sort_by', 'newest') if filters else 'newest'
    if sort_by == 'price_low':
        query += " ORDER BY price ASC"
    elif sort_by == 'price_high':
        query += " ORDER BY price DESC"
    elif sort_by == 'area_high':
        query += " ORDER BY area_sqft DESC"
    else:
        query += " ORDER BY id DESC"
        
    query += f" LIMIT {limit} OFFSET {offset}"
    
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_property_by_id(property_id):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"SELECT * FROM properties WHERE property_id = {ph}", (property_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def get_locations_intelligence():
    conn, db_type = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locations ORDER BY city, area_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_distinct_locations():
    conn, db_type = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT state, city, area_name, pincode FROM locations ORDER BY state, city, area_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_admin_dashboard_stats():
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as c FROM users")
    total_users = (cursor.fetchone() or {})['c'] if db_type == "mysql" else cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as c FROM properties")
    total_properties = (cursor.fetchone() or {})['c'] if db_type == "mysql" else cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as c FROM predictions")
    total_predictions = (cursor.fetchone() or {})['c'] if db_type == "mysql" else cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(price) as avg_p, MAX(price) as max_p, MIN(price) as min_p FROM properties")
    p_stats = cursor.fetchone()
    avg_price = p_stats['avg_p'] if db_type == "mysql" else p_stats[0]
    max_price = p_stats['max_p'] if db_type == "mysql" else p_stats[1]
    min_price = p_stats['min_p'] if db_type == "mysql" else p_stats[2]
    
    cursor.execute("SELECT * FROM model_versions ORDER BY r2_score DESC")
    model_versions = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    return {
        "total_users": total_users,
        "total_properties": total_properties,
        "total_predictions": total_predictions,
        "avg_price": round(avg_price or 0),
        "max_price": max_price or 0,
        "min_price": min_price or 0,
        "model_versions": model_versions
    }

def delete_property_by_id(property_id):
    conn, db_type = get_connection()
    cursor = conn.cursor()
    ph = "?" if db_type == "sqlite" else "%s"
    cursor.execute(f"DELETE FROM properties WHERE property_id = {ph}", (property_id,))
    conn.commit()
    conn.close()
    return True

if __name__ == '__main__':
    init_db()
