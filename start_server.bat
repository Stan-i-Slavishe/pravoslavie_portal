@echo off
chcp 65001 >nul
echo.
echo ================================================
echo           ВЫБЕРИТЕ РЕЖИМ ЗАПУСКА
echo ================================================
echo.
echo 1. Быстрый запуск (без Allauth) - рекомендуется
echo 2. Полный запуск (с Allauth)
echo 3. Обычный запуск (основные настройки)
echo.
set /p choice="Введите номер (1-3): "

cd /d "E:\pravoslavie_portal"

REM Останавливаем существующие процессы
echo.
echo Останавливаем существующие процессы...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Активируем виртуальное окружение
call .venv\Scripts\activate.bat

echo.
if "%choice%"=="1" (
    echo Быстрый запуск выбран...
    set SETTINGS=config.settings_quick
    echo Применяем миграции...
    python manage.py migrate --settings=%SETTINGS%
) else if "%choice%"=="2" (
    echo Полный запуск выбран...
    set SETTINGS=config.settings_with_allauth
    echo Применяем миграции...
    python manage.py migrate --settings=%SETTINGS%
) else (
    echo Обычный запуск выбран...
    set SETTINGS=config.settings
    echo Применяем миграции...
    python manage.py migrate --settings=%SETTINGS%
)

echo.
echo Собираем статические файлы...
python manage.py collectstatic --noinput --clear --settings=%SETTINGS%

echo.
echo ================================================
echo           СЕРВЕР ЗАПУЩЕН
echo ================================================
echo.
echo Адрес: http://127.0.0.1:8000
echo Настройки: %SETTINGS%
echo Для остановки: Ctrl+C
echo.

python manage.py runserver 127.0.0.1:8000 --settings=%SETTINGS%
