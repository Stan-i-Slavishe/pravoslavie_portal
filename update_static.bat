@echo off
cd /d "E:\pravoslavie_portal"
echo Сбор статических файлов...
python manage.py collectstatic --noinput --clear
echo Готово!
pause
