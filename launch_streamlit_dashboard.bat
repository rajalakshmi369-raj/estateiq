@echo off
title ESTATEIQ - Interactive AI Real Estate Dashboard
echo ===================================================================
echo     ESTATEIQ - AI Real Estate Analytics & House Price Prediction
echo                  Interactive Streamlit Cloud Dashboard
echo ===================================================================
echo.
echo Launching Interactive Dashboard on http://localhost:8501/ ...
echo.
cd /d "%~dp0"
python -m streamlit run streamlit_app.py --server.port 8501
pause
