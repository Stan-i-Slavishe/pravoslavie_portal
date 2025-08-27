@echo off
echo 🚨 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ
echo ===========================
cd /d "E:\pravoslavie_portal"

echo.
echo 🔧 Восстанавливаем удаленные PWA функции...
python emergency_fix.py

echo.
echo ✅ Готово! Попробуйте запустить сервер:
echo    python manage.py runserver
echo.
pause
