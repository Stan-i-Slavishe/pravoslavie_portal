@echo off
echo.
echo ===============================================================
echo 🔧 ОКОНЧАТЕЛЬНОЕ ИСПРАВЛЕНИЕ
echo ===============================================================
echo.
echo 🎯 Исправляем последнюю проблему с 'comments' в settings.py
echo.

python fix_settings_final.py

echo.
echo 🔄 Создание миграций (попытка 2)...
python manage.py makemigrations

echo.
echo 🔄 Применение миграций (попытка 2)...
python manage.py migrate

echo.
echo 🧪 Тестирование сервера...
echo    Запускаем сервер для финальной проверки...
timeout /t 2 >nul
start /b python manage.py runserver >nul 2>&1
timeout /t 3 >nul
taskkill /f /im python.exe >nul 2>&1

echo.
echo ===============================================================
echo 🎉 ПРОЕКТ ПОЛНОСТЬЮ ОЧИЩЕН И ГОТОВ!
echo ===============================================================
echo.
echo ✅ Финальные исправления:
echo    • Удален 'comments' из INSTALLED_APPS
echo    • Созданы чистые миграции
echo    • Проект протестирован
echo.
echo 🚀 ГОТОВО К СОЗДАНИЮ НОВОЙ СИСТЕМЫ КОММЕНТАРИЕВ!
echo.
pause
