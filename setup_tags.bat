@echo off
echo ======================================
echo 🔧 ИСПРАВЛЕНИЕ СИСТЕМЫ ТЕГОВ
echo ======================================
echo.

cd /d E:\pravoslavie_portal

echo Создаем базовые теги...
python manage.py setup_tags

echo.
echo ✅ Теги созданы! Перезапустите сервер и проверьте:
echo    http://127.0.0.1:8000/tag/doch/
echo.
echo Нажмите любую клавишу для закрытия...
pause > nul
