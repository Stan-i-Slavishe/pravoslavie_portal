@echo off
echo ======================================
echo Создание миграций для комментариев
echo ======================================

cd /d "E:\pravoslavie_portal"

echo Создаем миграции для stories...
python manage.py makemigrations stories

echo.
echo Применяем миграции...
python manage.py migrate

echo.
echo ======================================
echo Готово! Модели комментариев созданы
echo ======================================
pause
