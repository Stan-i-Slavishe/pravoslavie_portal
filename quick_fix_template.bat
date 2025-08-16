@echo off
echo ===== Быстрое исправление шаблона =====
echo Перезапускаем сервер...

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запускаем сервер...
python manage.py runserver

pause
