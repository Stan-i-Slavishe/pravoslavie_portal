@echo off
echo 🔧 Перезапуск сервера после исправления кнопок категорий...
echo.

cd /d "E:\pravoslavie_portal"

echo ⏹️ Остановка текущего сервера...
taskkill /f /im python.exe 2>nul

echo 🧹 Очистка кеша...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.pyc" del /q "*.pyc"

echo 🚀 Запуск сервера...
echo.
echo 📱 Откройте: http://127.0.0.1:8000/categories/
echo.

python manage.py runserver 127.0.0.1:8000

pause
