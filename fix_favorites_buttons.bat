@echo off
echo 🔄 Применяем исправления для страницы избранного...
cd /d "E:\pravoslavie_portal"

echo 📦 Обновляем статические файлы...
python manage.py collectstatic --noinput

echo ✅ Готово! Обновите страницу избранного с Ctrl+F5
echo 📱 Кнопки теперь шире и текст помещается полностью
pause