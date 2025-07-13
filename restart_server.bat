@echo off
echo 🚀 Перезапуск Django сервера с очисткой кеша...
echo.

REM Останавливаем существующие процессы Django (если запущены)
echo ⏹️ Останавливаем существующие процессы Django...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Очищаем кеш
echo 🧹 Очищаем кеш...
python clear_cache_and_restart.py

REM Собираем статические файлы
echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

REM Применяем миграции (если есть)
echo 🗄️ Применяем миграции...
python manage.py migrate

echo.
echo ✅ Готово! Запускаем сервер...
echo 🌐 Сервер будет доступен по адресу: http://127.0.0.1:8000/
echo.
echo 📱 Для тестирования мобильного виджета:
echo    1. Откройте браузер
echo    2. Нажмите F12 (инструменты разработчика)
echo    3. Включите мобильный режим (иконка телефона)
echo    4. Выберите устройство (например, iPhone SE)
echo    5. Перейдите на страницу рассказа
echo.

REM Запускаем сервер
python manage.py runserver 127.0.0.1:8000

pause
