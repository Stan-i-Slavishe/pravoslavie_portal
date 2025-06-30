@echo off
echo ===== ПРОСТОЕ СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ =====
echo.

echo 👤 Создаем тестового пользователя через одну команду...

python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Удаляем старых
User.objects.filter(username='testuser').delete()
User.objects.filter(email='testuser@example.com').delete()

# Создаем нового
user = User.objects.create_user(
    username='testuser',
    email='testuser@example.com',
    password='password123',
    first_name='Тестовый',
    last_name='Пользователь',
    is_active=True
)

print('✅ ПОЛЬЗОВАТЕЛЬ СОЗДАН!')
print(f'Username: {user.username}')
print(f'Email: {user.email}')
print(f'Активен: {user.is_active}')
print(f'ID: {user.id}')
"

echo.
echo 🎉 ГОТОВО!
echo.
echo 🔑 ДАННЫЕ ДЛЯ ВХОДА:
echo    Email: testuser@example.com
echo    Пароль: password123
echo.
echo 🌐 Теперь идите на: http://127.0.0.1:8000/accounts/login/
echo.
pause
