"""
ESTATEIQ - Application Configuration
"""

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'estateiq-vit-secret-key-2026-ml-real-estate')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'indian_housing_dataset.csv')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'generated')
    
    # Session config
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
