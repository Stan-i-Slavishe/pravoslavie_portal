@echo off
cd /d "%~dp0"
echo.
echo =================================================================
echo           ОБНОВЛЕНИЕ GOOGLE OAUTH КЛЮЧЕЙ
echo =================================================================
echo.
echo 🔑 Этот скрипт обновит тестовые ключи на настоящие
echo 📋 Ключи из Google Cloud Console проекта "dobrie-istorii"
echo.

echo ⏸️  Убедитесь, что Django сервер остановлен, затем нажмите любую клавишу...
pause > nul

echo.
echo 🚀 Обновление ключей...
echo.

python update_google_oauth_keys.py

echo.
echo =================================================================
echo.
echo 🎉 Готово! Теперь:
echo    1. Запустите Django сервер: python manage.py runserver
echo    2. Попробуйте войти через Google: http://127.0.0.1:8000/accounts/google/login/
echo    3. Должен работать полноценный вход через Google!
echo.
pause
