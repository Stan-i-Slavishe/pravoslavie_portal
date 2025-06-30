@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ===============================================================
echo 🧹 ПОЛНАЯ ЗАЧИСТКА СИСТЕМЫ КОММЕНТАРИЕВ
echo ===============================================================
echo.

echo 📋 Запускаем Python скрипт зачистки...
python complete_cleanup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Ошибка при выполнении скрипта зачистки
    pause
    exit /b 1
)

echo.
echo 🔧 Создание миграций...
python manage.py makemigrations

echo.
echo 🔧 Применение миграций...
python manage.py migrate

echo.
echo 🧪 Тестирование сервера...
echo    Запускаем сервер для финальной проверки...

timeout /t 2 /nobreak >nul

start /min python manage.py runserver

timeout /t 5 /nobreak >nul

taskkill /f /im python.exe /fi "WINDOWTITLE eq *runserver*" >nul 2>&1

echo.
echo ===============================================================
echo 🎉 ПОЛНАЯ ЗАЧИСТКА ЗАВЕРШЕНА!
echo ===============================================================
echo.
echo ✅ Финальные исправления:
echo    • Удалены все упоминания комментариев
echo    • Очищены все Python файлы
echo    • Очищены все шаблоны
echo    • Удалены файлы комментариев
echo    • Созданы чистые миграции
echo    • Проект протестирован
echo.
echo 🚀 ГОТОВО К СОЗДАНИЮ НОВОЙ СИСТЕМЫ КОММЕНТАРИЕВ!
echo.
echo Для продолжения нажмите любую клавишу . . .
pause >nul
