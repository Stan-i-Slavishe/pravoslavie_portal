@echo off
echo ===============================================
echo Исправление длинных названий книг в PDF ридере
echo ===============================================
echo.
echo Изменения:
echo 1. CSS: добавлено ограничение max-width для десктопа (768px+)
echo 2. JS: функция limitTitleForDesktop() с точным обрезанием до 30 символов  
echo 3. Автоматическое переключение при изменении размера окна
echo 4. Полное название в tooltip при наведении
echo.
echo Сбор статических файлов...
cd /d E:\pravoslavie_portal
python manage.py collectstatic --noinput

echo.
echo Запуск сервера для тестирования...
python manage.py runserver 127.0.0.1:8000

pause
