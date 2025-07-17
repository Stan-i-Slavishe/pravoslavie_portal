@echo off
echo 🧹 Очистка ошибок браузера и перезапуск Django
echo.

echo 1. Закрываем все процессы Django...
taskkill /f /im python.exe 2>nul

echo 2. Очищаем кеш браузера...
echo    - Откройте браузер
echo    - Нажмите Ctrl+Shift+R для жесткой перезагрузки
echo    - Или очистите кеш браузера

echo.
echo 3. Собираем статические файлы...
call .venv\Scripts\activate
python manage.py collectstatic --noinput

echo.
echo 4. Запускаем Django с очищенной консолью...
python manage.py runserver

pause
