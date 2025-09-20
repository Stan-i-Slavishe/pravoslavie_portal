@echo off
echo 🔄 ВОССТАНОВЛЕНИЕ ИЗ РЕЗЕРВНОЙ КОПИИ
echo ===================================

cd "E:\pravoslavie_portal\backups\django_backup_2025-09-01_21-36-16"

echo 📚 Загружаем core данные...
python "..\..\manage.py" loaddata core_data.json

echo 📖 Загружаем данные рассказов...
python "..\..\manage.py" loaddata stories_data.json

echo 📗 Загружаем данные книг...
python "..\..\manage.py" loaddata books_data.json

echo 🧚 Загружаем данные сказок...
python "..\..\manage.py" loaddata fairy_tales_data.json

echo 🛒 Загружаем данные магазина...
python "..\..\manage.py" loaddata shop_data.json

echo 👤 Загружаем данные аккаунтов...
python "..\..\manage.py" loaddata accounts_data.json

echo 🔐 Загружаем данные авторизации...
python "..\..\manage.py" loaddata auth_data.json

echo 📦 Загружаем данные подписок...
python "..\..\manage.py" loaddata subscriptions_data.json

cd "..\..\"

echo.
echo ✅ ГОТОВО! Данные восстановлены из резервной копии.
echo.
echo 🚀 Перезапустите сервер:
echo python manage.py runserver

pause
