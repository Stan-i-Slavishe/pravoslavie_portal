@echo off
echo 🔄 СОЗДАНИЕ СУПERPОЛЬЗОВАТЕЛЯ И ТЕСТОВЫХ ДАННЫХ
echo ===============================================

echo 👤 Создаем суперпользователя...
echo Введите данные для админа:
python manage.py createsuperuser

echo.
echo 📊 Создаем тестовые данные...
python create_test_data.py

echo.
echo ✅ ГОТОВО! Теперь можно:
echo 1. Запустить сервер: python manage.py runserver
echo 2. Зайти в админку: http://127.0.0.1:8000/admin/
echo 3. Добавить контент через интерфейс

pause
