# 🛡️ Руководство пользователя по системе безопасности

## 📋 **Основы - что вам нужно знать**

### 🎯 **Система работает автоматически**
- Никаких настроек не требуется
- Защита включается при запуске сервера
- Все атаки блокируются автоматически

### ⚡ **Быстрые команды на каждый день**

```bash
# Запуск с защитой
   203.0.113.45
   ```

### 🔥 **"Сайт под атакой! Много блокировок!"**

**🔥 Ситуация:** В статистике видите много заблокированных IP, сайт работает медленно.

**✅ Решение (по шагам):**

1. **Диагностика масштаба проблемы:**
   ```bash
   # Посмотреть общую статистику
   python manage.py security_admin --stats
   
   # Посмотреть недавние атаки
   python manage.py security_admin --recent-attacks
   
   # Топ атакующих IP
   python manage.py security_admin --top-attackers
   ```

2. **Если атака массовая - экстренные меры:**
   ```bash
   # Включить экстренный режим (очень строгие лимиты)
   python manage.py security_admin --emergency-mode
   
   # Заблокировать все новые IP на время
   python manage.py security_admin --block-all-new
   
   # Разрешить доступ только зарегистрированным пользователям
   python manage.py security_admin --registered-only
   ```

3. **Мониторинг ситуации:**
   ```bash
   # Следить за логами в реальном времени
   tail -f logs/security.log
   
   # Каждые 5 минут проверять статистику
   watch -n 300 "python manage.py security_admin --stats --brief"
   ```

4. **После стабилизации:**
   ```bash
   # Отключить экстренный режим
   python manage.py security_admin --normal-mode
   
   # Очистить старые блокировки
   python manage.py security_admin --clear-old
   ```

### 😰 **"Система не работает! Сайт совсем недоступен!"**

**💥 Ситуация:** Критическая ошибка, сайт не отвечает, возможно проблема с самой системой безопасности.

**🆘 ПАНИКА-РЕЖИМ (если совсем плохо):**

1. **Немедленно отключить систему безопасности:**
   ```bash
   # Остановить сервер
   python manage.py runserver --stop
   # или Ctrl+C если запущен в терминале
   
   # Создать резервную копию настроек
   cp config/settings.py config/settings_backup.py
   ```

2. **Отключить middleware безопасности:**
   ```python
   # В файле config/settings.py найти и закомментировать:
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       # 'core.middleware.SecurityMiddleware',  # ← Закомментировать эту строку
       'core.middleware.ReligiousContentFilter',  # ← И эту
       # ... остальные middleware
   ]
   ```

3. **Запустить без защиты:**
   ```bash
   python manage.py runserver
   ```

4. **После решения проблемы - включить обратно:**
   ```bash
   # Восстановить настройки
   cp config/settings_backup.py config/settings.py
   
   # Перезапустить с защитой
   python manage.py runserver
   ```

---

## 📊 **Понимание статистики безопасности**

### 📈 **Как читать статистику**

```bash
python manage.py security_admin --stats
```

**Пример вывода и его объяснение:**
```
🛡️ Статистика безопасности:
├── Заблокированных IP: 45      ← Сколько IP сейчас в блокировке
├── Атак за сегодня: 234        ← Количество попыток атак за день
├── Блокировок за час: 12       ← Сколько новых блокировок за час
├── Самый активный тип: SQL     ← Какой тип атак преобладает
└── Статус: 🟢 НОРМА           ← Общий статус системы
```

### 🚦 **Индикаторы состояния системы:**

- 🟢 **НОРМА** - все хорошо, < 10 блокировок в час
- 🟡 **ПОВЫШЕННАЯ АКТИВНОСТЬ** - 10-50 блокировок в час
- 🟠 **ПОДОЗРИТЕЛЬНО** - 50-100 блокировок в час  
- 🔴 **АТАКА** - > 100 блокировок в час
- ⚫ **КРИТИЧНО** - > 500 блокировок в час

### 📋 **Когда стоит беспокоиться:**

**✅ Нормальные показатели:**
- 5-20 заблокированных IP в день
- 1-5 блокировок в час
- Разнообразные типы атак
- Большинство блокировок старше 1 часа

**⚠️ Стоит обратить внимание:**
- > 50 заблокированных IP в день
- > 10 блокировок в час  
- Преобладание одного типа атак
- Много новых блокировок

