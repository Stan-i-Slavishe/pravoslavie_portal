@echo off
echo 🔍 ДИАГНОСТИКА ПРОБЛЕМЫ С ПЕРЕХОДАМИ В АДМИНКЕ
echo.

echo Проверяем настройки безопасности...
echo.

python manage.py shell -c "
from django.conf import settings
print('=== ТЕКУЩИЕ НАСТРОЙКИ БЕЗОПАСНОСТИ ===')
print('DEBUG:', settings.DEBUG)
print('SECURE_SSL_REDIRECT:', getattr(settings, 'SECURE_SSL_REDIRECT', 'не установлено'))
print('X_FRAME_OPTIONS:', getattr(settings, 'X_FRAME_OPTIONS', 'не установлено'))
print('CSRF_COOKIE_SECURE:', getattr(settings, 'CSRF_COOKIE_SECURE', 'не установлено'))
print('SESSION_COOKIE_SECURE:', getattr(settings, 'SESSION_COOKIE_SECURE', 'не установлено'))
print()
print('=== MIDDLEWARE ===')
for middleware in settings.MIDDLEWARE:
    print('-', middleware)
print()
print('=== ПРОВЕРКА АДМИНКИ ===')
try:
    from django.contrib.admin.sites import site
    from stories.models import Story
    from stories.admin import StoryAdmin
    print('✅ Админка Stories загружена успешно')
    print('✅ Модель Story зарегистрирована')
except Exception as e:
    print('❌ Ошибка админки:', e)
"

pause
