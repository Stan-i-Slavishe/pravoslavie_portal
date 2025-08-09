@echo off
cd /d "%~dp0"
echo.
echo =================================================================
echo           УБИРАЕМ ПРОМЕЖУТОЧНУЮ СТРАНИЦУ GOOGLE OAUTH
echo =================================================================
echo.
echo 🎯 Что делает этот скрипт:
echo    - Настраивает прямое перенаправление на Google
echo    - Убирает промежуточную страницу "Вход через Google"
echo    - Теперь сразу откроется Google для входа
echo.

echo ✅ Настройки уже добавлены в settings.py:
echo    - SOCIALACCOUNT_LOGIN_ON_GET = True
echo    - SOCIALACCOUNT_EMAIL_AUTHENTICATION = False
echo    - SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
echo.

echo 🚀 Перезапустите Django сервер для применения изменений:
echo    1. Остановите текущий сервер (Ctrl+C)
echo    2. Запустите заново: python manage.py runserver
echo    3. Перейдите на: http://127.0.0.1:8000/accounts/google/login/
echo.

echo 🎉 Теперь будет прямое перенаправление на Google!
echo.
pause
