# 🗑️ ПОЛНОЕ УДАЛЕНИЕ ПРАВОСЛАВНОГО КАЛЕНДАРЯ

## 🚀 Автоматическое удаление
Запустите: `REMOVE_CALENDAR_COMPLETE.bat`

Скрипт автоматически:
1. ✅ Удалит все данные календаря из базы данных
2. ✅ Очистит URLs и Views от календарных функций
3. ✅ Удалит все файлы календаря
4. ✅ Создаст и применит миграции

## ✋ РУЧНЫЕ ДЕЙСТВИЯ (обязательно!)

### 1. 📝 Очистить модели в `pwa/models.py`

**Удалить эти модели:**
```python
class FastingPeriod(models.Model):
    # ... вся модель

class OrthodoxEvent(models.Model): 
    # ... вся модель
    
class DailyOrthodoxInfo(models.Model):
    # ... вся модель
```

### 2. 🧹 Убрать из импортов в `pwa/views.py`
Найти строку:
```python
from .models import (
    PushSubscription, NotificationCategory, UserNotificationSettings,
    UserNotificationSubscription, OrthodoxEvent, DailyOrthodoxInfo  # ← УДАЛИТЬ ЭТИ
)
```

Оставить только:
```python
from .models import (
    PushSubscription, NotificationCategory, UserNotificationSettings,
    UserNotificationSubscription
)
```

### 3. 🔗 Убрать ссылки из меню

**В шаблоне навигации найти и удалить:**
```html
<!-- Убрать эти пункты меню -->
<a href="{% url 'pwa:orthodox_calendar' %}">Православный календарь</a>
<a href="{% url 'pwa:daily_orthodox_calendar' %}">Календарь на каждый день</a>
```

### 4. 🏗️ Финальные миграции
```bash
python manage.py makemigrations pwa
python manage.py migrate
```

### 5. ✅ Проверка
- Сайт открывается без ошибок
- Меню не содержит ссылок на календари  
- В админке нет моделей календаря
- База данных не содержит таблиц календаря

## 📂 Что будет удалено:

### 🗑️ Файлы:
- `templates/pwa/orthodox_calendar*.html`
- `templates/pwa/daily_orthodox_calendar*.html`
- Все скрипты `fix_july_*.py`
- Все батч-файлы календаря `.bat`
- Документация `ORTHODOX_CALENDAR_*.md`

### 🗄️ Данные БД:
- Таблица `pwa_orthodoxevent`
- Таблица `pwa_dailyorthodoxinfo`  
- Таблица `pwa_fastingperiod`
- Все записи календарных событий

### 🔗 Код:
- URL маршруты календаря
- Views функции календаря
- Импорты календарных моделей
- API endpoints календаря

## ⚡ Результат:
После выполнения всех шагов православный календарь будет **полностью удален** из проекта. 

Проект станет легче на ~50+ файлов и несколько таблиц БД.

---
**⚠️ ВНИМАНИЕ: Это необратимое действие!**  
Сделайте backup проекта перед удалением.