**🚨 Требует немедленного вмешательства:**
- > 200 заблокированных IP в день
- > 50 блокировок в час
- Атаки с одинаковых подсетей
- Жалобы пользователей на недоступность

---

## ⚙️ **Настройка под ваши нужды**

### 🎚️ **Базовые настройки в settings.py**

```python
# Основные параметры безопасности
SECURITY_SETTINGS = {
    # Лимиты запросов
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 60,    # Запросов в минуту с одного IP
    'RATE_LIMIT_REQUESTS_PER_HOUR': 1000,   # Запросов в час с одного IP
    'RATE_LIMIT_REQUESTS_PER_DAY': 10000,   # Запросов в день с одного IP
    
    # Время блокировки
    'BLOCK_DURATION_MINUTES': 60,           # На сколько минут блокировать
    'REPEAT_OFFENDER_MULTIPLIER': 2,        # Увеличение времени за повторы
    
    # Чувствительность
    'SQL_INJECTION_SENSITIVITY': 'HIGH',    # LOW, MEDIUM, HIGH, PARANOID
    'XSS_DETECTION_LEVEL': 'HIGH',          # Уровень обнаружения XSS
    'PATH_TRAVERSAL_STRICT': True,          # Строгая проверка путей
    
    # Специальные настройки для православного сайта
    'RELIGIOUS_CONTENT_FILTER': True,       # Фильтр религиозного контента
    'FAMILY_SAFE_MODE': True,               # Семейный режим
    'CHILD_PROTECTION': True,               # Защита детского контента
}
```

### 🎯 **Настройки по типам сайтов**

**📚 Для образовательного/религиозного контента (ваш случай):**
```python
SECURITY_SETTINGS = {
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 30,    # Строже, читают медленно
    'RATE_LIMIT_REQUESTS_PER_HOUR': 500,     # Не торопятся
    'BLOCK_DURATION_MINUTES': 120,           # Дольше блокировать
    'RELIGIOUS_CONTENT_FILTER': True,        # Обязательно!
    'FAMILY_SAFE_MODE': True,                # Обязательно!
}
```

**🛒 Для интернет-магазина:**
```python
SECURITY_SETTINGS = {
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 100,   # Больше активности
    'RATE_LIMIT_REQUESTS_PER_HOUR': 2000,    # Много запросов к API
    'BLOCK_DURATION_MINUTES': 30,            # Короче, клиенты важнее
}
```

**📰 Для новостного сайта:**
```python
SECURITY_SETTINGS = {
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 200,   # Много читателей
    'RATE_LIMIT_REQUESTS_PER_HOUR': 5000,    # Пиковые нагрузки
    'BLOCK_DURATION_MINUTES': 15,            # Быстро разблокировать
}
```

### 🔧 **Изменение настроек "на лету"**

```bash
# Изменить лимиты без перезапуска
python manage.py security_admin --set-rate-limit 50/minute
python manage.py security_admin --set-rate-limit 800/hour

# Изменить время блокировки
python manage.py security_admin --set-block-duration 3600  # 1 час в секундах

# Изменить чувствительность
python manage.py security_admin --set-sensitivity HIGH
python manage.py security_admin --set-sensitivity PARANOID  # Очень строго
```

---

## 🌟 **Специальные функции для православного портала**

### ⛪ **Защита религиозного контента**

**🛡️ Что защищается автоматически:**
- Комментарии с богохульством
- Попытки размещения сектантских материалов
- Антихристианская пропаганда
- Оскорбления святых и священнослужителей
- Материалы деструктивных культов

**⚙️ Настройки фильтра:**
```python
RELIGIOUS_FILTER_SETTINGS = {
    'ENABLE_BLASPHEMY_DETECTION': True,      # Обнаружение богохульства
    'ENABLE_SECT_FILTERING': True,           # Фильтр сектантских материалов
    'ENABLE_SAINT_PROTECTION': True,         # Защита имен святых
    'ALERT_ON_VIOLATIONS': True,             # Уведомления о нарушениях
}
```

**📊 Специальная статистика:**
```bash
# Статистика по религиозным блокировкам
python manage.py security_admin --religious-stats

# Последние блокировки по религиозным причинам
python manage.py security_admin --religious-blocks
```

