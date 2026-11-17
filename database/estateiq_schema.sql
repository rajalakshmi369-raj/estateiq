-- ====================================================================
-- ESTATEIQ - MySQL Database Schema
-- AI-Powered House Price Prediction & Real Estate Analytics System
-- ====================================================================

CREATE DATABASE IF NOT EXISTS estateiq_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE estateiq_db;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user', -- 'user' or 'admin'
    phone VARCHAR(20) DEFAULT NULL,
    city VARCHAR(60) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- 2. PROPERTIES TABLE
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id VARCHAR(30) NOT NULL UNIQUE,
    area_sqft INT NOT NULL,
    area_name VARCHAR(100) NOT NULL,
    city VARCHAR(60) NOT NULL,
    district VARCHAR(60) NOT NULL,
    state VARCHAR(60) NOT NULL,
    pincode INT NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    balcony INT DEFAULT 1,
    property_type VARCHAR(40) NOT NULL,
    property_age INT NOT NULL,
    furnishing VARCHAR(30) NOT NULL,
    parking INT DEFAULT 1,
    floor_number INT DEFAULT 1,
    total_floors INT DEFAULT 1,
    facing VARCHAR(30) DEFAULT 'East',
    amenities TEXT,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    price BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prop_city (city),
    INDEX idx_prop_area (area_name),
    INDEX idx_prop_price (price),
    INDEX idx_prop_bhk (bedrooms)
) ENGINE=InnoDB;

-- 3. LOCATIONS TABLE (Aggregated Locality Intelligence)
CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(60) NOT NULL,
    district VARCHAR(60) NOT NULL,
    state VARCHAR(60) NOT NULL,
    area_name VARCHAR(100) NOT NULL,
    pincode INT NOT NULL,
    avg_price_sqft INT NOT NULL,
    total_properties INT DEFAULT 0,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    tier VARCHAR(30) DEFAULT 'Standard',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_city_area (city, area_name)
) ENGINE=InnoDB;

-- 4. PREDICTIONS HISTORY TABLE
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    input_data_json TEXT NOT NULL,
    city VARCHAR(60) NOT NULL,
    area_name VARCHAR(100) NOT NULL,
    area_sqft INT NOT NULL,
    bedrooms INT NOT NULL,
    property_type VARCHAR(40) NOT NULL,
    predicted_price BIGINT NOT NULL,
    price_per_sqft INT NOT NULL,
    lower_bound BIGINT NOT NULL,
    upper_bound BIGINT NOT NULL,
    model_used VARCHAR(60) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_pred_user (user_id),
    INDEX idx_pred_created (created_at)
) ENGINE=InnoDB;

-- 5. SAVED PROPERTIES TABLE (User Shortlist)
CREATE TABLE IF NOT EXISTS saved_properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id VARCHAR(30) NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_property (user_id, property_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(property_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. MODEL VERSIONS TABLE
CREATE TABLE IF NOT EXISTS model_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(80) NOT NULL,
    algorithm VARCHAR(80) NOT NULL,
    r2_score DECIMAL(6, 4) NOT NULL,
    rmse BIGINT NOT NULL,
    mae BIGINT NOT NULL,
    mape DECIMAL(5, 2) NOT NULL,
    is_active TINYINT(1) DEFAULT 0,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Seed Default Admin User (Password: admin123 - hashed using Werkzeug sha256)
-- Default Demo User (Password: user123)
INSERT INTO users (full_name, email, password_hash, role, phone, city)
VALUES 
('System Administrator', 'admin@estateiq.in', 'scrypt:32768:8:1$x0jA$7b7e3fbe3f07b1d989f6644fceb15cbda5161099ea6ba5a4ee48ba6b90715399ecf208ce8a30e8c8949826e7a2b978d3eb685b8fae9feff14247e26ca4a1c5b4', 'admin', '+91 98765 43210', 'Bengaluru'),
('Demo User', 'user@estateiq.in', 'scrypt:32768:8:1$y1kB$8c8f4gce4g18c2e090g7755gdfc26dceb6272100fb7cb6b5ff59cb7c01826400fdg319df9b41f9d9050937f8b3c089e4fc796c9gbf0gffg25358f37db5b2d6c5', 'user', '+91 98111 22334', 'Mumbai')
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name);
