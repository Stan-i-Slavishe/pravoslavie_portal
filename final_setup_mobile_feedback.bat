@echo off
echo 🔄 Админка исправлена! Создание миграции...
cd /d "E:\pravoslavie_portal"

echo 🔄 Создание миграции...
python manage.py makemigrations core --name add_mobile_feedback

echo 🔄 Применение миграции...
python manage.py migrate

echo.
echo ✅ Система мобильной обратной связи готова!
echo 📱 Тестируйте на мобильном устройстве (долгое нажатие 2 сек)
echo 🔧 Админка: /admin/core/mobilefeedback/
echo.
pause