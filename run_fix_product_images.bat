@echo off
echo 🔄 Исправление изображений товаров в магазине...
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✅ Виртуальное окружение активировано
) else (
    echo ⚠️ Виртуальное окружение не найдено, используем глобальный Python
)

echo.
echo 🚀 Запускаем скрипт исправления...
python fix_product_images.py

echo.
echo ✅ Готово! Проверьте результаты выше.
echo.
pause
