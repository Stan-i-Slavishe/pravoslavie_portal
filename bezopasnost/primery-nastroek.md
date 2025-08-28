# 📋 Примеры настроек безопасности

## 🏢 **Для корпоративного сайта (строгие настройки)**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 20,      # Очень строго
    'requests_per_hour': 200,       # Очень строго  
    'login_attempts_per_hour': 3,   # Максимально строго
    'admin_attempts_per_hour': 2,   # Супер строго
    'api_requests_per_minute': 10,  # Ограниченно
}
```

---

## 🎪 **Для сайта событий/мероприятий (мягкие настройки)**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 120,     # Много посетителей
    'requests_per_hour': 3000,      # Высокая активность
    'login_attempts_per_hour': 20,  # Много регистраций
    'admin_attempts_per_hour': 10,  # Несколько админов
    'api_requests_per_minute': 60,  # Активное API
}
```

---

## 🛒 **Для интернет-магазина (сбалансированные настройки)**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 40,      # Средняя активность  
    'requests_per_hour': 800,       # Покупки и просмотры
    'login_attempts_per_hour': 5,   # Клиенты входят
    'admin_attempts_per_hour': 3,   # Администрация
    'api_requests_per_minute': 25,  # API заказов
}

# Дополнительно для магазина
SECURITY_EXTRA_PATTERNS = [
    r'coupon.*hack',        # Попытки взлома купонов
    r'price.*manipulation', # Манипуляции с ценами
    r'cart.*injection',     # Инъекции в корзину
]
```

---

## 🎓 **Для образовательного сайта**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 80,      # Студенты активны
    'requests_per_hour': 1500,      # Много материалов
    'login_attempts_per_hour': 15,  # Забывают пароли
    'admin_attempts_per_hour': 5,   # Преподаватели
    'api_requests_per_minute': 40,  # Онлайн тесты
}
```

---

## 🌐 **Для новостного сайта**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 100,     # Много читателей
    'requests_per_hour': 2500,      # Высокий трафик
    'login_attempts_per_hour': 10,  # Комментаторы
    'admin_attempts_per_hour': 8,   # Редакция
    'api_requests_per_minute': 50,  # RSS, API новостей
}
```

---

## 🎮 **Для игрового/развлекательного сайта**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 150,     # Активные геймеры
    'requests_per_hour': 4000,      # Много игровых запросов
    'login_attempts_per_hour': 25,  # Пробуют пароли
    'admin_attempts_per_hour': 6,   # Модераторы
    'api_requests_per_minute': 80,  # Игровое API
}
```

---

## 🧪 **Для тестирования/разработки**

### В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 200,     # Без ограничений
    'requests_per_hour': 10000,     # Тестируем много
    'login_attempts_per_hour': 50,  # Тестовые аккаунты
    'admin_attempts_per_hour': 20,  # Разработчики
    'api_requests_per_minute': 100, # API тесты
}

# Или полностью отключить защиту
MIDDLEWARE = [
    # Закомментировать security middleware
    # 'core.middleware.advanced_security.BlacklistMiddleware',
    # 'core.middleware.advanced_security.AdvancedSecurityMiddleware', 
    # 'core.middleware.advanced_security.MonitoringMiddleware',
]
```

---

## 🚨 **Экстренные настройки при атаке**

### Максимальная защита:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 5,       # Крайне строго
    'requests_per_hour': 50,        # Минимум
    'login_attempts_per_hour': 1,   # Почти заблокировано
    'admin_attempts_per_hour': 1,   # Только админы
    'api_requests_per_minute': 2,   # Критический минимум
}

# Дополнительные паттерны при атаке
SECURITY_EMERGENCY_PATTERNS = [
    r'bot',                 # Блокировать ботов
    r'crawler',             # Блокировать краулеров  
    r'scan',               # Блокировать сканеры
    r'hack',               # Блокировать хакеров
    r'exploit',            # Блокировать эксплоиты
]
```

---

## 📊 **Православный портал (текущие настройки)**

### Оптимизированные для духовного контента:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 60,          # Умеренная активность
    'requests_per_hour': 1000,          # Читают книги/рассказы
    'mobile_feedback_per_hour': 10,     # Мобильная обратная связь
    'login_attempts_per_hour': 10,      # Прихожане входят
    'admin_attempts_per_hour': 5,       # Админы портала
    'api_requests_per_minute': 30,      # Аналитика и API
}

# Специальные паттерны для религиозного сайта
SECURITY_RELIGIOUS_PATTERNS = [
    r'antichrist',         # Защита от кощунства
    r'blasphemy',          # Защита от богохульства
    r'sectarian',          # Защита от сектантства
]
```

---

## 🔧 **Как применить настройки**

### 1. Скопировать нужную конфигурацию в `config/settings.py`

### 2. Перезапустить сервер:
```bash
python manage.py runserver
```

### 3. Проверить что настройки применились:
```bash
python manage.py security_admin --stats
```

### 4. Протестировать новые лимиты:
```bash
python test_security.py
```

---

## ⚡ **Быстрое переключение режимов**

### Создайте файлы настроек:

**settings_strict.py:**
```python
from .settings import *

SECURITY_RATE_LIMITS = {
    'requests_per_minute': 20,
    'requests_per_hour': 200,
    # строгие настройки
}
```

**settings_soft.py:**
```python
from .settings import *

SECURITY_RATE_LIMITS = {
    'requests_per_minute': 120,
    'requests_per_hour': 3000,
    # мягкие настройки
}
```

### Запуск с разными настройками:
```bash
# Строгий режим
python manage.py runserver --settings=config.settings_strict

# Мягкий режим  
python manage.py runserver --settings=config.settings_soft
```

---

## 📈 **Мониторинг эффективности настроек**

### После изменения настроек проверяйте:

```bash
# Статистика каждые 30 минут первые 2 часа
python manage.py security_admin --stats

# Заблокированные IP
python manage.py security_admin --show-blocked

# Логи в реальном времени
tail -f logs/django.log
```

### Критерии успешных настроек:
- **< 2%** заблокированных запросов от общего трафика
- **0 жалоб** от легитимных пользователей
- **> 90%** атак заблокировано
- **< 50ms** дополнительная задержка

---

## 🎯 **Рекомендации по выбору настроек**

### 🤔 **Как выбрать правильные лимиты:**

1. **Начните с дефолтных настроек**
2. **Мониторьте 1-2 дня**
3. **Анализируйте статистику**
4. **Корректируйте по результатам**

### 📊 **Если много ложных срабатываний:**
- Увеличьте лимиты на 50%
- Проанализируйте паттерны атак
- Добавьте исключения для нужных IP

### 🚨 **Если мало атак блокируется:**
- Уменьшите лимиты на 30%
- Добавьте дополнительные паттерны
- Проверьте работу детекции

---

*Примеры настроек безопасности для различных типов сайтов*  
*Православный портал "Добрые истории"*  
*Август 2025*
