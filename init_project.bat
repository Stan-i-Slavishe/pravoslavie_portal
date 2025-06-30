@echo off
echo ================================
echo    ИНИЦИАЛИЗАЦИЯ ПРОЕКТА
echo ================================
echo.

echo 1️⃣ Применяем миграции...
python manage.py migrate --verbosity=1
if %errorlevel% neq 0 (
    echo ❌ Ошибка применения миграций
    pause
    exit /b 1
)

echo.
echo 2️⃣ Создаем тестового пользователя...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if User.objects.filter(username='testuser').exists():
    print('⚠️  Тестовый пользователь уже существует');
else:
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123', first_name='Тестовый', last_name='Пользователь');
    print(f'✅ Создан: {user.username} ({user.email})');
"

echo.
echo 3️⃣ Собираем статические файлы...
python manage.py collectstatic --noinput --verbosity=0

echo.
echo ✅ ПРОЕКТ ГОТОВ К РАБОТЕ!
echo.
echo 🚀 Данные для входа:
echo     Username: testuser
echo     Email: testuser@example.com  
echo     Пароль: password123
echo.
echo 💡 Запустите сервер: python manage.py runserver
echo.
pause
