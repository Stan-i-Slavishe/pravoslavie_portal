@echo off
echo 🔧 Перезапуск после исправления - единая кнопка "Перейти"
echo.

cd /d "E:\pravoslavie_portal"

echo ⏹️ Остановка сервера...
taskkill /f /im python.exe 2>nul

echo 🧹 Очистка кеша...
if exist "__pycache__" rmdir /s /q "__pycache__"

echo ✅ Исправления применены:
echo    - Убрана дублирующая кнопка "Видео-рассказы"  
echo    - Для всех категорий единая кнопка "Перейти"
echo    - Все кнопки ведут на правильные страницы категорий
echo.

echo 🚀 Запуск сервера...
echo 📱 Откройте: http://127.0.0.1:8000/categories/
echo.

python manage.py runserver 127.0.0.1:8000

pause
