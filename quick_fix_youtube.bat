@echo off
echo =======================================
echo БЫСТРОЕ ИСПРАВЛЕНИЕ YOUTUBE ID
echo =======================================

cd /d E:\pravoslavie_portal

call .venv\Scripts\activate.bat

echo.
echo Исправляем YouTube ID для рассказа...
python fix_youtube_id.py

echo.
echo Запускаем сервер...
python manage.py runserver

pause