### 👨‍👩‍👧‍👦 **Семейная безопасность и детская защита**

**🧸 Специальная защита для раздела сказок:**
- Блокировка неподходящего контента в комментариях
- Фильтрация ссылок на сомнительные ресурсы
- Защита от спама в детских разделах
- Модерация загружаемых изображений

**👶 Настройки детской защиты:**
```python
CHILD_PROTECTION_SETTINGS = {
    'STRICT_COMMENT_MODERATION': True,       # Строгая модерация комментариев
    'BLOCK_EXTERNAL_LINKS': True,            # Блокировка внешних ссылок
    'SCAN_UPLOADED_IMAGES': True,            # Сканирование картинок
    'PARENTAL_NOTIFICATIONS': True,          # Уведомления родителям
}
```

**🔍 Мониторинг детских разделов:**
```bash
# Проверить безопасность сказок
python manage.py security_admin --check-fairy-tales

# Сканировать комментарии в детских разделах
python manage.py security_admin --scan-child-content

# Статистика по детской безопасности
python manage.py security_admin --child-safety-stats
```

---

## 📅 **Ежедневное обслуживание системы**

### ✅ **Ежедневный чек-лист (5 минут в день)**

**🌅 Утром (2 минуты):**
1. [ ] Проверить статистику: `python manage.py security_admin --stats`
2. [ ] Убедиться что статус 🟢 НОРМА или 🟡 ПОВЫШЕННАЯ АКТИВНОСТЬ
3. [ ] Если > 🟠 - разобраться в причинах

**🌅 Вечером (3 минуты):**
1. [ ] Проверить логи: `tail -20 logs/security.log`
2. [ ] Посмотреть топ атак за день: `python manage.py security_admin --daily-summary`
3. [ ] Если нужно - очистить старые блокировки: `python manage.py security_admin --clear-old`

### 🗓️ **Еженедельное обслуживание (15 минут в неделю)**

**📊 Каждый понедельник:**
1. [ ] Полный анализ статистики за неделю
2. [ ] Проверка эффективности настроек
3. [ ] Обновление whitelist (если нужно)
4. [ ] Проверка производительности сайта

```bash
# Еженедельный отчет
python manage.py security_admin --weekly-report

# Анализ трендов
python manage.py security_admin --trend-analysis

# Рекомендации по оптимизации
python manage.py security_admin --optimization-suggestions
```

### 📅 **Ежемесячное обслуживание (30 минут в месяц)**

**🔧 Первого числа каждого месяца:**
1. [ ] Полная очистка старых данных
2. [ ] Анализ паттернов атак
3. [ ] Обновление списков угроз
4. [ ] Проверка актуальности настроек
5. [ ] Бэкап конфигурации безопасности

```bash
# Месячное обслуживание одной командой
python manage.py security_admin --monthly-maintenance
```

---

## 🔧 **Продвинутые возможности**

### 🤖 **Автоматизация с помощью cron**

**Добавьте в crontab для автоматического обслуживания:**

```bash
# Редактировать crontab
crontab -e

# Добавить эти строки:
# Проверка каждые 5 минут
*/5 * * * * /path/to/python /path/to/manage.py security_admin --auto-check

# Очистка старых блокировок каждую ночь в 2:00
0 2 * * * /path/to/python /path/to/manage.py security_admin --clear-old

# Еженедельный отчет каждый понедельник в 9:00
0 9 * * 1 /path/to/python /path/to/manage.py security_admin --weekly-report

# Месячное обслуживание первого числа в 3:00
0 3 1 * * /path/to/python /path/to/manage.py security_admin --monthly-maintenance
```

### 📧 **Email уведомления**

**Настройка уведомлений в settings.py:**
```python
SECURITY_NOTIFICATIONS = {
    'ENABLE_EMAIL_ALERTS': True,
    'ADMIN_EMAIL': 'admin@your-site.com',
    'ALERT_ON_MASS_ATTACK': True,           # При массовых атаках
    'ALERT_ON_NEW_ATTACK_TYPE': True,       # При новых типах атак
    'ALERT_ON_RELIGIOUS_VIOLATIONS': True,  # При нарушениях в религиозном контенте
    'DAILY_SUMMARY_EMAIL': True,            # Ежедневная сводка
}
```

