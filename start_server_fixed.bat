@echo off
chcp 65001 >nul
echo 🔧 Исправление HTTPS ошибки и запуск сервера...
echo.

cd /d "E:\pravoslavie_portal"

REM Останавливаем все процессы Python
echo Останавливаем существующие процессы Django...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Активируем виртуальное окружение
call .venv\Scripts\activate.bat

echo.
echo 🧹 Очищаем кеш Django...
python manage.py clearcache 2>nul

echo.
echo 🔧 Проверяем миграции...
python manage.py makemigrations --dry-run

echo.
echo 🗃️ Применяем миграции...
python manage.py migrate

echo.
echo 📊 Собираем статические файлы...
python manage.py collectstatic --noinput --clear

echo.
echo ⚠️  ВАЖНО: Очистите кеш браузера!
echo    Chrome: Ctrl+Shift+Delete
echo    Firefox: Ctrl+Shift+Delete  
echo    Edge: Ctrl+Shift+Delete
echo.
echo 🌐 Запускаем сервер с исправленными настройками...
echo    Адрес: http://127.0.0.1:8000
echo    НЕ ИСПОЛЬЗУЙТЕ https://
echo.

REM Запускаем с исправленными настройками
python manage.py runserver 127.0.0.1:8000 --settings=config.settings_dev_fixed
