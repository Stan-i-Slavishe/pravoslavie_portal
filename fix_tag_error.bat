@echo off
echo 🔧 Исправляем конфликт моделей Tag...
echo.

cd /d "E:\pravoslavie_portal"

echo 📊 Проверяем конфликт моделей...
python fix_tag_conflict.py

echo.
echo 🚀 Теперь проверьте страницу:
echo http://127.0.0.1:8000/tags/doch/
echo.
echo 💡 Если все еще есть ошибки, выполните:
echo python manage.py makemigrations books
echo python manage.py migrate
echo.
pause
