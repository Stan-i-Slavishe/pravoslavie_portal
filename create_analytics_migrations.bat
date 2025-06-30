@echo off
echo Создание миграций для analytics...
python manage.py makemigrations analytics
echo.
echo Применение миграций...
python manage.py migrate
echo.
echo Готово!
pause