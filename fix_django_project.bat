@echo off
echo 🩺 ДИАГНОСТИКА И ВОССТАНОВЛЕНИЕ DJANGO
echo =====================================
echo.

echo Этот скрипт поможет найти и исправить проблемы после Git отката
echo.

echo 🔸 Выберите действие:
echo.
echo 1. Быстрая диагностика (показать ошибки)
echo 2. Экстренное восстановление (исправить автоматически)
echo 3. Полная диагностика (детальная проверка)
echo 4. Выход
echo.

set /p choice="Введите номер (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🔍 Запускаем быструю диагностику...
    python quick_django_check.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🚨 Запускаем экстренное восстановление...
    call emergency_django_fix.bat
) else if "%choice%"=="3" (
    echo.
    echo 🔧 Запускаем полную диагностику...
    python django_diagnostics.py
    pause
) else if "%choice%"=="4" (
    echo Выход...
    exit /b 0
) else (
    echo.
    echo ❌ Неверный выбор. Попробуйте снова.
    pause
    goto :eof
)
