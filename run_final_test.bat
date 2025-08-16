@echo off
echo =============================================
echo ФИНАЛЬНАЯ ПРОВЕРКА И ЗАПУСК СЕРВЕРА
echo =============================================

cd /d E:\pravoslavie_portal

echo.
echo ✅ Все исправления выполнены:
echo    1. Шаблон story_detail.html - убраны стили между блоками
echo    2. Schema.org генератор - добавлена поддержка youtube_embed_id  
echo    3. Модель Story - добавлен алиас youtube_embed для совместимости
echo.

echo 🧪 Проверим, что база данных готова...
call .venv\Scripts\activate.bat

echo.
echo Применяю миграции на всякий случай...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🚀 Запускаю сервер для финального тестирования...
echo.
echo ПРОТЕСТИРУЙТЕ:
echo http://127.0.0.1:8000/stories/pochti-pokojnik/
echo.
echo Если все работает - проблема решена! 🎉
echo.

python manage.py runserver
