@echo off
echo 🔄 Исправление импорта и создание миграции...
cd /d "E:\pravoslavie_portal"

echo ✅ Импорт исправлен!
echo 🔄 Создание миграции...
python manage.py makemigrations core --name add_mobile_feedback

echo 🔄 Применение миграции...
python manage.py migrate

echo.
echo ✅ Готово! Теперь можно тестировать систему
echo 📱 Откройте сайт на мобильном и удерживайте палец 2 секунды
echo 🔧 Админка: /admin/core/mobilefeedback/
echo.
pause