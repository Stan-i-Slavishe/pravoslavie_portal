@echo off
echo 🖼️ Делаем обложки книг кликабельными...
cd /d "E:\pravoslavie_portal"

echo 📦 Обновляем статические файлы...
python manage.py collectstatic --noinput

echo ✅ Готово! Обновите страницу избранного с Ctrl+F5

echo 🎯 Что изменилось:
echo - Обложки книг теперь кликабельны
echo - Клик по обложке ведет на страницу книги
echo - Добавлен эффект наведения
echo - Улучшена интерактивность

pause