@echo off
echo Updating static files...
python manage.py collectstatic --noinput --clear
echo Static files updated successfully!
pause
