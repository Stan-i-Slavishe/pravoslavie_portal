@echo off
echo ===== ДИАГНОСТИКА ПРОБЛЕМЫ С ШАБЛОНОМ =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запуск диагностики...
python diagnose_template_issue.py

pause
