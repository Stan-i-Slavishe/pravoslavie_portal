@echo off
echo 🚀 Быстрый запуск Django проекта (оптимизированный)
echo.

REM Активируем виртуальное окружение
call .venv\Scripts\activate

REM Очищаем кеш
echo 🧹 Очистка кеша...
python -c "import django; django.setup(); from django.core.cache import cache; cache.clear()"

REM Запускаем оптимизацию
echo ⚡ Запуск оптимизации...
python optimize_performance.py

REM Запускаем сервер с легковесными настройками
echo 🌐 Запуск сервера...
python manage.py runserver --settings=config.settings_performance

pause
