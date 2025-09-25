"""
Скрипт для тестирования режима обслуживания
Запуск: python test_maintenance_mode.py
"""

import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import SiteSettings
from django.conf import settings

User = get_user_model()

def test_maintenance_mode():
    print("🧪 Тестирование режима обслуживания\n")
    print("=" * 60)
    
    # 1. Проверка модели SiteSettings
    print("\n1️⃣ Проверка модели SiteSettings:")
    try:
        site_settings = SiteSettings.get_settings()
        print(f"   ✅ Модель существует")
        print(f"   📝 Режим обслуживания: {'🔴 ВКЛЮЧЕН' if site_settings.maintenance_mode else '🟢 ВЫКЛЮЧЕН'}")
        print(f"   💬 Сообщение: {site_settings.maintenance_message or 'Не установлено'}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return
    
    # 2. Проверка middleware
    print("\n2️⃣ Проверка Middleware:")
    middleware_name = 'core.middleware.maintenance.MaintenanceModeMiddleware'
    if middleware_name in settings.MIDDLEWARE:
        print(f"   ✅ Middleware подключен")
        middleware_index = settings.MIDDLEWARE.index(middleware_name)
        print(f"   📍 Позиция: {middleware_index + 1} из {len(settings.MIDDLEWARE)}")
    else:
        print(f"   ❌ Middleware НЕ подключен!")
        print(f"   💡 Добавьте в MIDDLEWARE: '{middleware_name}'")
    
    # 3. Проверка context processor
    print("\n3️⃣ Проверка Context Processor:")
    context_processor = 'core.context_processors.maintenance_context'
    templates_config = settings.TEMPLATES[0]
    context_processors = templates_config['OPTIONS']['context_processors']
    
    if context_processor in context_processors:
        print(f"   ✅ Context processor подключен")
    else:
        print(f"   ❌ Context processor НЕ подключен!")
        print(f"   💡 Добавьте: '{context_processor}'")
    
    # 4. Проверка администраторов
    print("\n4️⃣ Проверка администраторов:")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(is_staff=True, is_superuser=False)
    
    print(f"   👑 Суперпользователей: {superusers.count()}")
    for user in superusers:
        print(f"      - {user.username} ({user.email})")
    
    print(f"   👤 Администраторов: {staff_users.count()}")
    for user in staff_users:
        print(f"      - {user.username} ({user.email})")
    
    if not superusers.exists() and not staff_users.exists():
        print(f"   ⚠️ Нет администраторов! Создайте хотя бы одного.")
    
    # 5. Проверка шаблонов
    print("\n5️⃣ Проверка шаблонов:")
    templates_dir = settings.BASE_DIR / 'templates'
    
    maintenance_template = templates_dir / 'maintenance.html'
    indicator_template = templates_dir / 'includes' / 'maintenance_indicator.html'
    
    if maintenance_template.exists():
        print(f"   ✅ maintenance.html существует")
    else:
        print(f"   ❌ maintenance.html НЕ найден!")
    
    if indicator_template.exists():
        print(f"   ✅ maintenance_indicator.html существует")
    else:
        print(f"   ❌ maintenance_indicator.html НЕ найден!")
    
    # 6. Итоговый статус
    print("\n" + "=" * 60)
    print("\n📊 ИТОГОВЫЙ СТАТУС:\n")
    
    if site_settings.maintenance_mode:
        print("🔴 РЕЖИМ ОБСЛУЖИВАНИЯ АКТИВЕН")
        print("\n👨‍💼 Кто имеет доступ:")
        print("   ✅ Суперпользователи (is_superuser=True)")
        print("   ✅ Администраторы (is_staff=True)")
        print("   ✅ Страницы входа (/accounts/login/, /admin/)")
        print("\n🚫 Кто НЕ имеет доступа:")
        print("   ❌ Обычные пользователи")
        print("   ❌ Неавторизованные посетители")
    else:
        print("🟢 САЙТ РАБОТАЕТ В ОБЫЧНОМ РЕЖИМЕ")
        print("   Все пользователи имеют доступ")
    
    print("\n" + "=" * 60)
    print("\n💡 Полезные ссылки:")
    print("   🔧 Настройки: http://localhost:8000/admin/core/sitesettings/1/change/")
    print("   👑 Админка: http://localhost:8000/admin/")
    print("   🏠 Главная: http://localhost:8000/")
    print("\n" + "=" * 60)

def toggle_maintenance_mode():
    """Быстрое переключение режима обслуживания"""
    site_settings = SiteSettings.get_settings()
    
    if site_settings.maintenance_mode:
        site_settings.maintenance_mode = False
        site_settings.save()
        print("✅ Режим обслуживания ВЫКЛЮЧЕН")
    else:
        site_settings.maintenance_mode = True
        site_settings.maintenance_message = "Мы проводим плановые работы. Сайт будет доступен в ближайшее время."
        site_settings.save()
        print("🔴 Режим обслуживания ВКЛЮЧЕН")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'toggle':
        toggle_maintenance_mode()
    else:
        test_maintenance_mode()
        
        print("\n🔄 Для переключения режима обслуживания запустите:")
        print("   python test_maintenance_mode.py toggle")
