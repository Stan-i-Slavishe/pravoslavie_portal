@echo off
cd /d "%~dp0"
echo.
echo =========================================
echo    Быстрое исправление Google OAuth
echo =========================================
echo.

python quick_fix_google_oauth.py

echo.
echo =========================================
echo.
echo 🚀 Готово! Теперь попробуйте войти через Google
echo 📝 Для настройки реальных ключей перейдите в админку:
echo    http://127.0.0.1:8000/admin/socialaccount/socialapp/
echo.
pause
