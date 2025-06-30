@echo off
echo Обновление статических файлов...

rmdir /s /q staticfiles 2>nul
python manage.py collectstatic --noinput

echo.
echo Готово! Запустите: python manage.py runserver
echo Не забудьте очистить кеш браузера Ctrl+F5
pause