@echo off
REM 🔧 Запуск локального сервера разработки (Windows)
REM Файл: run_local.bat

echo 🔧 Запуск локального сервера разработки...

REM Копируем локальные настройки
copy .env.local .env

REM Активируем виртуальное окружение
if exist ".venv\Scripts\activate.bat" (
    echo 📦 Активация виртуального окружения...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo 📦 Активация виртуального окружения...
    call venv\Scripts\activate.bat
)

REM Устанавливаем зависимости если нужно
if not exist "requirements_installed.flag" (
    echo 📦 Установка зависимостей...
    pip install -r requirements.txt
    echo. > requirements_installed.flag
)

REM Создаем папки
if not exist "logs" mkdir logs
if not exist "media" mkdir media  
if not exist "staticfiles" mkdir staticfiles

REM Миграции
echo 🗄️ Применение миграций...
python manage.py migrate

REM Сбор статики
echo 📁 Сбор статических файлов...
python manage.py collectstatic --noinput

REM Создание суперпользователя
echo 👤 Проверка суперпользователя...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'admin123') if not User.objects.filter(is_superuser=True).exists() else print('👤 Суперпользователь уже существует')"

echo.
echo 🎉 Локальный сервер готов к запуску!
echo.
echo 📋 Полезные команды:
echo    🌐 Запуск сервера:     python manage.py runserver
echo    👤 Админка:            http://localhost:8000/admin/
echo.
echo 🚀 Запуск сервера...
python manage.py runserver

pause
