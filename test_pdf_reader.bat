@echo off
cd /d "E:\pravoslavie_portal"
echo === Тестирование PDF Reader ===
echo.
python manage.py runserver 127.0.0.1:8000
pause
