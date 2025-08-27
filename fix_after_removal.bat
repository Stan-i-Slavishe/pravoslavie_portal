@echo off
echo 🔧 Быстрое исправление проекта
echo ============================
cd /d "E:\pravoslavie_portal"

echo.
echo 🚑 Исправляем сломанные ссылки...
python fix_after_removal.py

echo.
echo ✅ Готово! Проект исправлен
echo.
echo 🚀 Теперь можно запустить:
echo    python manage.py runserver
echo.
pause
