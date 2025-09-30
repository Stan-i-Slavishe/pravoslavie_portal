@echo off
chcp 65001 >nul
echo ====================================
echo 🔐 Проверка OAuth провайдеров
echo ====================================
echo.

python check_oauth_status.py

echo.
echo ====================================
pause
