@echo off
echo 🚀 Обновление православного календаря с комбинированным отображением
echo ===============================================================
cd /d "E:\pravoslavie_portal"

echo.
echo 📋 Что будет сделано:
echo   1. Добавлены сплошные седмицы (зеленые недели)
echo   2. Обновлен алгоритм определения типов дней
echo   3. Добавлено комбинированное отображение 80/20
echo   4. Исправлено отображение 29 августа (пост приоритетнее праздника)
echo.

pause

echo 🔧 Выполняем обновления...
python add_continuous_weeks_and_update_calendar.py

echo.
echo 🔄 Применяем миграции...
python manage.py makemigrations pwa
python manage.py migrate

echo.
echo 🗑️ Очищаем кеш...
python -c "from django.core.cache import cache; cache.clear(); print('Кеш очищен')"

echo.
echo ✅ Обновления завершены!
echo.
echo 📊 Итог:
echo   🔴 Красный = Праздники
echo   🟣 Фиолетовый = Посты (включая 29 августа)
echo   🟢 Зеленый = Сплошные недели
echo   🎭 Комбинированные = 80%% основное + 20%% дополнительное событие
echo.
echo 🌐 Календарь доступен по адресу:
echo   http://127.0.0.1:8000/pwa/daily-calendar/
echo.
echo 🚀 Запустить Django сервер? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo Запускаем сервер...
    python manage.py runserver
) else (
    echo Для запуска сервера выполните: python manage.py runserver
)

pause
