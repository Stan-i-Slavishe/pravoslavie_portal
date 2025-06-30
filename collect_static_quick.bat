@echo off
echo ✅ Сборка статических файлов...
python manage.py collectstatic --noinput
echo.
echo 🚀 Готово! Проверьте изменения в браузере.
echo.
pause
