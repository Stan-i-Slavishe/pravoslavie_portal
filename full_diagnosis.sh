#!/bin/bash
# Полная диагностика проблемы с режимом обслуживания

echo "🔍 ДИАГНОСТИКА РЕЖИМА ОБСЛУЖИВАНИЯ"
echo "════════════════════════════════════════════════════════"
echo ""

cd /var/www/pravoslavie_portal
source venv/bin/activate

# 1. Статус режима
echo "1️⃣ Статус режима обслуживания:"
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); print(f'   Режим: {\"🔴 ВКЛЮЧЕН\" if s.maintenance_mode else \"🟢 ВЫКЛЮЧЕН\"}'); print(f'   Сообщение: {s.maintenance_message or \"Не установлено\"}')"
echo ""

# 2. Проверка middleware файла
echo "2️⃣ Проверка файла middleware:"
if [ -f "core/middleware/maintenance.py" ]; then
    echo "   ✅ Файл существует: core/middleware/maintenance.py"
    echo ""
    echo "   Содержимое (первые 20 строк):"
    head -20 core/middleware/maintenance.py | sed 's/^/      /'
else
    echo "   ❌ Файл НЕ НАЙДЕН: core/middleware/maintenance.py"
fi
echo ""

# 3. Порядок middleware в settings
echo "3️⃣ Порядок middleware в настройках:"
python manage.py shell << 'PYTHON'
from django.conf import settings
import os

print(f"   Используется настройка: {os.environ.get('DJANGO_SETTINGS_MODULE', 'не указано')}")
print("")

middleware_list = settings.MIDDLEWARE
auth_m = 'django.contrib.auth.middleware.AuthenticationMiddleware'
maint_m = 'core.middleware.maintenance.MaintenanceModeMiddleware'

print("   Текущий порядок middleware:")
for i, m in enumerate(middleware_list, 1):
    if auth_m in m:
        print(f"   {i}. 🔐 {m}")
    elif maint_m in m:
        print(f"   {i}. 🛠️  {m}")
    else:
        print(f"   {i}.    {m}")

print("")

if auth_m in middleware_list and maint_m in middleware_list:
    auth_idx = middleware_list.index(auth_m)
    maint_idx = middleware_list.index(maint_m)
    
    if maint_idx > auth_idx:
        print("   ✅ Порядок ПРАВИЛЬНЫЙ")
    else:
        print("   ❌ ОШИБКА: MaintenanceModeMiddleware ПЕРЕД AuthenticationMiddleware!")
else:
    if maint_m not in middleware_list:
        print("   ⚠️  MaintenanceModeMiddleware НЕ НАЙДЕН в MIDDLEWARE")
    if auth_m not in middleware_list:
        print("   ❌ AuthenticationMiddleware НЕ НАЙДЕН в MIDDLEWARE")
PYTHON
echo ""

# 4. Проверка context processor
echo "4️⃣ Context processor:"
python manage.py shell << 'PYTHON'
from django.conf import settings

context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
maint_cp = 'core.context_processors.maintenance_context'

if maint_cp in context_processors:
    print("   ✅ maintenance_context подключен")
else:
    print("   ❌ maintenance_context НЕ подключен")
PYTHON
echo ""

# 5. Проверка вашего пользователя
echo "5️⃣ Ваш пользователь (введите username):"
read -p "   Username: " username

if [ ! -z "$username" ]; then
    python manage.py shell << PYTHON
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    user = User.objects.get(username='$username')
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   is_superuser: {user.is_superuser}")
    print(f"   is_staff: {user.is_staff}")
    print(f"   is_active: {user.is_active}")
except User.DoesNotExist:
    print(f"   ❌ Пользователь '$username' не найден")
PYTHON
fi
echo ""

# 6. Логи Gunicorn (последние 20 строк)
echo "6️⃣ Последние логи Gunicorn:"
sudo journalctl -u gunicorn -n 20 --no-pager | sed 's/^/   /'
echo ""

echo "════════════════════════════════════════════════════════"
echo ""
echo "📝 РЕКОМЕНДАЦИИ:"
echo ""
echo "Если порядок middleware неправильный:"
echo "   nano config/settings_production.py"
echo "   # Переместите MaintenanceModeMiddleware ПОСЛЕ AuthenticationMiddleware"
echo "   sudo systemctl restart gunicorn nginx"
echo ""
echo "Если файл middleware старый:"
echo "   git pull origin main"
echo "   ./deploy.sh"
echo ""
echo "Если проблема с сессией:"
echo "   # Выйдите и войдите заново в админку"
echo ""
