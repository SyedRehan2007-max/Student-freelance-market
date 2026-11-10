@echo off
title Student Freelance Marketplace - Run Unit Tests
echo ===================================================
echo Running 17 Automated Unit Tests...
echo ===================================================
echo.
cd /d "%~dp0"
if exist "freelance_marketplace\manage.py" cd freelance_marketplace
python manage.py test
echo.
echo ===================================================
pause

