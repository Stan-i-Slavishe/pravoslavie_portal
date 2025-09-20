@echo off
echo 🔄 ВОССТАНОВЛЕНИЕ ДАННЫХ ПОСЛЕ СИНХРОНИЗАЦИИ
echo ============================================

echo 📥 Загружаем основные данные...
python manage.py loaddata core_data.json

echo 📚 Загружаем данные рассказов...
python manage.py loaddata stories_data.json

echo 📖 Загружаем данные книг...
python manage.py loaddata books_data.json

echo 🧚 Загружаем данные сказок...
python manage.py loaddata fairy_tales_data.json

echo 🛒 Загружаем данные магазина...
python manage.py loaddata shop_data.json

echo.
echo ✅ ГОТОВО! Данные восстановлены.
echo.
echo 🚀 Перезапустите сервер:
echo python manage.py runserver

pause
