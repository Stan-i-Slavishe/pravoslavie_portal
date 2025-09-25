# ✅ ЧЕК-ЛИСТ: Режим обслуживания готов к использованию

## 🎯 Проверьте перед использованием

### 1. Файлы на месте
- [x] `core/middleware/maintenance.py` - обновлен
- [x] `core/context_processors.py` - обновлен
- [x] `config/settings_base.py` - исправлен
- [x] `templates/maintenance.html` - существует
- [x] `templates/includes/maintenance_indicator.html` - обновлен
- [x] `test_maintenance_mode.py` - создан
- [x] `maintenance_control.bat` - создан

### 2. Конфигурация Django
- [ ] Middleware подключен в `MIDDLEWARE` ПОСЛЕ `AuthenticationMiddleware`
- [ ] Context processor подключен в `TEMPLATES`
- [ ] Модель `SiteSettings` создана в БД
- [ ] Есть хотя бы один администратор

### 3. Первый запуск

**Выполните команды:**

```bash
# 1. Применить миграции (если нужно)
python manage.py makemigrations
python manage.py migrate

# 2. Проверить систему
python test_maintenance_mode.py

# 3. Запустить сервер
python manage.py runserver
```

### 4. Тестирование

**Шаг 1: Включите режим**
- [ ] Откройте: http://localhost:8000/admin/core/sitesettings/1/change/
- [ ] Поставьте галочку "Режим обслуживания"
- [ ] Нажмите "Сохранить"

**Шаг 2: Проверка как администратор**
- [ ] Перейдите на главную страницу
- [ ] Видите красную полосу сверху?
- [ ] Сайт работает нормально?

**Шаг 3: Проверка как пользователь**
- [ ] Откройте режим инкогнито (Ctrl+Shift+N)
- [ ] Перейдите на сайт
- [ ] Видите страницу обслуживания?

**Шаг 4: Выключите режим**
- [ ] Вернитесь в админку
- [ ] Снимите галочку "Режим обслуживания"
- [ ] Нажмите "Сохранить"
- [ ] Проверьте - сайт доступен всем?

### 5. Инструменты работают

**Проверьте доступность:**
- [ ] `python test_maintenance_mode.py` - показывает статус
- [ ] `python test_maintenance_mode.py toggle` - переключает режим
- [ ] `maintenance_control.bat` - открывает меню (Windows)
- [ ] Админ-панель: http://localhost:8000/admin/

---

## 🚀 Быстрый старт

### Включить режим обслуживания:

**Способ 1 - Админка (рекомендуется):**
```
http://localhost:8000/admin/core/sitesettings/1/change/
→ Поставить галочку
→ Сохранить
```

**Способ 2 - Bat-файл (Windows):**
```bash
maintenance_control.bat
→ Выбрать пункт 2
```

**Способ 3 - Python:**
```bash
python test_maintenance_mode.py toggle
```

### Выключить режим обслуживания:

**Любым из способов выше** (они переключают режим)

---

## 📋 Что делать, если что-то не работает

### Проблема: Администратор видит страницу обслуживания

**Решение 1:** Проверьте права пользователя
```bash
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='ваш_логин')
print(f"is_superuser: {user.is_superuser}")
print(f"is_staff: {user.is_staff}")
```

**Решение 2:** Перезапустите сервер
```bash
python manage.py runserver
```

### Проблема: Индикатор не отображается

**Проверьте context processor:**
```python
# В settings.py должно быть:
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ...
            'core.context_processors.maintenance_context',
        ],
    },
}]
```

### Проблема: Страница обслуживания не загружается

**Проверьте шаблон:**
```bash
# Должен существовать файл:
templates/maintenance.html
```

### Проблема: Middleware не работает (ОШИБКА: 'WSGIRequest' object has no attribute 'user')

**Причина:** MaintenanceModeMiddleware стоит ДО AuthenticationMiddleware

**Проверьте порядок в settings_base.py:**
```python
# ПРАВИЛЬНО:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← СНАЧАЛА!
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'core.middleware.maintenance.MaintenanceModeMiddleware',  # ← ПОТОМ!
]
```

**Ключевое правило:** MaintenanceModeMiddleware должен быть ПОСЛЕ AuthenticationMiddleware!

---

## 💡 Полезные команды

### Проверка системы:
```bash
python test_maintenance_mode.py
```

### Переключение режима:
```bash
python test_maintenance_mode.py toggle
```

### Очистка кеша:
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

### Создание администратора:
```bash
python manage.py createsuperuser
```

---

## 🎉 Система готова!

**После прохождения чек-листа:**
- ✅ Middleware работает
- ✅ Context processor активен
- ✅ Шаблоны загружаются
- ✅ Индикатор отображается
- ✅ Администраторы имеют доступ
- ✅ Пользователи видят страницу обслуживания

**Документация:**
- 📖 `MAINTENANCE_MODE_READY.md` - Итоговая сводка
- 📚 `MAINTENANCE_MODE_GUIDE.md` - Подробное руководство
- 🎨 Визуальная инструкция - в Artifacts

**Инструменты:**
- 🛠️ `test_maintenance_mode.py` - проверка и управление
- 🪟 `maintenance_control.bat` - меню для Windows
- 🌐 Админ-панель Django - веб-интерфейс

---

**Можно использовать в продакшене!** 🚀

**Дата готовности:** 26.09.2025
