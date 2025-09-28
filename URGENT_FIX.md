# СРОЧНОЕ РЕШЕНИЕ: Не пускает администратора

## 🚨 ПРОБЛЕМА
Страница обслуживания показывается даже администратору.

## ✅ БЫСТРОЕ РЕШЕНИЕ (3 команды)

### На сервере выполните:

```bash
# 1. Подключитесь
ssh root@46.62.167.17

# 2. Перейдите в проект
cd /var/www/pravoslavie_portal && source venv/bin/activate

# 3. Выключите режим обслуживания
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Режим ВЫКЛЮЧЕН')"
```

**Обновите страницу** - сайт должен работать! ✅

---

## 🔍 ДИАГНОСТИКА

### Проверьте статус:
```bash
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); print('Режим:', '🔴 ВКЛЮЧЕН' if s.maintenance_mode else '🟢 ВЫКЛЮЧЕН')"
```

### Проверьте своего пользователя:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.filter(is_superuser=True).first(); print(f'Админ: {user.username if user else \"НЕТ\"}') if user else print('❌ Нет администраторов')"
```

---

## 🛠️ АЛЬТЕРНАТИВНЫЕ РЕШЕНИЯ

### Вариант 1: Войдите через админку
```
https://dobrist.com/admin/login/
```
Эта страница доступна ВСЕГДА, даже в режиме обслуживания!

### Вариант 2: Создайте нового администратора
```bash
python manage.py createsuperuser
```

### Вариант 3: Проверьте порядок middleware
```bash
python manage.py shell << 'PYTHON'
from django.conf import settings
ml = settings.MIDDLEWARE
auth_idx = ml.index('django.contrib.auth.middleware.AuthenticationMiddleware') if 'django.contrib.auth.middleware.AuthenticationMiddleware' in ml else -1
maint_idx = ml.index('core.middleware.maintenance.MaintenanceModeMiddleware') if 'core.middleware.maintenance.MaintenanceModeMiddleware' in ml else -1
print(f"Auth: {auth_idx}, Maint: {maint_idx}")
print("✅ OK" if maint_idx > auth_idx and auth_idx != -1 else "❌ ОШИБКА")
PYTHON
```

---

## 📋 ЧТО ДЕЛАТЬ ДАЛЬШЕ

1. **Выключите режим обслуживания** (команда выше)
2. **Войдите в админку**: https://dobrist.com/admin/
3. **Проверьте настройки**: https://dobrist.com/admin/core/sitesettings/1/change/
4. **Если нужно - включите режим снова** (через админку)

---

## 🔗 ПОЛЕЗНЫЕ ССЫЛКИ

- Админка: https://dobrist.com/admin/
- Вход: https://dobrist.com/admin/login/
- Настройки режима: https://dobrist.com/admin/core/sitesettings/1/change/

---

## 📞 КОМАНДЫ ДЛЯ КОПИРОВАНИЯ

```bash
# Подключение к серверу
ssh root@46.62.167.17

# Переход в проект
cd /var/www/pravoslavie_portal
source venv/bin/activate

# Выключить режим
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Выключен')"

# Проверить статус
python manage.py shell -c "from core.models import SiteSettings; print('🔴 ВКЛ' if SiteSettings.get_settings().maintenance_mode else '🟢 ВЫКЛ')"

# Посмотреть логи
sudo journalctl -u gunicorn -n 50
```
