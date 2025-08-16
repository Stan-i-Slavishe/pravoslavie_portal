@echo off
echo ===== ТЕСТИРОВАНИЕ ШАБЛОННЫХ УСЛОВИЙ =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запуск тестирования условий шаблона...
python test_template_conditions.py

pause
