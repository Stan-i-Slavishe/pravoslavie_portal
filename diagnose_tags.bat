@echo off
echo ======================================
echo 🔍 ДИАГНОСТИКА СИСТЕМЫ ТЕГОВ
echo ======================================
echo.

cd /d E:\pravoslavie_portal

echo Запуск диагностики...
python diagnose_tags.py

echo.
echo Нажмите любую клавишу для закрытия...
pause > nul
