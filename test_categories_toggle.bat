@echo off
echo =====================================
echo 🧚 ТЕСТИРОВАНИЕ ПЕРЕКЛЮЧЕНИЯ КАТЕГОРИЙ
echo =====================================
echo.

echo 🔍 Запуск проверки категорий...
python test_category_toggle.py

echo.
echo 🌐 Для полного тестирования запустите:
echo python manage.py runserver
echo.
echo 📱 Затем откройте в браузере:
echo http://127.0.0.1:8000/fairy-tales/
echo.

pause
