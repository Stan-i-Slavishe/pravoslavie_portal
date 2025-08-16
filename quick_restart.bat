@echo off
cd /d "E:\pravoslavie_portal"

echo Stopping current server...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak > nul

echo Starting Django server...
python manage.py runserver 127.0.0.1:8000
