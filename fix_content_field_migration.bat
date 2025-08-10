@echo off
cd /d "%~dp0"
echo.
echo =================================================================
echo           ДИАГНОСТИКА И ИСПРАВЛЕНИЕ ПОЛЯ CONTENT
echo =================================================================
echo.
echo 🎯 Проверим:
echo    1. Есть ли поле 'content' в базе данных
echo    2. Состояние миграций
echo    3. Создадим миграцию если нужно
echo    4. Применим миграции
echo.

echo 📋 ШАГ 1: Диагностика базы данных...
echo.
python check_database_structure.py

echo.
echo 📋 ШАГ 2: Создание миграций (если нужно)...
echo.
python manage.py makemigrations books

echo.
echo 📋 ШАГ 3: Применение миграций...
echo.
python manage.py migrate

echo.
echo 📋 ШАГ 4: Проверка после миграций...
echo.
python check_database_structure.py

echo.
echo =================================================================
echo                           ГОТОВО!
echo =================================================================
echo.
echo ✅ Что было сделано:
echo    1. Проверена структура базы данных
echo    2. Созданы необходимые миграции
echo    3. Применены миграции
echo    4. Поле 'content' должно теперь работать
echo.
echo 🚀 Что делать дальше:
echo    1. Перезапустите Django сервер: python manage.py runserver
echo    2. Откройте админку: http://127.0.0.1:8000/admin/books/book/
echo    3. Отредактируйте книгу "Великая книга"
echo    4. Заполните поле "Содержание"
echo    5. Сохраните и проверьте на сайте
echo.
pause
