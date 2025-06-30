@echo off
echo Создание миграций для analytics (исправлено)...
python manage.py makemigrations analytics
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Ошибка при создании миграций!
    pause
    exit /b %ERRORLEVEL%
)

echo Применение миграций...
python manage.py migrate
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Ошибка при применении миграций!
    pause
    exit /b %ERRORLEVEL%
)

echo ✅ Все миграции созданы успешно!
echo.
echo Проверим админку...
python manage.py check
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Проверка пройдена успешно!
    echo.
    echo 🚀 Можете тестировать email систему:
    echo python test_email_system.py
) else (
    echo ❌ Найдены проблемы при проверке!
)

echo.
pause