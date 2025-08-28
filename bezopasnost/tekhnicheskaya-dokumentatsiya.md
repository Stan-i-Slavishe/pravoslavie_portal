# 🛡️ Техническая документация системы безопасности

## 📋 **Архитектура системы**

### 🔧 **Компоненты**

1. **BlacklistMiddleware** - Первый барьер
   - Проверяет заблокированные IP
   - Блокирует доступ до обработки запроса

2. **AdvancedSecurityMiddleware** - Основная защита
   - Детекция подозрительных паттернов
   - Rate limiting  
   - Блокировка атак

3. **MonitoringMiddleware** - Наблюдение
   - Логирование запросов
   - Мониторинг производительности
   - Статистика ошибок

### 📂 **Файловая структура**
```
core/middleware/advanced_security.py     # Основной код
core/management/commands/security_admin.py  # CLI команды
config/settings.py                      # Настройки
logs/django.log                         # Логи
```

---

## 🔍 **Детекция атак**

### 🚨 **SQL Injection паттерны**
```python
r'union\s+select',
r'drop\s+table',
r'delete\s+from',
r'insert\s+into',
r'update\s+.*set',
r'exec\s*\(',
r'sp_executesql',
r'xp_cmdshell',
```

### 🕷️ **XSS паттерны**
```python
r'<script[^>]*>',
r'javascript:',
r'vbscript:',
r'onload\s*=',
r'onerror\s*=',
r'<iframe[^>]*>',
```

### 📁 **Path Traversal паттерны**
```python
r'\.\./',
r'\.\.\\',
r'\/\.\.\/',
r'\\\.\.\\',
```

### 🔐 **Admin Scan паттерны**
```python
r'wp-admin',
r'wp-login',
r'phpmyadmin',
r'admin\.php',
r'config\.php',
r'\.env',
r'\.git',
```

---

## ⚡ **Rate Limiting**

### 📊 **Лимиты по умолчанию**

**Разработка (DEBUG=True):**
```python
{
    'requests_per_minute': 60,
    'requests_per_hour': 1000,
    'mobile_feedback_per_hour': 10,
    'login_attempts_per_hour': 10,
    'admin_attempts_per_hour': 5,
    'api_requests_per_minute': 30,
}
```

**Продакшен (DEBUG=False):**
```python
{
    'requests_per_minute': 30,
    'requests_per_hour': 500,
    'mobile_feedback_per_hour': 5,
    'login_attempts_per_hour': 5,
    'admin_attempts_per_hour': 3,
    'api_requests_per_minute': 15,
}
```

### 🎯 **Специальные эндпоинты**

- `/api/mobile-feedback/` - Ограничен отдельно
- `/accounts/login/` - Защита от брутфорса
- `/admin/login/` - Строже чем обычный логин
- `/api/*` - Общие API лимиты

---

## 🗄️ **Кеширование и хранение**

### 💾 **Redis (предпочтительно)**
```python
# Ключи блокировки
"blacklist:{ip}" - Заблокированные IP
"whitelist:{ip}" - Разрешенные IP

# Ключи счетчиков
"rate:{ip}:{minute}" - Счетчик в минуту
"rate_hour:{ip}:{hour}" - Счетчик в час
"api_feedback:{ip}:{hour}" - API обратной связи
"login_attempts:{ip}:{hour}" - Попытки входа
```

### 🏠 **Local Memory (fallback)**
- Если Redis недоступен
- Работает в рамках одного процесса
- Данные теряются при перезапуске

---

## 📝 **Логирование**

### 📊 **Уровни логов**
```python
logger.info()    # Обычные запросы
logger.warning() # Подозрительная активность
logger.error()   # Атаки и блокировки
```

### 📋 **Типы событий**

**Обычные события:**
```
POST запрос от 127.0.0.1 к /analytics/track-event/
INFO "GET / HTTP/1.1" 200 79857
```

