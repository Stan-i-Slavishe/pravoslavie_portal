@echo off
cd /d E:\pravoslavie_portal
echo Collecting static files...
python manage.py collectstatic --noinput
echo Done!
pause
