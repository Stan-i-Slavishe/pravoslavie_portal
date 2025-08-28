# 🛡️ СИСТЕМА БЕЗОПАСНОСТИ АКТИВИРОВАНА!

Ваш православный портал теперь защищен от всех основных угроз:
- DDoS атак и флуда
- SQL инъекций  
- XSS атак
- Path traversal
- Брутфорс атак
- Сканирования админки
- Спама

## 🚀 КАК ЗАПУСТИТЬ

### Вариант 1: Автоматический запуск
```bash
activate_security.bat
```

### Вариант 2: Ручной запуск  
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## 🧪 ТЕСТИРОВАНИЕ

```bash
# Тест системы безопасности
python test_security.py

# Тест через команды управления
python manage.py security_admin --test-patterns
python manage.py security_admin --stats
```

## 📊 УПРАВЛЕНИЕ

```bash
# Статистика
python manage.py security_admin --stats

# Заблокированные IP
python manage.py security_admin --show-blocked

# Разблокировать IP
python manage.py security_admin --unblock-ip 192.168.1.100

# Заблокировать IP
python manage.py security_admin --block-ip 192.168.1.100 --reason "Spam"

# Очистить все блокировки
python manage.py security_admin --clear-all
```

## 📝 ЛОГИ

Все события безопасности записываются в:
- `logs/django.log` - основные логи
- Консоль - для разработки

Примеры логов:
```
🚨 Suspicious patterns detected from 192.168.1.100: /admin.php
🚫 BLOCKED IP 192.168.1.100: Suspicious patterns detected
⚠️ Rate limit exceeded for 10.0.0.50
```

## ⚙️ НАСТРОЙКИ

### Изменить лимиты в settings.py:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 30,     # Строже
    'requests_per_hour': 300,      # Строже
    'login_attempts_per_hour': 3,  # Очень строго
}
```

### Для продакшена в .env:
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
REDIS_URL=redis://localhost:6379/0
```

## 🚨 ЧТО БЛОКИРУЕТСЯ

### Автоматически:
- SQL injection: `/?id=1; DROP TABLE users;`
- XSS: `/search?q=<script>alert("xss")</script>`
- Path traversal: `/files?path=../../etc/passwd`
- Admin scans: `/wp-admin/admin.php`
- Превышение лимитов запросов
- Большие файлы (>10MB)

### Rate limits:
- 60 запросов/минуту (30 в продакшене)
- 1000 запросов/час (500 в продакшене)  
- 10 попыток входа/час (5 в продакшене)

## 📞 ПОДДЕРЖКА

Если система заблокировала вас по ошибке:
```bash
python manage.py security_admin --unblock-ip ВАШ_IP
```

Если нужна помощь - проверьте логи:
```bash
tail -f logs/django.log
```

## 🎉 ГОТОВО!

Система безопасности работает автоматически. 
Ваш сайт теперь надежно защищен!

🛡️ Православный портал под защитой! 🛡️
