@echo off
echo 🔄 Перезапуск с очисткой кеша...
cd /d "E:\pravoslavie_portal"

echo 📁 Собираем статические файлы...
python manage.py collectstatic --noinput

echo 🔄 Перезапускаем сервер...
echo ✅ Готово! Откройте браузер и обновите страницу
pause
