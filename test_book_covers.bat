@echo off
echo 🖼️ Тестирование отображения обложек книг
echo ============================================

cd /d "%~dp0"

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ❌ Виртуальное окружение не найдено
    pause
    exit /b 1
)

echo 🚀 Запуск сервера для тестирования...
echo.
echo 📱 Откройте в браузере:
echo    http://127.0.0.1:8000/books/
echo.
echo 🔍 Проверьте:
echo    ✅ Обложки отображаются полностью
echo    ✅ Текст на обложках виден
echo    ✅ Нет обрезанных краев
echo.
echo 🛑 Для остановки нажмите Ctrl+C
echo.

python manage.py runserver 127.0.0.1:8000