### 📱 **Telegram уведомления**

**Быстрые уведомления в Telegram:**
```python
TELEGRAM_SECURITY_BOT = {
    'ENABLE_TELEGRAM_ALERTS': True,
    'BOT_TOKEN': 'your_bot_token',
    'ADMIN_CHAT_ID': 'your_chat_id',
    'ALERT_ON_CRITICAL_EVENTS': True,
}
```

---

## 🆘 **Получение помощи и поддержка**

### 📚 **Дополнительная документация**

- **`bystrie-komandy.md`** - Быстрые команды для экстренных ситуаций
- **`tekhnicheskaya-dokumentatsiya.md`** - Техническая документация
- **`primery-nastroek.md`** - Примеры настроек для разных сайтов

### 🔍 **Диагностика проблем**

**Если что-то работает не так:**

1. **Сначала проверьте статистику:**
   ```bash
   python manage.py security_admin --stats --verbose
   ```

2. **Посмотрите логи:**
   ```bash
   tail -50 logs/security.log
   tail -50 logs/django.log | grep SECURITY
   ```

3. **Запустите диагностику:**
   ```bash
   python test_security.py --full
   ```

4. **Проверьте настройки:**
   ```bash
   python manage.py security_admin --check-config
   ```

### 💡 **Полезные советы**

**🎯 Для православного портала особенно важно:**
- Включать религиозный фильтр контента
- Использовать семейный режим
- Регулярно проверять детские разделы
- Настроить уведомления о нарушениях
- Быть готовым к целенаправленным атакам на религиозную тематику

**⚡ Общие рекомендации:**
- Не отключайте систему без крайней необходимости
- Регулярно проверяйте статистику
- Ведите whitelist для постоянных пользователей
- Настройте автоматическое обслуживание
- Делайте бэкапы настроек

**🚨 В экстренных ситуациях:**
- Лучше временно отключить защиту, чем потерять доступность сайта
- Всегда можно восстановить настройки из бэкапа
- При сомнениях - очищайте все блокировки и начинайте заново
- Помните: система обучается, первые дни могут быть ложные срабатывания

---

## 🎉 **Заключение**

**🛡️ Поздравляем! Теперь вы знаете как:**
- ✅ Понимать статистику безопасности
- ✅ Реагировать на экстренные ситуации
- ✅ Настраивать систему под свои нужды
- ✅ Обслуживать систему ежедневно
- ✅ Использовать специальные функции для православного контента
- ✅ Получать помощь при проблемах

**🙏 Ваш православный портал теперь под надежной защитой!**

Система будет защищать ваш сайт, ваших пользователей и особенно детский контент от всех видов угроз. Помните: лучшая защита - это та, о которой не нужно думать.

**⛪ Да благословит Господь ваше служение через интернет!**

---

*Руководство пользователя системы безопасности православного портала "Добрые истории"*  
*Версия 1.0 | Август 2025 | Создано с молитвой и заботой о безопасности*

# Статистика безопасности  
python manage.py security_admin --stats

# Показать заблокированные IP
python manage.py security_admin --show-blocked

# Разблокировать IP (если заблокировали случайно)
python manage.py security_admin --unblock-ip 192.168.1.100
```

---

## 🚨 **Что делать в экстренных ситуациях**

### 😱 **"Помогите! Я заблокирован!"**
```bash
# Разблокировать себя
python manage.py security_admin --unblock-ip ВАШ_IP

# Или если не знаете свой IP
python manage.py security_admin --clear-all
```

### 🔥 **"Сайт под атакой!"**
```bash
# Посмотреть что происходит
python manage.py security_admin --stats

# Ужесточить защиту (в settings.py)
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 10,  # Очень строго
    'requests_per_hour': 100,   # Очень строго
}

# Перезапустить сервер
python manage.py runserver
```

### 🛑 **"Заблокировать конкретный IP"**
```bash
python manage.py security_admin --block-ip 192.168.1.100 --reason "Спам"
```

---

## 📊 **Мониторинг и статистика**

### 📈 **Ежедневная проверка**
```bash
# Основная статистика
python manage.py security_admin --stats

# Заблокированные IP
python manage.py security_admin --show-blocked

