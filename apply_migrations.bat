#!/bin/bash
echo "=== Применение миграций для books ==="
cd E:/pravoslavie_portal
python manage.py migrate books

echo "=== Проверяем статус миграций ==="
python manage.py showmigrations books

echo "=== Перезапускаем сервер ==="
echo "Нажмите Ctrl+C и снова запустите: python manage.py runserver"
echo "Затем перейдите к: http://127.0.0.1:8000/books/book/yandeks-direkt/"
pause