# 🚀 ДЕПЛОЙ РЕЖИМА ОБСЛУЖИВАНИЯ НА ПРОДАКШН

## 📋 Быстрая инструкция

### Шаг 1: Локально - Коммит и Push

```bash
# 1. Проверьте измененные файлы
git status

# 2. Добавьте все изменения
git add .

# 3. Создайте коммит
git commit -m "feat: добавлен режим обслуживания с доступом для администраторов

- Обновлен middleware с правильным порядком (после AuthenticationMiddleware)
- Обновлен context processor для передачи переменных
- Добавлен визуальный индикатор для администраторов
- Исправлена ошибка AttributeError с request.user
- Документация и инструменты управления"

# 4. Запушьте на сервер
git push origin main
```

### Шаг 2: На сервере - Деплой

```bash
# 1. Подключитесь к серверу
ssh root@46.62.167.17
# Пароль: vRgFjmEpCVvjXeLTJn7

# 2. Перейдите в директорию проекта
cd /var/www/pravoslavie_portal

# 3. Активируйте виртуальное окружение
source venv/bin/activate

# 4. Выполните деплой
./deploy.sh
```

**Готово!** ✅

---

## 🎯 Что проверит deploy.sh

Ваш скрипт `deploy.sh` автоматически:
- ✅ Подтянет изменения из Git
- ✅ Применит миграции (если нужно)
- ✅ Соберет статические файлы
- ✅ Перезапустит Gunicorn
- ✅ Перезапустит Nginx

---

## ✅ Проверка после деплоя

### 1. Откройте админ-панель:
```
https://dobrist.com/admin/core/sitesettings/1/change/
```

### 2. Включите режим обслуживания:
- ✅ Поставьте галочку "Режим обслуживания"
- 📝 Введите сообщение (опционально)
- 💾 Нажмите "Сохранить"

### 3. Проверьте как администратор:
```
https://dobrist.com/
```
- ✅ Красная полоса сверху: "РЕЖИМ ОБСЛУЖИВАНИЯ АКТИВЕН"
- ✅ Сайт работает нормально

### 4. Проверьте как пользователь:
- Откройте режим инкогнито (Ctrl+Shift+N)
- Перейдите на https://dobrist.com/
- ✅ Видите страницу обслуживания

### 5. Выключите режим:
- Снимите галочку в админке
- Сохраните

---

## 📁 Файлы для коммита

**Основные:**
- ✅ `core/middleware/maintenance.py`
- ✅ `core/context_processors.py`
- ✅ `config/settings_base.py`
- ✅ `templates/includes/maintenance_indicator.html`
- ✅ `templates/maintenance.html` (если обновляли)

**Документация:**
- ✅ `MAINTENANCE_MODE_READY.md`
- ✅ `MAINTENANCE_MODE_GUIDE.md`
- ✅ `MAINTENANCE_CHECKLIST.md`
- ✅ `MIDDLEWARE_ORDER_FIX.md`
- ✅ `MAINTENANCE_READY_FINAL.md`

**Инструменты:**
- ✅ `test_maintenance_mode.py`
- ✅ `maintenance_control.bat`

---

## 🔧 Быстрые команды на сервере

### Проверка статуса через SSH:
```bash
# Текущий статус режима обслуживания
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); print(f'Режим: {\"🔴 ВКЛЮЧЕН\" if s.maintenance_mode else \"🟢 ВЫКЛЮЧЕН\"}')"

# Включить режим
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = True; s.maintenance_message = 'Техническое обслуживание. Скоро вернёмся!'; s.save(); print('✅ Включен')"

# Выключить режим
python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('✅ Выключен')"
```

### Просмотр логов:
```bash
# Логи Gunicorn
sudo journalctl -u gunicorn -f

# Логи Nginx
sudo tail -f /var/log/nginx/error.log
```

---

## 🚨 Возможные проблемы

### Проблема 1: Ошибка "no attribute 'user'"
**Причина:** Неправильный порядок middleware

**Решение:** Проверьте `config/settings_production.py`:
```python
MIDDLEWARE = [
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← СНАЧАЛА
    # ...
    'core.middleware.maintenance.MaintenanceModeMiddleware',  # ← ПОТОМ
]
```

### Проблема 2: Индикатор не отображается
**Причина:** Context processor не подключен

**Решение:** Проверьте в settings:
```python
'context_processors': [
    # ...
    'core.context_processors.maintenance_context',
]
```

### Проблема 3: Изменения не применяются
**Решение:**
```bash
# Очистить кеш Django
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('✅ Кеш очищен')"

# Перезапустить сервисы
sudo systemctl restart gunicorn nginx
```

---

## 📝 Чек-лист деплоя

### Локально:
- [ ] Проверил изменения: `git status`
- [ ] Добавил файлы: `git add .`
- [ ] Создал коммит: `git commit -m "..."`
- [ ] Запушил: `git push origin main`

### На сервере:
- [ ] Подключился: `ssh root@46.62.167.17`
- [ ] Перешел в проект: `cd /var/www/pravoslavie_portal`
- [ ] Активировал venv: `source venv/bin/activate`
- [ ] Выполнил деплой: `./deploy.sh`
- [ ] Проверил админку: https://dobrist.com/admin/core/sitesettings/1/change/
- [ ] Протестировал режим обслуживания
- [ ] Выключил режим

---

## 🎉 Готово!

**Процесс деплоя:**
1. **Локально:** `git add . && git commit -m "..." && git push`
2. **На сервере:** `./deploy.sh`
3. **Готово!** ✅

**Управление на продакшне:**
- 🌐 https://dobrist.com/admin/core/sitesettings/1/change/
- 📱 SSH: `ssh root@46.62.167.17`
- 🔧 Путь: `/var/www/pravoslavie_portal`
