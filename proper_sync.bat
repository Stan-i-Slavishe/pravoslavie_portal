@echo off
echo 🔄 ПРАВИЛЬНАЯ СИНХРОНИЗАЦИЯ С СЕРВЕРОМ
echo =====================================

echo 📁 Переходим в корень проекта...
cd /d "E:\pravoslavie_portal"

echo 🔍 Проверяем текущий статус...
git status

echo.
echo 📥 Получаем последние изменения с сервера...
git fetch origin

echo.
echo 🔄 Синхронизируемся с сервером (безопасно)...
git reset --hard origin/main

echo.
echo 🆕 Создаем новые миграции (если нужны)...
python manage.py makemigrations

echo.
echo 📊 Применяем все миграции...
python manage.py migrate

echo.
echo 📦 Загружаем данные из лучшего бэкапа...
python manage.py loaddata "backups\django_backup_2025-09-01_21-36-16\full_data.json"

echo.
echo ✅ ГОТОВО! Правильная синхронизация завершена.
echo.
echo 🚀 Запустите сервер:
echo python manage.py runserver

pause
