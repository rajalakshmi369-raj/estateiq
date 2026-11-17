@echo off
title Push ESTATEIQ System to GitHub
set "PATH=%PATH%;C:\Users\LOKESH ELUMALAI\AppData\Local\GitHubDesktop\app-3.5.6\resources\app\git\cmd"
echo ===================================================================
echo        ESTATEIQ - AI Real Estate Analytics & House Price
echo                   Prediction System for Indian Cities
echo                     Push to GitHub Repository
echo ===================================================================
echo.
echo Target GitHub Repository:
echo https://github.com/rajalakshmi369-raj/estateiq
echo.
echo Active Branch: main
echo.
cd /d "%~dp0"
echo 1. Checking git status...
git status
echo.
echo 2. Pushing code to GitHub...
echo (If a browser window appears, click "Sign in" / "Authorize" to complete GitHub authentication)
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ===================================================================
    echo SUCCESS! Code successfully pushed to GitHub!
    echo.
    echo Accessible Repository URL:
    echo https://github.com/rajalakshmi369-raj/estateiq
    echo ===================================================================
) else (
    echo ===================================================================
    echo Note: If the repository 'estateiq' does not exist yet on GitHub:
    echo 1. Go to https://github.com/new
    echo 2. Name the repository: estateiq
    echo 3. Keep it Public and click "Create repository" (do not add README)
    echo 4. Double click this 'push_to_github.bat' script again!
    echo ===================================================================
)
echo.
pause
