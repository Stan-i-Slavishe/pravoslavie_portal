@echo off
echo 🔄 ЭКСТРЕННЫЙ ОТКАТ изменений
echo.

echo ⚠️ Этот скрипт отменит все изменения от fix_browser_errors.bat
echo.
pause

echo 1. Активируем виртуальное окружение...
call .venv\Scripts\activate

echo 2. Запускаем полный откат...
python full_rollback.py

echo.
echo 3. Пересобираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo 4. Закрываем все процессы Python...
taskkill /f /im python.exe 2>nul

echo.
echo ✅ Экстренный откат завершен!
echo.
echo 🚀 Теперь запустите Django заново:
echo python manage.py runserver
echo.
echo 💻 В браузере сделайте жесткую перезагрузку:
echo Ctrl + Shift + R
echo.
pause
