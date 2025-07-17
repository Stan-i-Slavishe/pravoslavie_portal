@echo off
chcp 65001 >nul

echo QUICK BROWSER FIX
echo =================
echo.

call .venv\Scripts\activate

echo Clearing Django sessions...
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
try:
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
    print('Sessions cleared')
except:
    pass
"

echo.
echo Creating browser reset HTML...
echo ^<!DOCTYPE html^> > reset_browser.html
echo ^<html^>^<head^>^<title^>Reset Browser^</title^>^</head^> >> reset_browser.html
echo ^<body^> >> reset_browser.html
echo ^<h1^>Browser Reset^</h1^> >> reset_browser.html
echo ^<p^>Click the link below:^</p^> >> reset_browser.html
echo ^<h2^>^<a href="http://127.0.0.1:8000/"^>HTTP Version^</a^>^</h2^> >> reset_browser.html
echo ^<p^>Direct address: http://127.0.0.1:8000/^</p^> >> reset_browser.html
echo ^</body^>^</html^> >> reset_browser.html

echo.
echo SOLUTION:
echo 1. Open reset_browser.html file (created in project folder)
echo 2. Click "HTTP Version" link
echo 3. Or manually type: http://127.0.0.1:8000/
echo.

echo Starting HTTP server...
python manage.py runserver 127.0.0.1:8000
