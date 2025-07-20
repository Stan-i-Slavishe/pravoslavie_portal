@echo off
echo 🔧 Тестируем добавление кнопки "Все плейлисты" в мобильный виджет
echo.

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput --clear

echo.
echo 🌐 Запускаем сервер для тестирования...
echo 👀 Откройте http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/ в мобильном режиме
echo.
echo 🔍 Ожидаемый результат: кнопка "Все плейлисты (1)" внизу мобильного виджета плейлистов
echo 📱 Для просмотра в мобильном режиме: F12 → Toggle Device Toolbar
echo.

python manage.py runserver