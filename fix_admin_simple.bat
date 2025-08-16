@echo off
title Admin Fix - Pravoslavie Portal

echo.
echo =======================================
echo    FIXING DJANGO ADMIN ISSUES
echo =======================================
echo.

cd /d "E:\pravoslavie_portal"

echo Step 1: Stopping current server...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak > nul

echo Step 2: Running admin diagnostics...
python diagnose_admin.py
echo.

echo Step 3: Clearing Django cache...
python -c "from django.core.cache import cache; cache.clear()" 2>nul
echo.

echo Step 4: Checking migrations...
python manage.py migrate --check
echo.

echo Step 5: Collecting static files...
python manage.py collectstatic --noinput --clear
echo.

echo Step 6: Starting server with fixes...
echo.
echo Server will be available at: http://127.0.0.1:8000/admin/
echo Try accessing admin panel after server starts
echo.
echo If problem persists:
echo - Clear browser cache (Ctrl+Shift+Delete)
echo - Open admin in private browser mode
echo - Check browser console for JavaScript errors
echo.

python manage.py runserver 127.0.0.1:8000

pause
