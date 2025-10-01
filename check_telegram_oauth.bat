@echo off
chcp 65001 >nul
echo.
echo ================================================
echo Проверка настроек Telegram OAuth
echo ================================================
echo.

REM Активация виртуального окружения
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ВНИМАНИЕ: Виртуальное окружение не найдено
)

REM Запуск скрипта проверки
python check_telegram_oauth.py

echo.
echo ================================================
echo Проверка завершена
echo ================================================
echo.
pause