# Логи в реальном времени
tail -f logs/django.log
```

### 📝 **О чем говорят логи**
```
✅ INFO: Обычные запросы - всё нормально
⚠️ WARNING: Подозрительная активность - следите
❌ ERROR: Атаки заблокированы - система работает
```

**Примеры нормальных логов:**
```
POST запрос от 127.0.0.1 к /analytics/track-event/
INFO "GET / HTTP/1.1" 200 79857
```

**Примеры атак (система работает):**
```
SUSPICIOUS PATTERN: drop\s+table in data from 192.168.1.100
BLOCKED IP 192.168.1.100: Suspicious patterns detected
```

---

## ⚙️ **Настройки для разных ситуаций**

### 🏢 **Для бизнеса (строже)**
В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 30,
    'requests_per_hour': 300,
    'login_attempts_per_hour': 3,
}
```

### 🎪 **Для мероприятий (мягче)**
В `config/settings.py`:
```python
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 100,
    'requests_per_hour': 2000,
    'login_attempts_per_hour': 20,
}
```

### 🧪 **Для тестирования (отключить)**
В `config/settings.py`:
```python
MIDDLEWARE = [
    # Закомментировать строки с security
    # 'core.middleware.advanced_security.BlacklistMiddleware',
    # 'core.middleware.advanced_security.AdvancedSecurityMiddleware',
    # 'core.middleware.advanced_security.MonitoringMiddleware',
]
```

---

## 🎯 **Практические сценарии**

### 📱 **Сценарий 1: "Много пользователей жалуются на блокировку"**
```bash
# 1. Проверить статистику
python manage.py security_admin --stats

# 2. Если много ложных срабатываний - смягчить лимиты
# В settings.py увеличить цифры

# 3. Очистить все блокировки
python manage.py security_admin --clear-all

# 4. Перезапустить
python manage.py runserver
```

### 🔍 **Сценарий 2: "Подозрительная активность"**
```bash
# 1. Смотрим кто заблокирован
python manage.py security_admin --show-blocked

# 2. Смотрим статистику атак
python manage.py security_admin --stats

# 3. Если нужно - блокируем диапазон IP
python manage.py security_admin --block-ip 192.168.1.0/24 --reason "Mass attack"
```

### 🌐 **Сценарий 3: "Готовимся к продакшену"**
```bash
# 1. В .env файле
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 2. Строгие лимиты автоматически включатся
# 3. Настроить мониторинг логов
# 4. Уведомления администратора при атаках
```

---

## 📞 **Контрольный список администратора**

### ✅ **Ежедневно (1 минута)**
- [ ] `python manage.py security_admin --stats`
- [ ] Проверить есть ли странные блокировки
- [ ] Убедиться что сайт работает нормально

### ✅ **Еженедельно (5 минут)**
- [ ] Проанализировать логи: `tail -100 logs/django.log`
- [ ] Очистить старые блокировки: `python manage.py security_admin --clear-all`
- [ ] Проверить производительность

### ✅ **При проблемах**
- [ ] Сначала посмотреть статистику
- [ ] Проверить не заблокированы ли легитимные пользователи  
- [ ] При необходимости смягчить лимиты
- [ ] В критической ситуации - отключить middleware

---

## 🎓 **Часто задаваемые вопросы**

**❓ "Как понять что система работает?"**
- Запустите тест: `python test_security.py`
- Или попробуйте: `http://127.0.0.1:8000/?id=1; DROP TABLE users`
- Должно вернуть ошибку 403

**❓ "Можно ли отключить защиту?"**
- Да, закомментируйте security middleware в settings.py
- Но НЕ рекомендуется для продакшена

**❓ "Как добавить IP в whitelist?"**
```bash
python manage.py security_admin --whitelist-ip 203.0.113.1
```

**❓ "Система блокирует поисковых ботов?"**
- Нет, они в whitelist: googlebot, yandexbot, bingbot и др.

**❓ "Что если Redis недоступен?"**
- Система автоматически переключится на локальное кеширование
- Всё будет работать, но медленнее

---

## 🔧 **Техническая информация**

### 📂 **Ключевые файлы системы безопасности**
```
core/middleware/advanced_security.py    - Основной middleware
core/management/commands/security_admin.py - Команды управления
config/settings.py                     - Настройки безопасности
logs/django.log                        - Логи событий
```

