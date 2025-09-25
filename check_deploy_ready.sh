#!/bin/bash
# Проверка готовности к деплою

echo "🔍 Проверка файлов для деплоя..."
echo ""

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Функция проверки файла
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
        return 0
    else
        echo -e "${RED}❌${NC} $1 - НЕ НАЙДЕН!"
        return 1
    fi
}

# Проверяем основные файлы
echo "📁 Основные файлы:"
check_file "core/middleware/maintenance.py"
check_file "core/context_processors.py"
check_file "config/settings_base.py"
check_file "templates/includes/maintenance_indicator.html"
check_file "templates/maintenance.html"
echo ""

# Проверяем документацию
echo "📚 Документация:"
check_file "PRODUCTION_DEPLOY.md"
check_file "MAINTENANCE_MODE_READY.md"
check_file "MAINTENANCE_MODE_GUIDE.md"
check_file "MIDDLEWARE_ORDER_FIX.md"
echo ""

# Проверяем инструменты
echo "🛠️ Инструменты:"
check_file "test_maintenance_mode.py"
check_file "maintenance_control.bat"
echo ""

# Проверяем порядок middleware
echo "🔍 Проверка порядка middleware..."
python manage.py shell << 'PYTHON_CHECK'
from django.conf import settings

middleware_list = settings.MIDDLEWARE
auth_m = 'django.contrib.auth.middleware.AuthenticationMiddleware'
maint_m = 'core.middleware.maintenance.MaintenanceModeMiddleware'

if auth_m in middleware_list and maint_m in middleware_list:
    auth_idx = middleware_list.index(auth_m)
    maint_idx = middleware_list.index(maint_m)
    
    if maint_idx > auth_idx:
        print("✅ Порядок middleware правильный")
    else:
        print("❌ ОШИБКА: MaintenanceModeMiddleware стоит ДО AuthenticationMiddleware!")
        print("   Исправьте в config/settings_base.py")
else:
    print("❌ Один из middleware отсутствует")
PYTHON_CHECK
echo ""

# Проверяем Git статус
echo "📊 Git статус:"
if git diff --quiet; then
    echo -e "${GREEN}✅${NC} Нет незакоммиченных изменений"
else
    echo -e "${YELLOW}⚠️${NC} Есть незакоммиченные изменения:"
    git status --short
fi
echo ""

# Итоговая информация
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📝 Следующие шаги:${NC}"
echo ""
echo "1. Локально:"
echo "   git add ."
echo "   git commit -m \"feat: режим обслуживания с доступом для администраторов\""
echo "   git push origin main"
echo ""
echo "2. На сервере:"
echo "   ssh root@46.62.167.17"
echo "   cd /var/www/pravoslavie_portal"
echo "   source venv/bin/activate"
echo "   ./deploy.sh"
echo ""
echo "3. Проверка:"
echo "   https://dobrist.com/admin/core/sitesettings/1/change/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
