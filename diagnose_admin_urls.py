import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.contrib.admin.sites import site
from stories.models import Story
from stories.admin import StoryAdmin

print("🔍 ДИАГНОСТИКА ПРОБЛЕМЫ С ПЕРЕХОДАМИ В АДМИНКЕ")
print("=" * 60)

# Проверяем базовые URL админки
try:
    admin_index = reverse('admin:index')
    print(f"✅ Главная админки: {admin_index}")
except NoReverseMatch as e:
    print(f"❌ Ошибка главной админки: {e}")

try:
    stories_list = reverse('admin:stories_story_changelist')
    print(f"✅ Список рассказов: {stories_list}")
except NoReverseMatch as e:
    print(f"❌ Ошибка списка рассказов: {e}")

# Проверяем URL для редактирования
try:
    story = Story.objects.first()
    if story:
        story_change = reverse('admin:stories_story_change', args=[story.pk])
        print(f"✅ Редактирование рассказа #{story.pk}: {story_change}")
        
        # Проверяем прямой доступ к объекту
        print(f"📝 Название рассказа: {story.title}")
        print(f"🔗 Slug: {story.slug}")
    else:
        print("⚠️ В базе данных нет рассказов для тестирования")
except Exception as e:
    print(f"❌ Ошибка URL редактирования: {e}")

# Проверяем регистрацию модели в админке
print("\n📋 ПРОВЕРКА РЕГИСТРАЦИИ В АДМИНКЕ:")
if Story in site._registry:
    print("✅ Модель Story зарегистрирована в админке")
    admin_class = site._registry[Story]
    print(f"✅ Класс админки: {admin_class.__class__.__name__}")
    
    # Проверяем основные настройки админки
    print(f"📊 list_display: {getattr(admin_class, 'list_display', 'не установлено')}")
    print(f"🔍 search_fields: {getattr(admin_class, 'search_fields', 'не установлено')}")
    print(f"📄 list_per_page: {getattr(admin_class, 'list_per_page', 'по умолчанию')}")
else:
    print("❌ Модель Story НЕ зарегистрирована в админке!")

# Проверяем настройки безопасности
print("\n🔒 НАСТРОЙКИ БЕЗОПАСНОСТИ:")
from django.conf import settings

security_settings = [
    'SECURE_SSL_REDIRECT',
    'SECURE_BROWSER_XSS_FILTER', 
    'SECURE_CONTENT_TYPE_NOSNIFF',
    'SECURE_CROSS_ORIGIN_OPENER_POLICY',
    'SECURE_REFERRER_POLICY',
    'X_FRAME_OPTIONS',
    'CSRF_COOKIE_SAMESITE',
    'SESSION_COOKIE_SAMESITE'
]

for setting in security_settings:
    value = getattr(settings, setting, 'не установлено')
    print(f"🔧 {setting}: {value}")

print("\n" + "=" * 60)
print("🎯 РЕКОМЕНДАЦИИ:")

if not Story.objects.exists():
    print("1. ⚠️ Создайте тестовый рассказ для проверки редактирования")

print("2. 🔧 Проверьте настройки безопасности в config/settings.py")
print("3. 🔄 Очистите кеш браузера (Ctrl+Shift+Del)")
print("4. 🚀 Перезапустите сервер после изменений")

print("\n💡 Если проблема сохраняется:")
print("   - Откройте консоль разработчика (F12)")
print("   - Проверьте ошибки JavaScript")
print("   - Попробуйте в режиме инкогнито")
