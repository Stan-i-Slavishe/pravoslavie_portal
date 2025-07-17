@echo off
chcp 65001 >nul
echo.
echo ================================================
echo    БЫСТРЫЙ ЗАПУСК DJANGO СЕРВЕРА
echo ================================================
echo.

cd /d "E:\pravoslavie_portal"

REM Останавливаем существующие процессы
echo [1/5] Останавливаем существующие процессы Django...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Активируем виртуальное окружение
echo [2/5] Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo [3/5] Применяем миграции...
python manage.py migrate --settings=config.settings_quick

echo [4/5] Собираем статические файлы...
python manage.py collectstatic --noinput --clear --settings=config.settings_quick

echo [5/5] Запускаем сервер...
echo.
echo ================================================
echo    СЕРВЕР ГОТОВ К РАБОТЕ
echo ================================================
echo.
echo Адрес: http://127.0.0.1:8000
echo Для остановки: Ctrl+C
echo.

REM Запускаем сервер с исправленными настройками
python manage.py runserver 127.0.0.1:8000 --settings=config.settings_quick
