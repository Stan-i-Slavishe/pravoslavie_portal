@echo off
echo ========================================
echo Тестирование ограничения названия книги
echo для десктопной версии (30 символов)
echo ========================================
echo.
echo Изменения внесены в:
echo - books/templates/books/modern_reader.html
echo.
echo Что изменилось:
echo 1. Добавлено CSS ограничение max-width для десктопа (768px+)
echo 2. Добавлена JavaScript функция ограничения до 30 символов
echo 3. Автоматическое переключение между полным и сокращенным названием
echo 4. Tooltip с полным названием при наведении на сокращенное
echo.
echo Запускаем сервер для тестирования...
echo.
cd /d E:\pravoslavie_portal
python manage.py collectstatic --noinput
python manage.py runserver 127.0.0.1:8000
pause
