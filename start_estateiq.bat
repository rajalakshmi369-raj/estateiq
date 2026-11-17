@echo off
title ESTATEIQ - AI Real Estate Analytics & House Price Prediction
echo ===================================================================
echo     ESTATEIQ - AI-Powered Real Estate Analytics & House Price
echo                  Prediction System for Indian Cities
echo ===================================================================
echo.
echo Starting Flask Web Application on http://127.0.0.1:5000 ...
echo.
cd /d "%~dp0"
python app.py
pause
