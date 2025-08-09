@echo off
cd /d "%~dp0"
echo.
echo =================================================================
echo             ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С GOOGLE OAUTH
echo =================================================================
echo.
echo 🎯 Этот скрипт исправит ошибку: SocialApp.DoesNotExist
echo 📝 Создаст тестовое Google OAuth приложение в базе данных
echo.

echo ⏸️  Убедитесь, что Django сервер остановлен, затем нажмите любую клавишу...
pause > nul

echo.
echo 🚀 Запуск исправления...
echo.

python fix_google_oauth_complete.py

echo.
echo =================================================================
echo.
echo 🎉 Готово! Теперь:
echo    1. Запустите Django сервер: python manage.py runserver
echo    2. Попробуйте войти через Google
echo.
echo ⚠️  Для продакшена замените тестовые ключи на настоящие в админке
echo.
pause
