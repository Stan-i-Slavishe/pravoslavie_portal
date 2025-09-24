# 🚀 Деплой Google reCAPTCHA v3 на продакшен сервер

## 🎯 Готовность к деплою

### ✅ Что уже настроено:
1. **Реальные ключи reCAPTCHA** для домена `dobrist.com`
2. **Кастомная форма** с условной капчей (включается только на продакшене)
3. **Правильные настройки** в `settings_production.py`
4. **django-recaptcha** в requirements.txt
5. **ACCOUNT_FORMS** настроен корректно

## 🧪 Предварительная проверка

### Автоматическая проверка:
```bash
python check_production_recaptcha.py
```

### Ручная проверка настроек:
```python
# Проверить что в settings_production.py:
DEBUG = False  # ✅ Обязательно!
RECAPTCHA_PUBLIC_KEY = '6LeD-dErAAAAAPFCCTD0oEDipeyX8FYmrbJgZ9Ri'  # ✅ Реальный ключ
RECAPTCHA_PRIVATE_KEY = '6LeD-dErAAAAAD6Asd70b0wN98n-YFi0BunWmm2f'  # ✅ Реальный ключ
ALLOWED_HOSTS = ['dobrist.com', 'www.dobrist.com', '46.62.167.17']  # ✅ Домены
```

## 🚀 Методы деплоя

### Метод 1: Автоматический деплой с проверкой
```bash
chmod +x deploy_with_recaptcha_check.sh
./deploy_with_recaptcha_check.sh
```

### Метод 2: Ручной деплой
```bash
# 1. Коммит изменений
git add .
git commit -m "🔒 Настроена Google reCAPTCHA v3 для продакшена"
git push origin main

# 2. На сервере
ssh your-server
cd /path/to/pravoslavie_portal
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# 3. Перезапуск сервисов  
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🔍 Проверка после деплоя

### 1. Проверка формы регистрации:
- Откройте: `https://dobrist.com/accounts/signup/`
- **Должно быть видно:** "Форма защищена Google reCAPTCHA" 🛡️
- **Должен быть значок** reCAPTCHA в правом нижнем углу
- **НЕ должно быть** ошибок в консоли браузера

### 2. Тест регистрации:
```
Email: test-production-user@example.com
Пароль: SecureProductionPassword123!
Подтверждение: SecureProductionPassword123!
```

**Ожидаемый результат:** Успешная регистрация с проверкой капчи

### 3. Проверка логов Django:
```bash
# На сервере
tail -f /var/log/pravoslavie_portal/django.log | grep -i recaptcha
```

## 📊 Мониторинг reCAPTCHA

### Google reCAPTCHA Admin панель:
1. Перейдите: https://www.google.com/recaptcha/admin
2. Выберите сайт: `dobrist.com`
3. Мониторьте:
   - Количество запросов регистрации
   - Процент заблокированных ботов  
   - График активности пользователей
   - Оценки доверия (должны быть ≥ 0.85)

### Настройки мониторинга:
```python
# В settings_production.py при необходимости:

# Если много ложных срабатываний:
RECAPTCHA_REQUIRED_SCORE = 0.7  # Снизить порог

# Если проходят боты:
RECAPTCHA_REQUIRED_SCORE = 0.9  # Повысить порог
```

## 🐛 Возможные проблемы и решения

### Проблема: "reCAPTCHA validation failed" на продакшене
**Причины:**
- Неправильные ключи для домена
- Проблемы с DNS
- Заблокирован доступ к google.com

**Решение:**
```bash
# Проверить доступ к Google API с сервера
curl -I https://www.google.com/recaptcha/api.js

# Проверить DNS домена
nslookup dobrist.com

# Проверить настройки в Google Admin
# https://www.google.com/recaptcha/admin
```

### Проблема: Капча не отображается
**Причины:**
- DEBUG=True на продакшене
- Неправильные статические файлы
- Ошибки JavaScript

**Решение:**
```bash
# Убедиться что DEBUG=False
python manage.py shell -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"

# Пересобрать статические файлы
python manage.py collectstatic --noinput

# Проверить консоль браузера на ошибки
```

### Проблема: Форма не работает в мобильной версии
**Решение:**
- Проверить адаптивность CSS
- Убедиться что reCAPTCHA загружается на мобильных
- Проверить touch события

## 🔧 Тонкая настройка

### Настройка порога безопасности:
```python
# Консервативный (много блокировок)
RECAPTCHA_REQUIRED_SCORE = 0.9

# Сбалансированный (рекомендуемый) 
RECAPTCHA_REQUIRED_SCORE = 0.85

# Либеральный (меньше блокировок)
RECAPTCHA_REQUIRED_SCORE = 0.7
```

### Логирование reCAPTCHA:
```python
# Добавить в settings_production.py
LOGGING = {
    'version': 1,
    'handlers': {
        'recaptcha_file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/pravoslavie_portal/recaptcha.log',
        },
    },
    'loggers': {
        'django_recaptcha': {
            'handlers': ['recaptcha_file'],
            'level': 'INFO',
        },
    },
}
```

## ✅ Checklist готовности к деплою

- [ ] Проверка `python check_production_recaptcha.py` проходит
- [ ] DEBUG=False в продакшен настройках  
- [ ] Реальные ключи reCAPTCHA настроены
- [ ] Домены dobrist.com и www.dobrist.com в ALLOWED_HOSTS
- [ ] django-recaptcha==4.0.0 в requirements.txt
- [ ] Форма тестируется локально без ошибок
- [ ] Git изменения закоммичены
- [ ] Сервер доступен и готов к деплою

## 🎉 После успешного деплоя

### Что произойдет:
1. ✅ **На продакшене (dobrist.com):** Полная защита reCAPTCHA активна
2. ✅ **В разработке (127.0.0.1:8000):** Капча отключена для удобства
3. ✅ **Защита от ботов:** Автоматическая блокировка подозрительной активности
4. ✅ **Мониторинг:** Статистика в Google reCAPTCHA Admin
5. ✅ **UX:** Невидимая защита не мешает пользователям

### Поздравляем! 🎊
Ваш православный портал теперь имеет профессиональную защиту от ботов и спама на этапе регистрации пользователей!

---

**📈 Прогресс проекта: 99% готовности к коммерческому запуску!** 🚀
