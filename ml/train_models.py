"""
ESTATEIQ - Machine Learning Pipeline & Model Training
Trains 5 Regressors:
  1. Linear Regression
  2. Decision Tree Regressor
  3. Random Forest Regressor
  4. Gradient Boosting Regressor
  5. XGBoost Regressor
Evaluates using MAE, MSE, RMSE, R2 score, and MAPE.
Saves best model and preprocessing pipeline.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model._base import LinearRegression
from sklearn.tree._classes import DecisionTreeRegressor
from sklearn.ensemble._forest import RandomForestRegressor
from sklearn.ensemble._gb import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from ml.preprocessor import EstateIQPreprocessor, extract_features

def build_ml_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'indian_housing_dataset.csv')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    df = extract_features(df)
    
    # Define features
    categorical_cols = ['city', 'area_name', 'property_type', 'furnishing', 'facing']
    numeric_cols = ['area_sqft', 'bedrooms', 'bathrooms', 'balcony', 'property_age', 
                    'parking', 'floor_number', 'total_floors', 'num_amenities', 'floor_ratio']
    
    target_col = 'price'
    
    X = df[categorical_cols + numeric_cols]
    y = df[target_col]
    
    # Train / Test split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape[0]} rows, Test set: {X_test.shape[0]} rows")
    
    # Fit preprocessor
    print("Fitting preprocessor...")
    preprocessor = EstateIQPreprocessor(numeric_cols, categorical_cols)
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)
    
    # Save fitted preprocessor
    joblib.dump(preprocessor, os.path.join(models_dir, 'preprocessor.joblib'))
    print(f"Preprocessor saved. Total processed feature dimensions: {X_train_trans.shape[1]}")
    
    # Define the 5 Regressors
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(max_depth=16, min_samples_split=4, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=150, max_depth=18, min_samples_split=4, random_state=42, n_jobs=-1),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=160, learning_rate=0.08, max_depth=6, random_state=42),
        "XGBoost Regressor": xgb.XGBRegressor(n_estimators=180, learning_rate=0.07, max_depth=6, random_state=42, n_jobs=-1)
    }
    
    results = {}
    best_model_name = None
    best_r2 = -1.0
    best_estimator = None
    
    print("\n--- Training & Evaluating 5 Regression Algorithms ---")
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_trans, y_train)
        
        # Predictions
        y_train_pred = model.predict(X_train_trans)
        y_test_pred = model.predict(X_test_trans)
        
        # Evaluation metrics on Test Set
        mae = mean_absolute_error(y_test, y_test_pred)
        mse = mean_squared_error(y_test, y_test_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_test_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        mape = np.mean(np.abs((y_test - y_test_pred) / y_test)) * 100
        
        results[name] = {
            "MAE": round(float(mae), 2),
            "MSE": round(float(mse), 2),
            "RMSE": round(float(rmse), 2),
            "R2_Score": round(float(r2), 4),
            "Train_R2": round(float(train_r2), 4),
            "MAPE": round(float(mape), 2)
        }
        
        # Save individual model
        filename = f"{name.lower().replace(' ', '_')}.joblib"
        joblib.dump(model, os.path.join(models_dir, filename))
        
        print(f"  {name:28} -> R2: {r2:.4f} | RMSE: Rs. {rmse:,.0f} | MAE: Rs. {mae:,.0f} | MAPE: {mape:.2f}%")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_estimator = model

    print(f"\n==========================================")
    print(f"BEST MODEL SELECTED: {best_model_name} (R2 Score = {best_r2:.4f})")
    print(f"==========================================")
    
    # Save best model
    joblib.dump(best_estimator, os.path.join(models_dir, 'best_model.joblib'))
    
    # Extract feature importances
    feature_names = preprocessor.feature_names_out_
    top_features = []
    
    if hasattr(best_estimator, 'feature_importances_'):
        importances = best_estimator.feature_importances_
        feat_imp_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        top_features = feat_imp_df.head(25).to_dict(orient='records')
        # Clean up numpy floats in dict
        for item in top_features:
            item['importance'] = round(float(item['importance']), 5)
            
    # Save metrics and metadata to JSON
    metadata = {
        "best_model_name": best_model_name,
        "best_r2": round(best_r2, 4),
        "total_records": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "models_evaluated": results,
        "numeric_features": numeric_cols,
        "categorical_features": categorical_cols,
        "top_feature_importances": top_features
    }
    
    metrics_path = os.path.join(models_dir, 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Pipeline complete! Metrics and models successfully saved in {models_dir}")
    return results

if __name__ == '__main__':
    build_ml_pipeline()
