@echo off
echo ===== СОЗДАНИЕ АДМИНА И ТЕСТОВОГО ПОЛЬЗОВАТЕЛЯ =====
echo.

echo 🔧 Создаем суперпользователя для админки...
echo Введите данные:
python manage.py createsuperuser --username admin --email admin@example.com
echo.

echo 👤 Создаем тестового пользователя...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();

# Удаляем старого если есть
User.objects.filter(username='testuser').delete();
User.objects.filter(email='testuser@example.com').delete();

# Создаем нового
user = User.objects.create_user(
    username='testuser',
    email='testuser@example.com',
    password='password123',
    first_name='Тестовый',
    last_name='Пользователь',
    is_active=True
);
print(f'✅ Создан тестовый пользователь:');
print(f'   Username: {user.username}');
print(f'   Email: {user.email}');
print(f'   Активен: {user.is_active}');
"

echo.
echo 🎉 ГОТОВО! Теперь у вас есть:
echo.
echo 🔧 АДМИН:
echo    Username: admin
echo    Email: admin@example.com
echo    Пароль: [введенный вами]
echo    URL: http://127.0.0.1:8000/admin/
echo.
echo 👤 ТЕСТОВЫЙ ПОЛЬЗОВАТЕЛЬ:
echo    Email: testuser@example.com
echo    Username: testuser
echo    Пароль: password123
echo    URL: http://127.0.0.1:8000/accounts/login/
echo.
echo 💡 Для входа используйте EMAIL: testuser@example.com
echo.
pause
