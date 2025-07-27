#!/bin/bash

echo "=== Создание миграций для новых моделей чтения ==="
cd E:/pravoslavie_portal
python manage.py makemigrations books

echo "=== Применение миграций ==="
python manage.py migrate books

echo "=== Запуск сервера для тестирования ==="
echo "Откройте браузер и перейдите к книге:"
echo "http://127.0.0.1:8000/books/book/yandeks-direkt/"
echo "Теперь должна быть кнопка 'Читать книгу'!"
echo ""
echo "Нажмите Ctrl+C для остановки сервера"
python manage.py runserver