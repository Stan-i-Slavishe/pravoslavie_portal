а@echo off
echo "🔧 Проверка настройки аналитики..."
cd /d E:\pravoslavie_portal

echo "1. Применяем миграции аналитики..."
python manage.py migrate analytics

echo.
echo "2. Создаем суперпользователя (если нужно)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('✅ Создан admin/admin123')
else:
    print('ℹ️ Админ уже существует')
"

echo.
echo "3. Проверяем модели аналитики..."
python manage.py shell -c "
from analytics.models import PurchaseIntent, PopularContent, UserBehavior
print(f'📊 PurchaseIntent: {PurchaseIntent.objects.count()} записей')
print(f'📈 PopularContent: {PopularContent.objects.count()} записей') 
print(f'👤 UserBehavior: {UserBehavior.objects.count()} записей')
"

echo.
echo "✅ Готово! Теперь запустите:"
echo "   python manage.py runserver"
echo "   Откройте: http://127.0.0.1:8000/books/"
echo "   Кликните на книгу и на кнопку 'Купить'"
echo "   Проверьте: http://127.0.0.1:8000/analytics/dashboard/"
echo.
pause
