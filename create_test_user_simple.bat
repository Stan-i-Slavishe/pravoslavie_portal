@echo off
echo === Создание тестового пользователя ===
echo.

echo Попытка 1: Через Django management команду...
python manage.py create_test_user
if %errorlevel% equ 0 (
    echo ✅ Успешно создан через management команду!
    goto success
)

echo.
echo Попытка 2: Через исправленный Python скрипт...
python create_test_comments_fixed.py
if %errorlevel% equ 0 (
    echo ✅ Успешно создан через Python скрипт!
    goto success
)

echo.
echo Попытка 3: Через Django shell...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='testuser').delete(); user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123', first_name='Тестовый', last_name='Пользователь'); print(f"✅ Создан: {user.username} ({user.email})") | python manage.py shell
if %errorlevel% equ 0 (
    echo ✅ Успешно создан через Django shell!
    goto success
)

echo ❌ Все методы неудачны. Создайте пользователя вручную через админку.
pause
exit /b 1

:success
echo.
echo 🎉 Тестовый пользователь готов!
echo 🚀 Данные для входа:
echo     Username: testuser
echo     Email: testuser@example.com
echo     Пароль: password123
echo.
echo 🌐 Теперь можете входить в систему!
echo.
pause
