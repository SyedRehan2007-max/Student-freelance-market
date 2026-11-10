@echo off
title Student Freelance Marketplace - Seed Sample Data
echo ===================================================
echo Populating Database with Realistic Sample Data...
echo ===================================================
echo.
cd /d "%~dp0"
if exist "freelance_marketplace\manage.py" cd freelance_marketplace
python manage.py seed_data
echo.
echo ===================================================
pause

