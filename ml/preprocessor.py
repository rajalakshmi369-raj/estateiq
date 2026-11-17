"""
ESTATEIQ - Preprocessor Module
Defines the preprocessing class for numerical scaling and categorical encoding.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing._data import StandardScaler
from sklearn.preprocessing._encoders import OneHotEncoder

class EstateIQPreprocessor:
    """Robust preprocessing pipeline for numerical scaling and categorical encoding."""
    def __init__(self, numeric_cols, categorical_cols):
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.feature_names_out_ = []

    def fit(self, df):
        # Fit scaler
        num_data = df[self.numeric_cols].values
        self.scaler.fit(num_data)

        # Fit encoder
        cat_data = df[self.categorical_cols].astype(str).values
        self.encoder.fit(cat_data)

        # Build feature names
        cat_names = self.encoder.get_feature_names_out(self.categorical_cols)
        self.feature_names_out_ = list(self.numeric_cols) + list(cat_names)
        return self

    def transform(self, df):
        num_scaled = self.scaler.transform(df[self.numeric_cols].values)
        cat_encoded = self.encoder.transform(df[self.categorical_cols].astype(str).values)
        return np.hstack([num_scaled, cat_encoded])

    def fit_transform(self, df):
        return self.fit(df).transform(df)

def extract_features(df):
    """Derive relevant predictive features from raw dataframe."""
    df_feat = df.copy()
    
    # Calculate number of amenities
    df_feat['num_amenities'] = df_feat['amenities'].apply(
        lambda x: len(str(x).split(';')) if pd.notnull(x) and str(x).strip() != '' else 0
    )
    
    # Floor ratio (relative height)
    total_floors_safe = df_feat['total_floors'].replace(0, 1)
    df_feat['floor_ratio'] = (df_feat['floor_number'] / total_floors_safe).round(4)
    
    return df_feat
