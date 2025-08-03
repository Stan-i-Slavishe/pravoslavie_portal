@echo off
echo 🚀 Настройка профиля пользователя...

cd /d E:\pravoslavie_portal

echo 📝 Создаем миграции для модели профиля...
.venv\Scripts\python.exe manage.py makemigrations accounts

echo 🔄 Применяем миграции...
.venv\Scripts\python.exe manage.py migrate

echo 👤 Создаем профили для существующих пользователей...
echo from django.contrib.auth.models import User > create_profiles.py
echo from accounts.models import UserProfile >> create_profiles.py
echo. >> create_profiles.py
echo users_without_profile = User.objects.filter(profile__isnull=True) >> create_profiles.py
echo for user in users_without_profile: >> create_profiles.py
echo     UserProfile.objects.create(user=user) >> create_profiles.py
echo     print(f"Создан профиль для пользователя: {user.username}") >> create_profiles.py
echo. >> create_profiles.py
echo print(f"Всего профилей создано: {users_without_profile.count()}") >> create_profiles.py

.venv\Scripts\python.exe manage.py shell < create_profiles.py
del create_profiles.py

echo ✅ Настройка профиля завершена!
echo.
echo 📋 Теперь доступны следующие страницы:
echo    - /profile/ - Профиль пользователя
echo    - /profile/edit/ - Редактирование профиля  
echo    - /profile/password/ - Смена пароля
echo    - /favorites/ - Избранные книги
echo    - /orders/ - Мои заказы
echo    - /purchases/ - Мои покупки
echo    - /reading/ - Прогресс чтения
echo.
echo 🎨 Обновите навигацию для отображения ссылки на профиль!
pause
