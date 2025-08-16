@echo off
echo ================================
echo ИСПРАВЛЕНИЕ ОШИБКИ ЗАВЕРШЕНО!
echo ================================

cd /d E:\pravoslavie_portal

echo.
echo ✅ Проблема исправлена:
echo    - Удалены стили между блоками Django
echo    - Исправлена структура блоков в story_detail.html
echo.

echo 🚀 Запускаю сервер...
echo.
echo Откройте в браузере:
echo http://127.0.0.1:8000/stories/pochti-pokojnik/
echo.

call .venv\Scripts\activate.bat
python manage.py runserver
