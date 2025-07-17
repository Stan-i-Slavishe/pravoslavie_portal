@echo off
chcp 65001 >nul
echo 🚀 Быстрый запуск Django сервера (исправленная версия)
echo ================================================
echo.

cd /d "E:\pravoslavie_portal"

REM Останавливаем существующие процессы
echo Останавливаем существующие процессы Django...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Активируем виртуальное окружение
echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo.
echo 🔧 Применяем миграции...
python manage.py migrate --settings=config.settings_quick

echo.
echo 📊 Собираем статические файлы...
python manage.py collectstatic --noinput --clear --settings=config.settings_quick

echo.
echo ✅ Готово! Запускаем сервер...
echo.
echo 🌐 Адрес: http://127.0.0.1:8000
echo ⚠️  НЕ используйте https://
echo.
echo Для остановки: Ctrl+C
echo.

REM Запускаем сервер с исправленными настройками
python manage.py runserver 127.0.0.1:8000 --settings=config.settings_quick
