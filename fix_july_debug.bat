@echo off
echo 🔧 Отладочное исправление календаря
echo ================================
cd /d "E:\pravoslavie_portal"

echo.
echo 🐛 Запуск с подробным выводом...
echo.

python fix_july_debug.py

echo.
echo 🔍 Скрипт завершен
pause
