@echo off
echo ===== ПРОВЕРКА ТЕСТОВОГО ПОЛЬЗОВАТЕЛЯ =====
echo.

echo 👤 Проверяем существующих пользователей...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
users = User.objects.all();
print(f'📊 Всего пользователей: {users.count()}');
print('📋 Список пользователей:');
for user in users:
    print(f'   👤 {user.username} | {user.email} | Активен: {user.is_active}');
    
# Проверяем конкретно testuser
try:
    test_user = User.objects.get(username='testuser');
    print(f'✅ Тестовый пользователь найден:');
    print(f'   Username: {test_user.username}');
    print(f'   Email: {test_user.email}');
    print(f'   Активен: {test_user.is_active}');
    print(f'   ID: {test_user.id}');
except User.DoesNotExist:
    print('❌ Тестовый пользователь не найден!');
    print('🔧 Создаем нового...');
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123',
        first_name='Тестовый',
        last_name='Пользователь'
    );
    print(f'✅ Создан: {user.username} ({user.email})');
"

echo.
echo 🚀 ДАННЫЕ ДЛЯ ВХОДА:
echo    Email: testuser@example.com
echo    Username: testuser  
echo    Пароль: password123
echo.
echo 💡 Попробуйте войти по EMAIL: testuser@example.com
echo.
pause
