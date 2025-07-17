@echo off
echo 🌐 МАСТЕР ИСПРАВЛЕНИЯ БРАУЗЕРНЫХ ПРОБЛЕМ
echo =======================================
echo.

echo 🔹 Django запускается, но браузер показывает ошибки HTTPS/HTTP
echo 🔹 Этот мастер поможет исправить проблему пошагово
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

echo 🎯 ВЫБЕРИТЕ РЕШЕНИЕ:
echo.
echo 1. 🚨 Быстрое исправление (рекомендуется)
echo 2. 🧹 Инструкции по очистке кеша браузера
echo 3. 🔧 Подробная диагностика Django
echo 4. 🆘 Экстренное восстановление проекта
echo 5. ❌ Выход
echo.

set /p choice="Введите номер (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚨 БЫСТРОЕ ИСПРАВЛЕНИЕ
    echo ━━━━━━━━━━━━━━━━━━━━━━
    call fix_https_problem.bat
    
) else if "%choice%"=="2" (
    echo.
    echo 🧹 ИНСТРУКЦИИ ПО ОЧИСТКЕ КЕША
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    call clear_browser_cache_guide.bat
    
) else if "%choice%"=="3" (
    echo.
    echo 🔧 ПОДРОБНАЯ ДИАГНОСТИКА
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━
    if exist django_diagnostics.py (
        python django_diagnostics.py
    ) else (
        echo ❌ Файл django_diagnostics.py не найден
        echo Запустите сначала: emergency_django_fix.bat
    )
    pause
    
) else if "%choice%"=="4" (
    echo.
    echo 🆘 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if exist emergency_django_fix.bat (
        call emergency_django_fix.bat
    ) else (
        echo ❌ Файл emergency_django_fix.bat не найден
        echo.
        echo 🔧 Выполняем базовое восстановление...
        call .venv\Scripts\activate
        taskkill /f /im python.exe 2>nul
        rmdir /s /q staticfiles 2>nul
        python manage.py collectstatic --noinput
        python manage.py runserver 127.0.0.1:8000
    )
    
) else if "%choice%"=="5" (
    echo Выход...
    exit /b 0
    
) else (
    echo.
    echo ❌ Неверный выбор. Попробуйте снова.
    pause
    goto :eof
)

echo.
echo 🎉 ГОТОВО!
echo.
echo 📝 ПАМЯТКА:
echo   • Всегда используйте: http://127.0.0.1:8000/
echo   • НЕ используйте: https://127.0.0.1:8000/
echo   • При проблемах откройте: open_django.html
echo   • Или используйте режим инкогнито
echo.
pause
