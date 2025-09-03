@echo off
REM Fix ALLOWED_HOSTS and restart server
REM ====================================

echo.
echo Fixing ALLOWED_HOSTS issue...
echo.

REM Stop any running Django processes
taskkill /F /IM python.exe >nul 2>&1

REM Force LOCAL environment
set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8

echo Environment set to LOCAL
echo.

echo Testing connection...
python manage.py check --database default
if errorlevel 1 (
    echo Connection failed
    pause
    exit /b 1
)

echo.
echo Starting server with correct settings...
echo Server will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop
echo.

python manage.py runserver 127.0.0.1:8000

pause