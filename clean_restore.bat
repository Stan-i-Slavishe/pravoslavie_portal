@echo off
echo 🔄 ПОЛНОЕ ВОССТАНОВЛЕНИЕ С ОЧИСТКОЙ БД
echo =====================================

echo ⚠️ ВНИМАНИЕ! Это удалит ВСЕ данные из БД и загрузит из бэкапа!
pause

echo 🗑️ Удаляем все данные из БД...
python manage.py flush --noinput

echo 📦 Загружаем данные из резервной копии...
python manage.py loaddata "backups\django_backup_2025-09-01_21-36-16\full_data.json"

echo.
echo ✅ ГОТОВО! База данных полностью восстановлена.
echo.
echo 🚀 Запустите сервер:
echo python manage.py runserver

pause
