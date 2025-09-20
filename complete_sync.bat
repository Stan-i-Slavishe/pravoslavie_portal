@echo off
echo 🔄 ПОЛНАЯ ОЧИСТКА БД + ПРАВИЛЬНАЯ СИНХРОНИЗАЦИЯ
echo ==============================================

echo ⚠️ ВНИМАНИЕ! Это полностью очистит базу данных!
pause

echo 🗑️ Полная очистка базы данных...
python manage.py flush --noinput

echo 📦 Загружаем данные из бэкапа...
python manage.py loaddata "backups\django_backup_2025-09-01_21-36-16\full_data.json"

echo.
echo ✅ ГОТОВО! База данных синхронизирована с сервером.
echo.
echo 🚀 Запустите сервер:
echo python manage.py runserver

pause
