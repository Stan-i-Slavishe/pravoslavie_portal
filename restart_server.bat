@echo off
echo Restarting Django server...
taskkill /F /IM python.exe 2>nul
timeout /t 2
python manage.py collectstatic --noinput 2>nul
start cmd /k "python manage.py runserver"
echo Server restarted!
timeout /t 3
start http://127.0.0.1:8000/stories/
