@echo off
echo === Проверка и создание миграций ===
echo.

echo 📋 Проверяем состояние миграций...
python manage.py showmigrations
echo.

echo 🏗️ Создаем недостающие миграции...
python manage.py makemigrations
echo.

echo 📊 Применяем все миграции...
python manage.py migrate
echo.

echo 🎯 Создаем суперпользователя (если нужно)...
echo Введите данные для администратора:
python manage.py createsuperuser --username admin --email admin@example.com
echo.

echo ✅ База данных готова!
echo 🚀 Теперь создаем тестового пользователя...
echo.

echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='testuser').delete(); user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123', first_name='Тестовый', last_name='Пользователь'); print(f"✅ Создан тестовый пользователь: {user.username} ({user.email})") | python manage.py shell

echo.
echo 🎉 Все готово!
echo 📋 Данные для входа:
echo     👤 Тестовый пользователь:
echo        Username: testuser
echo        Email: testuser@example.com
echo        Пароль: password123
echo.
echo     🔧 Администратор:
echo        Username: admin
echo        Email: admin@example.com
echo        Пароль: [введенный вами]
echo.
pause
