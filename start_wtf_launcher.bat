@echo off
title WTF Modpack Launcher
echo ========================================
echo    WTF Modpack Launcher
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing/updating dependencies...
pip install -r requirements_wtf.txt --quiet

if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
    echo The launcher may still work, continuing...
    echo.
)

echo Starting WTF Modpack Launcher...
echo.
python wtf_launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Launcher failed to start
    echo Check the error messages above
    pause
)
