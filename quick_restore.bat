@echo off
echo 🔄 БЫСТРОЕ ВОССТАНОВЛЕНИЕ ВСЕХ ДАННЫХ
echo ====================================

echo 📦 Загружаем полный дамп данных...
python manage.py loaddata "backups\django_backup_2025-09-01_21-36-16\full_data.json"

echo.
echo ✅ ГОТОВО! Все данные восстановлены одной командой.
echo.
echo 🚀 Запустите сервер:
echo python manage.py runserver

pause
