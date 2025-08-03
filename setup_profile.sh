#!/bin/bash

echo "🚀 Настройка профиля пользователя..."

# Переходим в директорию проекта
cd /e/pravoslavie_portal

# Активируем виртуальное окружение
source .venv/Scripts/activate

echo "📝 Создаем миграции для модели профиля..."
python manage.py makemigrations accounts

echo "🔄 Применяем миграции..."
python manage.py migrate

echo "👤 Создаем профили для существующих пользователей..."
python manage.py shell << EOF
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Создаем профили для всех пользователей, у которых их нет
users_without_profile = User.objects.filter(profile__isnull=True)
for user in users_without_profile:
    UserProfile.objects.create(user=user)
    print(f"Создан профиль для пользователя: {user.username}")

print(f"Всего профилей создано: {users_without_profile.count()}")
EOF

echo "✅ Настройка профиля завершена!"
echo ""
echo "📋 Теперь доступны следующие страницы:"
echo "   - /profile/ - Профиль пользователя"
echo "   - /profile/edit/ - Редактирование профиля"
echo "   - /profile/password/ - Смена пароля"
echo "   - /favorites/ - Избранные книги"
echo "   - /orders/ - Мои заказы"
echo "   - /purchases/ - Мои покупки"
echo "   - /reading/ - Прогресс чтения"
echo ""
echo "🎨 Обновите навигацию для отображения ссылки на профиль!"
