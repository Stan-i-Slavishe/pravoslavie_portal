@echo off
echo 🗑️ ПОЛНОЕ УДАЛЕНИЕ ПРАВОСЛАВНОГО КАЛЕНДАРЯ
echo ========================================
echo.
echo ⚠️  ВНИМАНИЕ! Это необратимо удалит весь календарь
echo.
set /p confirm="Вы уверены? (y/N): "
if /i not "%confirm%"=="y" (
    echo Отменено пользователем
    pause
    exit /b 0
)

echo.
echo 🚀 Начинаем полное удаление...
echo.

cd /d "E:\pravoslavie_portal"

echo 📊 Шаг 1/5: Удаление данных из базы...
python remove_orthodox_calendar.py
echo.

echo 🧹 Шаг 2/5: Очистка кода (URLs и Views)...
python clean_calendar_code.py
echo.

echo 📂 Шаг 3/5: Удаление файлов...
python remove_calendar_files.py
echo.

echo 🏗️ Шаг 4/5: Создание миграции...
python manage.py makemigrations pwa
echo.

echo 📦 Шаг 5/5: Применение миграции...
python manage.py migrate
echo.

echo ✅ УДАЛЕНИЕ ЗАВЕРШЕНО!
echo.
echo 📋 Что остается сделать ВРУЧНУЮ:
echo    1. Удалить модели календаря из pwa/models.py:
echo       - OrthodoxEvent
echo       - DailyOrthodoxInfo  
echo       - FastingPeriod
echo    2. Убрать ссылки календаря из навигационного меню
echo    3. Создать финальную миграцию: python manage.py makemigrations
echo    4. Применить: python manage.py migrate
echo.
echo 🎉 Православный календарь полностью удален из проекта!
echo.
pause