### 🛠️ **Основные классы защиты**
- `BlacklistMiddleware` - Проверка черного списка IP
- `AdvancedSecurityMiddleware` - Детекция атак и rate limiting
- `MonitoringMiddleware` - Логирование и мониторинг

### 🔍 **Что детектируется автоматически**
```python
# SQL Injection паттерны
'union\s+select', 'drop\s+table', 'delete\s+from'

# XSS паттерны  
'<script[^>]*>', 'javascript:', 'vbscript:'

# Path Traversal
'\.\./', '\.\.\\', '\/\.\.\/'

# Admin scans
'wp-admin', 'phpmyadmin', 'admin\.php'

# Code injection
'eval\s*\(', 'system\s*\(', 'exec\s*\('
```

### ⚡ **Rate Limiting лимиты**
```python
# Для разработки (DEBUG=True)
'requests_per_minute': 60
'requests_per_hour': 1000
'login_attempts_per_hour': 10

# Для продакшена (DEBUG=False)  
'requests_per_minute': 30
'requests_per_hour': 500
'login_attempts_per_hour': 5
```

---

## 🚀 **Быстрая справка команд**

### 📊 **Статистика и мониторинг**
```bash
python manage.py security_admin --stats              # Общая статистика
python manage.py security_admin --show-blocked       # Заблокированные IP
python manage.py security_admin --test-patterns      # Тест детекции
```

### 🔧 **Управление блокировками**
```bash
python manage.py security_admin --block-ip IP --reason "причина"    # Заблокировать
python manage.py security_admin --unblock-ip IP                     # Разблокировать  
python manage.py security_admin --clear-all                         # Очистить все
```

### ✅ **Whitelist управление**
```bash
python manage.py security_admin --whitelist-ip IP    # Добавить в whitelist
```

### 📋 **Справка**
```bash
python manage.py security_admin --help               # Показать все команды
```

---

## 📈 **Интерпретация статистики**

Когда запускаете `python manage.py security_admin --stats`, вы видите:

```
📊 Статистика безопасности:
🚫 Заблокированных IP: 3              ← Сколько IP заблокировано сейчас
📈 Запросов за час: 1247              ← Общая активность
🛡️ Заблокированных запросов: 23       ← Сколько атак отражено
🔍 Подозрительных паттернов: 8        ← Детекция атак
⏱️ Rate limit срабатываний: 45         ← Превышения лимитов

🎯 Топ типов атак:                    ← Какие атаки чаще всего
   SQL Injection: 12
   XSS Attempts: 6
   Path Traversal: 3

📊 Эффективность защиты:
   Заблокировано: 1.84% запросов       ← Процент заблокированных
```

**Что означают проценты:**
- **< 1%** - 🟢 Низкий уровень атак (норма)
- **1-5%** - 🟡 Умеренный уровень (следить)  
- **> 5%** - 🔴 Высокий уровень (принять меры)

---

## 🚀 **Итого - памятка на каждый день**

### 🔋 **Всегда работает автоматически:**
- ✅ Блокировка SQL injection
- ✅ Блокировка XSS атак  
- ✅ Блокировка сканеров админки
- ✅ Rate limiting (лимиты запросов)
- ✅ Логирование всех событий

### 🎛️ **Ваши команды:**
```bash
python manage.py security_admin --stats      # Статистика
python manage.py security_admin --unblock-ip # Разблокировать  
python manage.py runserver                   # Запуск с защитой
```

### 📱 **В экстренной ситуации:**
1. `python manage.py security_admin --stats` - посмотреть что происходит
2. `python manage.py security_admin --clear-all` - очистить блокировки
3. Изменить лимиты в settings.py если нужно
4. `python manage.py runserver` - перезапустить

---

## 📞 **Поддержка и контакты**

Если возникли проблемы с системой безопасности:

1. **Сначала проверьте логи:** `tail -f logs/django.log`
2. **Посмотрите статистику:** `python manage.py security_admin --stats`
3. **При блокировке:** `python manage.py security_admin --unblock-ip ВАШ_IP`

**🛡️ Ваш православный портал под надежной защитой! Система работает сама, вам нужно только изредка проверять статистику.**

---

*Документация создана для православного портала "Добрые истории"*  
*Последнее обновление: Август 2025*
