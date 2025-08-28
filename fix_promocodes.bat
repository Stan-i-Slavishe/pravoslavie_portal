@echo off
chcp 65001 > nul
echo 🚀 Исправление промокодов...
echo.

cd /d "E:\pravoslavie_portal"

python fix_promocodes_debug.py

echo.
echo ✅ Готово! Нажмите любую клавишу для выхода...
pause > nul
