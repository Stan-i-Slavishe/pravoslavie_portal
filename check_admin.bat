@echo off
echo ===== ПРОВЕРКА АДМИНА =====
echo.

echo 👑 Проверяем существующего админа...

python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Ищем всех суперпользователей
admins = User.objects.filter(is_superuser=True)
print(f'👑 Найдено админов: {admins.count()}')

if admins.exists():
    for admin in admins:
        print(f'✅ Админ: {admin.username}')
        print(f'   Email: {admin.email}')
        print(f'   Активен: {admin.is_active}')
        print(f'   Суперпользователь: {admin.is_superuser}')
        print('---')
else:
    print('❌ Админы не найдены!')
    print('🔧 Создаем нового админа...')
    print('Введите данные для нового админа:')
"

if %errorlevel% equ 0 (
    echo.
    echo 💡 Попробуйте войти с этими данными!
) else (
    echo.
    echo 🔧 Создаем нового админа...
    python manage.py createsuperuser
)

echo.
echo 🌐 Идите на: http://127.0.0.1:8000/accounts/login/
echo 💡 Используйте данные админа из списка выше
echo.
pause
