@echo off
echo 🔄 Применяем исправления кнопок...
cd /d "E:\pravoslavie_portal"

echo 🗑️ Очистка staticfiles...
if exist "staticfiles" rmdir /s /q "staticfiles"

echo 📦 Сборка статических файлов...
python manage.py collectstatic --noinput --clear

echo ✅ Готово! Обновите страницу с Ctrl+F5
pause