@echo off
echo 🔥 Создание системы мобильной обратной связи
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo 🔄 Создание миграции для MobileFeedback...
python manage.py makemigrations core --name add_mobile_feedback

echo 🔄 Применение миграции...
python manage.py migrate

echo.
echo ✅ Система мобильной обратной связи готова!
echo.
echo 🗺️ Как использовать:
echo 1. Откройте сайт на мобильном устройстве
echo 2. Удерживайте палец на экране 2 секунды
echo 3. Появится форма обратной связи
echo 4. Выберите тип обращения и опишите проблему
echo.
echo 🔧 Админка: /admin/core/mobilefeedback/
echo.
echo 🚀 Запуск сервера разработки...
python manage.py runserver

pause