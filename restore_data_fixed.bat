@echo off
echo 🔄 ВОССТАНОВЛЕНИЕ ДАННЫХ - ИСПРАВЛЕННАЯ ВЕРСИЯ
echo ===============================================

echo ⚠️ Пропускаем поврежденный core_data.json...

echo 📚 Загружаем данные рассказов...
python manage.py loaddata stories_data.json

echo 📖 Загружаем данные книг...
python manage.py loaddata books_data.json

echo 🧚 Загружаем данные сказок...
python manage.py loaddata fairy_tales_data.json

echo 🛒 Загружаем данные магазина...
python manage.py loaddata shop_data.json

echo.
echo 📦 Пробуем загрузить полный набор данных...
python manage.py loaddata full_content_data.json

echo.
echo ✅ ГОТОВО! Данные восстановлены (кроме поврежденных файлов).
echo.
echo 🚀 Перезапустите сервер:
echo python manage.py runserver

pause