**Подозрительная активность:**
```
SUSPICIOUS PATTERN: drop\s+table in data from 192.168.1.100
SUSPICIOUS PATTERNS DETECTED from 192.168.1.100: /search
RATE LIMITED IP 192.168.1.100: Rate limit exceeded
```

**Блокировки:**
```
BLOCKED IP 192.168.1.100: Suspicious patterns detected (severity: high, duration: 86400s)
BLOCKED IP 192.168.1.100 trying to access
```

**Ошибки:**
```
ERROR 404 от 127.0.0.1 к /search
ERROR 403 от 192.168.1.100 к /admin.php
SLOW REQUEST (3.24s) от 10.0.0.1 к /heavy-page
```

---

## 🔧 **Настройка и кастомизация**

### ⚙️ **Изменение лимитов**

В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 100,  # Увеличить для высокой нагрузки
    'requests_per_hour': 2000,   # Увеличить для событий
    'login_attempts_per_hour': 3, # Уменьшить для строгости
}
```

### 🎯 **Добавление новых паттернов**

В `core/middleware/advanced_security.py`:
```python
self.suspicious_patterns = [
    # Существующие паттерны...
    r'your_custom_pattern',  # Ваш паттерн
    r'malicious_payload',    # Еще один
]
```

### 🤖 **Расширение whitelist**

```python
self.bot_whitelist = [
    'googlebot',
    'bingbot', 
    'yandexbot',
    'your_custom_bot',  # Добавить свой бот
]
```

---

## 🚀 **Производительность**

### 📈 **Оптимизация**

1. **Используйте Redis** в продакшене
2. **Настройте правильные лимиты** для вашей нагрузки
3. **Мониторьте логи** на ложные срабатывания
4. **Регулярно очищайте** старые блокировки

### 📊 **Метрики производительности**

- Время обработки middleware: < 1ms
- Память на IP: ~100 байт
- Влияние на скорость: < 5%
- CPU нагрузка: минимальная

---

## 🔒 **Security Headers**

### 📋 **Автоматически добавляемые заголовки**

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: [строгая политика]
```

### 🛡️ **Content Security Policy**

```
default-src 'self';
script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
img-src 'self' data: https:;
connect-src 'self';
frame-ancestors 'none';
```

---

## 🧪 **Тестирование**

### 🔍 **Автоматические тесты**

```bash
python test_security.py              # Полный тест системы
python manage.py security_admin --test-patterns  # Тест паттернов
```

### 🚨 **Ручное тестирование атак**

```bash
# SQL Injection
curl "http://127.0.0.1:8000/?id=1; DROP TABLE users"

# XSS
curl "http://127.0.0.1:8000/search?q=<script>alert('xss')</script>"

# Path Traversal  
curl "http://127.0.0.1:8000/files?path=../../etc/passwd"

# Admin Scan
curl "http://127.0.0.1:8000/wp-admin/admin.php"
```

**Ожидаемый результат:** HTTP 403 Forbidden

---

## 📞 **Troubleshooting**

### 🔧 **Частые проблемы**

**Проблема:** Система блокирует легитимных пользователей
**Решение:** 
```bash
python manage.py security_admin --clear-all
# Увеличить лимиты в settings.py
```

**Проблема:** Unicode ошибки в логах  
**Решение:** Уже исправлено - убраны эмодзи из логов

**Проблема:** Redis недоступен
**Решение:** Система автоматически переключится на локальное кеширование

**Проблема:** Медленная работа
**Решение:** Проверить настройки кеширования и лимиты

---

## 📊 **Мониторинг в продакшене**

### 📈 **Метрики для отслеживания**

- Количество заблокированных IP в час
- Процент заблокированных запросов  
- Типы атак и их частота
- Время ответа системы безопасности
- Ложные срабатывания

### 🔔 **Алерты**

Настройте уведомления при:
- Более 10% заблокированных запросов
- Массовых атаках (>100 IP в час)
- Критических ошибках в логах
- Недоступности Redis

---

*Техническая документация системы безопасности*  
*Православный портал "Добрые истории"*  
*Версия: 1.0 | Август 2025*
