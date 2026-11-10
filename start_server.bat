@echo off
title Student Freelance Marketplace - Server
echo ===================================================
echo Starting Student Freelance Marketplace Web Server...
echo ===================================================
echo.
cd /d "%~dp0"
if exist "freelance_marketplace\manage.py" cd freelance_marketplace
echo Open your browser and navigate to: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server anytime.
echo.
python manage.py runserver 127.0.0.1:8000
pause

