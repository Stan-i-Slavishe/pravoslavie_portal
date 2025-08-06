@echo off
echo 🧹 Очистка бесплатных товаров из магазина...
echo.

cd /d "%~dp0"

echo ⚡ Используем Django management команду:
python manage.py clean_free_products

echo.
echo ✅ Готово! Проверьте магазин.
pause