@echo off
cd /d "%~dp0"
echo.
echo =================================================================
echo                    ПЕРЕЗАПУСК DJANGO СЕРВЕРА
echo =================================================================
echo.
echo 🔄 Этот скрипт поможет правильно перезапустить сервер
echo.

echo 📋 ИНСТРУКЦИЯ:
echo.
echo 1. ⏹️  ОСТАНОВИТЕ текущий сервер:
echo    - В терминале где запущен Django нажмите Ctrl+C
echo    - Дождитесь полной остановки
echo.
echo 2. 🚀 ЗАПУСТИТЕ сервер заново:
echo    - В том же терминале выполните: python manage.py runserver
echo    - Или запустите этот батник в новом терминале
echo.

echo 💻 Хотите запустить сервер прямо сейчас? (y/N):
set /p choice=

if /i "%choice%"=="y" (
    echo.
    echo 🚀 Запуск Django сервера...
    echo.
    python manage.py runserver
) else (
    echo.
    echo ✅ Хорошо! Запустите сервер вручную командой:
    echo    python manage.py runserver
    echo.
    pause
)
