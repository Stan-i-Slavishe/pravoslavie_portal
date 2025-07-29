@echo off
echo Применяем исправления CSS для мобильной читалки...
cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate
python manage.py collectstatic --noinput
echo Исправления применены! Перезапустите сервер.
pause
