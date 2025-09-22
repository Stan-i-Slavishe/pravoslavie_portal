#!/bin/bash
echo "Деплой изменений..."
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart gunicorn
systemctl restart nginx
echo "Деплой завершен"
