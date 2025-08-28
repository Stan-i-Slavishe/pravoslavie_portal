# 🛡️ Система безопасности православного портала

## 🎯 Обзор защиты

Наш православный портал теперь защищен комплексной системой безопасности, которая защищает от:
- **DDoS атак** и флуда запросов
- **SQL injection** и XSS атак
- **Брутфорс атак** на формы входа
- **Подозрительных паттернов** в запросах
- **Спама через мобильную обратную связь**

## 🚀 Быстрая установка

```bash
# Запустите установочный скрипт
setup_security.bat
```

## 🔧 Ручная настройка

### 1. Middleware уже добавлены в settings.py:
```python
MIDDLEWARE = [
    'core.middleware.security.BlacklistMiddleware',  # Черный список
    'core.middleware.security.SecurityMiddleware',   # Основная защита
    # ... другие middleware ...
    'core.middleware.security.MonitoringMiddleware', # Мониторинг
]
```

### 2. Лимиты запросов (настраиваемые):
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 60,      # Запросов в минуту
    'requests_per_hour': 1000,      # Запросов в час  
    'mobile_feedback_per_hour': 10, # Мобильная обратная связь
    'login_attempts_per_hour': 10,  # Попытки входа
}
```

## 🛡️ Типы защиты

### 1. **Rate Limiting**
- ✅ **60 запросов/минуту** для обычных пользователей
- ✅ **1000 запросов/час** максимум
- ✅ **10 попыток входа/час** на IP
- ✅ **10 мобильных отзывов/час** на IP

### 2. **Детекция подозрительных паттернов**
Автоматическая блокировка при обнаружении:
- `../` - Path traversal атаки
- `<script` - XSS попытки  
- `union select` - SQL injection
- `wp-admin` - WordPress атаки
- `.php`, `.asp` - Поиск уязвимых файлов
- `.env`, `.git` - Попытки доступа к конфигам

### 3. **API Protection**
Специальная защита для:
- `/api/mobile-feedback/` - Ограничение спама
- `/accounts/login/` - Защита от брутфорса
- `/admin/login/` - Защита админки

### 4. **Security Headers**
Автоматическое добавление заголовков:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy` (базовый)
- `Referrer-Policy: strict-origin-when-cross-origin`

## 📊 Управление системой

### Просмотр заблокированных IP:
```bash
python manage.py security --show-blocked
```

### Разблокировка IP:
```bash
python manage.py security --unblock-ip 192.168.1.100
```

### Блокировка IP вручную:
```bash
python manage.py security --block-ip 192.168.1.100 --reason "Spam"
```

### Статистика безопасности:
```bash
python manage.py security --stats
```

### Очистка всех блокировок:
```bash
python manage.py security --clear-all
```

## 📝 Логирование

### Логи безопасности сохраняются в:
- **Файл:** `logs/security.log`
- **Консоль:** Для разработки
- **Уровни:** INFO, WARNING, ERROR

### Примеры логов:
```
[2025-01-XX 10:30:15] WARNING core.middleware.security: Подозрительный запрос от 192.168.1.100: /admin.php
[2025-01-XX 10:30:16] ERROR core.middleware.security: Заблокирован запрос от 192.168.1.100: Suspicious patterns detected
```

## ⚙️ Настройка для продакшена

### 1. Включите Redis для кеширования:
```bash
# В .env файле
REDIS_URL=redis://localhost:6379/0
```

### 2. Строгие лимиты для продакшена:
При `DEBUG=False` автоматически включаются строгие лимиты:
- 30 запросов/минуту (вместо 60)
- 500 запросов/час (вместо 1000)
- 5 попыток входа/час (вместо 10)

### 3. HTTPS настройки:
```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🔥 Что происходит при атаке

### 1. **Превышение лимитов:**
```json
{
  "error": "Too many requests",
  "message": "Ваш IP адрес временно заблокирован из-за подозрительной активности",
  "blocked_until": 1640995200
}
```

### 2. **Подозрительные паттерны:**
- IP автоматически блокируется на 1 час
- Запись в лог с деталями атаки
- Возврат HTTP 429 (Too Many Requests)

### 3. **Повторные нарушения:**
- Увеличение времени блокировки
- Возможность ручной блокировки навсегда

## 🆘 Экстренные меры

### При массовой атаке:
```bash
# Заблокировать весь диапазон IP
python manage.py security --block-ip 192.168.1.0/24 --reason "Mass attack"

# Включить режим обслуживания через админку
# Или временно изменить лимиты в settings.py
```

### Восстановление после атаки:
```bash
# Очистить все блокировки
python manage.py security --clear-all

# Проверить логи
tail -f logs/security.log

# Перезапустить сервер
python manage.py runserver
```

## 📈 Мониторинг

### Что отслеживается:
- ✅ Количество запросов по IP
- ✅ Время ответа сервера
- ✅ Ошибки 4xx/5xx
- ✅ POST запросы
- ✅ Медленные запросы (>2 сек)

### Интеграция с внешним мониторингом:
```python
# Добавьте в settings.py для интеграции с Sentry/ELK
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'sentry_sdk.integrations.logging.EventHandler',
}
```

## 🎯 Производительность

### Влияние на скорость:
- **Минимальное** - middleware работают очень быстро
- **Кеширование** - все проверки кешируются
- **Асинхронность** - не блокирует выполнение запросов

### Оптимизация:
- Используйте Redis для продакшена
- Настройте правильные лимиты
- Мониторьте логи на предмет ложных срабатываний

## 🔐 Дополнительные рекомендации

### 1. **На уровне сервера (Nginx/Apache):**
```nginx
# Nginx rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=1r/s;
limit_req zone=api burst=5 nodelay;
```

### 2. **Cloudflare/CDN:**
- Включите DDoS protection
- Настройте WAF правила
- Используйте геоблокировку при необходимости

### 3. **Мониторинг сервера:**
```bash
# Установите мониторинг
pip install psutil
# Добавьте алерты на высокую нагрузку
```

## ⚠️ Важные замечания

1. **Не блокируйте поисковых ботов** - добавьте их в whitelist
2. **Тестируйте лимиты** на development окружении
3. **Регулярно проверяйте логи** на ложные срабатывания
4. **Имейте план восстановления** на случай сбоя

---

**🎉 Ваш православный портал теперь надежно защищен от всех основных типов атак!**

**📞 Поддержка:** При возникновении проблем с безопасностью, проверьте логи и используйте команды управления.