@echo off
echo ======================================
echo 🔍 ДИАГНОСТИКА БАЗЫ ДАННЫХ
echo ======================================
echo.

cd /d E:\pravoslavie_portal

echo Проверяем миграции и создаем теги...
python check_database.py

echo.
echo ✅ Готово! Проверьте: http://127.0.0.1:8000/tag/doch/
echo.
pause
