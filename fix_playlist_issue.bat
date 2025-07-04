@echo off
echo ============================================
echo ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЛЕЙЛИСТАМИ
echo ============================================

cd /d "E:\pravoslavie_portal"

echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo Запускаем исправление...
python manage.py fix_playlists

echo.
echo Готово! Теперь можно перезагрузить страницу.
pause
