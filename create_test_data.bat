@echo off
echo === Создание тестовых данных для комментариев ===
echo.

echo 📦 Создание тестового пользователя и комментариев...
python manage.py create_test_user
if %errorlevel% neq 0 (
    echo ❌ Ошибка при создании тестовых данных
    pause
    exit /b 1
)

echo.
echo ✅ Тестовые данные созданы!
echo 🚀 Теперь войдите в систему как:
echo     Логин: testuser
echo     Email: testuser@example.com
echo     Пароль: password123
echo.
echo 🌐 Откройте страницу рассказа для тестирования комментариев
echo.
pause
