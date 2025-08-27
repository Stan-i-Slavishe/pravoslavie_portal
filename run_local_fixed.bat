@echo off
REM 🔧 Быстрый запуск локального сервера (исправленная версия)
REM Файл: run_local_fixed.bat

echo 🔧 Запуск исправленной версии локального сервера...

REM Устанавливаем переменную для использования упрощенных настроек
set DJANGO_SETTINGS_MODULE=config.settings_simple

REM Активируем виртуальное окружение
if exist ".venv\Scripts\activate.bat" (
    echo 📦 Активация виртуального окружения...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo 📦 Активация виртуального окружения...
    call venv\Scripts\activate.bat
)

REM Создаем папки
if not exist "logs" mkdir logs
if not exist "media" mkdir media  
if not exist "staticfiles" mkdir staticfiles

REM Миграции
echo 🗄️ Применение миграций...
python manage.py migrate --settings=config.settings_simple

REM Сбор статики
echo 📁 Сбор статических файлов...
python manage.py collectstatic --noinput --settings=config.settings_simple

echo.
echo 🎉 Сервер готов к запуску!
echo.
echo 🚀 Запуск Django сервера...
python manage.py runserver --settings=config.settings_simple

pause
