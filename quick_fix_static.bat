@echo off
echo 🛠️ Быстрое исправление кнопки покупки...
cd /d "E:\pravoslavie_portal"

echo 🗑️ Очистка staticfiles...
if exist "staticfiles" rmdir /s /q "staticfiles"

echo 🔄 Сборка статических файлов...
python manage.py collectstatic --noinput --clear

echo ✅ Готово! Перезапустите сервер и обновите страницу с Ctrl+F5
pause