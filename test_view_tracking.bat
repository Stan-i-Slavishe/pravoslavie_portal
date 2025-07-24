@echo off
echo 🧪 Тестирование системы отслеживания просмотров
echo ================================================

cd /d "%~dp0"

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ❌ Виртуальное окружение не найдено
    pause
    exit /b 1
)

echo 🚀 Запуск тестов...
python test_view_tracking.py

echo.
echo ✅ Готово! Нажмите любую клавишу для закрытия...
pause > nul
