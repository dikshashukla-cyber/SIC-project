@echo off
title Personal Wellness Dashboard Launcher
cd /d "%~dp0"
echo ========================================================
echo   Launching Personal Wellness Dashboard (Next-Level Edition)
echo ========================================================
echo.
echo Opening browser to http://localhost:8501 ...
python -m streamlit run app.py
pause
