@echo off
echo 🔄 ПОЛНОЕ ПЕРЕСОЗДАНИЕ БАЗЫ ДАННЫХ
echo ==================================

echo ⚠️ ВНИМАНИЕ! Это полностью пересоздаст базу данных!
pause

echo 🗑️ Удаляем миграции...
for /d %%i in (accounts\migrations analytics\migrations books\migrations core\migrations fairy_tales\migrations pwa\migrations shop\migrations stories\migrations subscriptions\migrations) do (
    if exist "%%i" (
        echo Удаляем %%i\*.py кроме __init__.py
        for %%f in ("%%i\*.py") do (
            if not "%%~nxf"=="__init__.py" del "%%f"
        )
    )
)

echo 📊 Создаем новые миграции...
python manage.py makemigrations

echo 🔄 Применяем миграции...
python manage.py migrate

echo 📦 Загружаем данные...
python manage.py loaddata "backups\django_backup_2025-09-01_21-36-16\full_data.json"

echo.
echo ✅ ГОТОВО! База данных полностью пересоздана.
echo.
echo 🚀 Запустите сервер:
echo python manage.py runserver

pause
