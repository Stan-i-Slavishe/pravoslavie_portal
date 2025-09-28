# 🎯 ПРАВИЛЬНЫЙ ДЕПЛОЙ РЕЖИМА ОБСЛУЖИВАНИЯ

## 📋 План действий

### Шаг 1: Локально - Коммит и Push

```bash
# Проверьте изменения
git status

# Добавьте все файлы
git add .

# Создайте коммит
git commit -m "feat: режим обслуживания с доступом для администраторов

- Обновлен middleware (правильный порядок после AuthenticationMiddleware)
- Добавлен context processor для индикатора
- Визуальный индикатор для администраторов (красная полоса)
- Страница обслуживания для пользователей
- Исправлена ошибка AttributeError
- Полная документация и инструменты"

# Отправьте на GitHub
git push origin main
```

---

### Шаг 2: На сервере - Полный деплой с проверкой

```bash
# 1. Подключитесь к серверу
ssh root@46.62.167.17

# 2. Перейдите в проект
cd /var/www/pravoslavie_portal
source venv/bin/activate

# 3. ВАЖНО: Убедитесь, что режим ВЫКЛЮЧЕН перед деплоем
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Режим выключен')"

# 4. Выполните деплой
./deploy.sh

# 5. Проверьте порядок middleware
python manage.py shell << 'PYTHON'
from django.conf import settings

ml = settings.MIDDLEWARE
try:
    auth_idx = ml.index('django.contrib.auth.middleware.AuthenticationMiddleware')
    maint_idx = ml.index('core.middleware.maintenance.MaintenanceModeMiddleware')
    
    print(f"AuthenticationMiddleware: позиция {auth_idx + 1}")
    print(f"MaintenanceModeMiddleware: позиция {maint_idx + 1}")
    
    if maint_idx > auth_idx:
        print("\n✅ Порядок ПРАВИЛЬНЫЙ")
    else:
        print("\n❌ ОШИБКА: Неправильный порядок!")
except ValueError as e:
    print(f"❌ Middleware не найден: {e}")
PYTHON

# 6. Проверьте статус режима
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); print(f'Режим обслуживания: {\"🔴 ВКЛЮЧЕН\" if s.maintenance_mode else \"🟢 ВЫКЛЮЧЕН\"}')"
```

---

### Шаг 3: Тестирование

#### A. Проверка 1: Включите режим через админку

```
https://dobrist.com/admin/core/sitesettings/1/change/
```

**Действия:**
1. ✅ Поставьте галочку "Режим обслуживания"
2. 📝 Введите сообщение: "Проводим плановые работы. Скоро вернёмся!"
3. 💾 Нажмите "Сохранить"

#### B. Проверка 2: Как администратор

1. Откройте главную: https://dobrist.com/
2. **Ожидаемый результат:**
   - ✅ Красная полоса сверху: "РЕЖИМ ОБСЛУЖИВАНИЯ АКТИВЕН"
   - ✅ Сайт работает нормально
   - ✅ Кнопка "Настройки" в индикаторе

#### C. Проверка 3: Как обычный пользователь

1. Откройте браузер в режиме инкогнито (Ctrl+Shift+N)
2. Перейдите на https://dobrist.com/
3. **Ожидаемый результат:**
   - ✅ Страница обслуживания (градиент, иконка шестеренки)
   - ✅ Текст вашего сообщения
   - ✅ Кнопка "Вход для администраторов"

#### D. Проверка 4: Выключите режим

1. Вернитесь в админку
2. Снимите галочку "Режим обслуживания"
3. Сохраните
4. **Ожидаемый результат:**
   - ✅ Сайт доступен всем
   - ✅ Индикатор исчез

---

## 🔍 ДИАГНОСТИКА (если что-то не работает)

### Проблема 1: Вас не пускает как администратора

**Причина:** Вы не авторизованы

**Решение:**
```
https://dobrist.com/admin/login/
```
Войдите с правами администратора.

---

### Проблема 2: Индикатор не отображается

**Проверьте на сервере:**
```bash
# Проверка context processor
python manage.py shell << 'PYTHON'
from django.conf import settings

cp = settings.TEMPLATES[0]['OPTIONS']['context_processors']
maint_cp = 'core.context_processors.maintenance_context'

if maint_cp in cp:
    print("✅ Context processor подключен")
else:
    print("❌ Context processor НЕ подключен!")
    print(f"Добавьте в TEMPLATES: {maint_cp}")
PYTHON
```

**Если не подключен - добавьте в `config/settings_production.py`:**
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... остальные
                'core.context_processors.maintenance_context',
            ],
        },
    },
]
```

---

### Проблема 3: Ошибка "no attribute 'user'"

**Проверьте порядок middleware:**
```bash
nano config/settings_production.py
```

**Должно быть:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← СНАЧАЛА
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'core.middleware.maintenance.MaintenanceModeMiddleware',  # ← ПОТОМ
]
```

После исправления:
```bash
sudo systemctl restart gunicorn nginx
```

---

## 🎯 ИТОГОВЫЙ ЧЕК-ЛИСТ

### Перед деплоем:
- [ ] Все изменения сохранены локально
- [ ] `git add . && git commit && git push` выполнены
- [ ] Режим обслуживания на сервере ВЫКЛЮЧЕН

### После деплоя:
- [ ] `./deploy.sh` выполнен успешно
- [ ] Порядок middleware правильный
- [ ] Context processor подключен
- [ ] Gunicorn и Nginx перезапущены

### Тестирование:
- [ ] Режим включен через админку
- [ ] Как админ: красная полоса отображается
- [ ] Как пользователь: страница обслуживания
- [ ] Режим выключен - всё работает

---

## 🚀 КОМАНДЫ ДЛЯ КОПИРОВАНИЯ

### Локально:
```bash
git add .
git commit -m "feat: режим обслуживания с доступом для администраторов"
git push origin main
```

### На сервере:
```bash
ssh root@46.62.167.17
cd /var/www/pravoslavie_portal && source venv/bin/activate
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save()"
./deploy.sh
```

### Проверка:
```
https://dobrist.com/admin/core/sitesettings/1/change/
```

---

## 💡 ВАЖНЫЕ МОМЕНТЫ

1. **Всегда выключайте режим перед деплоем** - иначе можете заблокировать себя
2. **Проверяйте порядок middleware** - MaintenanceModeMiddleware должен быть ПОСЛЕ AuthenticationMiddleware
3. **Используйте админку для управления** - это безопаснее чем через SSH
4. **Страница `/admin/login/` доступна ВСЕГДА** - даже в режиме обслуживания

---

## 🎉 ГОТОВО!

После выполнения всех шагов у вас будет:
- ✅ Режим обслуживания с доступом для администраторов
- ✅ Визуальный индикатор (красная полоса)
- ✅ Страница обслуживания для пользователей
- ✅ Управление через админ-панель

**Начните с Шага 1!** 🚀
