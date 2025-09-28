#!/bin/bash
# Диагностика режима обслуживания на продакшен сервере

echo "🔍 ДИАГНОСТИКА РЕЖИМА ОБСЛУЖИВАНИЯ"
echo "════════════════════════════════════════════════"
echo ""

# 1. Проверка статуса режима обслуживания
echo "1️⃣ Статус режима обслуживания:"
python manage.py shell << 'PYTHON'
from core.models import SiteSettings
try:
    settings = SiteSettings.get_settings()
    status = "🔴 ВКЛЮЧЕН" if settings.maintenance_mode else "🟢 ВЫКЛЮЧЕН"
    print(f"   Режим: {status}")
    print(f"   Сообщение: {settings.maintenance_message or 'Не установлено'}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
PYTHON
echo ""

# 2. Проверка администраторов
echo "2️⃣ Администраторы в базе данных:"
python manage.py shell << 'PYTHON'
from django.contrib.auth import get_user_model
User = get_user_model()

superusers = User.objects.filter(is_superuser=True)
staff = User.objects.filter(is_staff=True, is_superuser=False)

print(f"\n   👑 Суперпользователи: {superusers.count()}")
for user in superusers:
    print(f"      - {user.username} | email: {user.email} | активен: {user.is_active}")

print(f"\n   👤 Администраторы: {staff.count()}")
for user in staff:
    print(f"      - {user.username} | email: {user.email} | активен: {user.is_active}")
PYTHON
echo ""

# 3. Проверка порядка middleware
echo "3️⃣ Порядок middleware:"
python manage.py shell << 'PYTHON'
from django.conf import settings

middleware_list = settings.MIDDLEWARE
auth_m = 'django.contrib.auth.middleware.AuthenticationMiddleware'
maint_m = 'core.middleware.maintenance.MaintenanceModeMiddleware'

print("\n   Текущий порядок middleware:")
for i, m in enumerate(middleware_list, 1):
    prefix = ""
    if auth_m in m:
        prefix = "   🔐 "
    elif maint_m in m:
        prefix = "   🛠️ "
    else:
        prefix = "      "
    print(f"{prefix}{i}. {m.split('.')[-1]}")

if auth_m in middleware_list and maint_m in middleware_list:
    auth_idx = middleware_list.index(auth_m)
    maint_idx = middleware_list.index(maint_m)
    
    if maint_idx > auth_idx:
        print("\n   ✅ Порядок правильный (MaintenanceModeMiddleware после AuthenticationMiddleware)")
    else:
        print("\n   ❌ ОШИБКА: MaintenanceModeMiddleware стоит ДО AuthenticationMiddleware!")
PYTHON
echo ""

# 4. Проверка context processor
echo "4️⃣ Context processors:"
python manage.py shell << 'PYTHON'
from django.conf import settings

context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
maint_cp = 'core.context_processors.maintenance_context'

if maint_cp in context_processors:
    print("   ✅ maintenance_context подключен")
else:
    print("   ❌ maintenance_context НЕ подключен!")
    print(f"   💡 Добавьте: {maint_cp}")
PYTHON
echo ""

# 5. Проверка файлов
echo "5️⃣ Проверка файлов:"
if [ -f "core/middleware/maintenance.py" ]; then
    echo "   ✅ core/middleware/maintenance.py"
else
    echo "   ❌ core/middleware/maintenance.py - НЕ НАЙДЕН"
fi

if [ -f "templates/maintenance.html" ]; then
    echo "   ✅ templates/maintenance.html"
else
    echo "   ❌ templates/maintenance.html - НЕ НАЙДЕН"
fi

if [ -f "templates/includes/maintenance_indicator.html" ]; then
    echo "   ✅ templates/includes/maintenance_indicator.html"
else
    echo "   ❌ templates/includes/maintenance_indicator.html - НЕ НАЙДЕН"
fi
echo ""

# 6. Итоговые рекомендации
echo "════════════════════════════════════════════════"
echo ""
echo "📝 РЕКОМЕНДАЦИИ:"
echo ""
echo "Если вы НЕ авторизованы:"
echo "   1. Войдите в админку: https://dobrist.com/admin/"
echo "   2. Используйте учетные данные администратора"
echo ""
echo "Если режим включен и нужно выключить:"
echo "   python manage.py shell -c \"from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Выключен')\""
echo ""
echo "Если нужно создать администратора:"
echo "   python manage.py createsuperuser"
echo ""
echo "════════════════════════════════════════════════"
