@echo off
echo ↔️ Располагаем кнопки "Скачать" и "В избранном" в одну строку...
cd /d "E:\pravoslavie_portal"

echo 📦 Обновляем статические файлы...
python manage.py collectstatic --noinput

echo ✅ Готово! Обновите страницу книги с Ctrl+F5

echo 🎯 Что изменилось:
echo - Кнопки "Скачать" и "В избранном" теперь в одной строке
echo - Использован Bootstrap класс d-flex с gap-2
echo - Кнопки равномерно распределены с flex-fill
echo - Сохранены все эффекты и функциональность

pause