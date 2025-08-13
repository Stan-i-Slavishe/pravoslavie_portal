# 🚨 Быстрые команды безопасности

## ⚡ **Экстренные команды (копируй и вставляй)**

### 🆘 **Я заблокирован!**
```bash
# Разблокировать свой IP
python manage.py security_admin --unblock-ip 127.0.0.1
python manage.py security_admin --unblock-ip YOUR_IP_HERE

# Если не помогает - очистить все
python manage.py security_admin --clear-all
```

### 🔥 **Сайт под атакой!**
```bash
# Быстрая диагностика
python manage.py security_admin --stats
python manage.py security_admin --show-blocked
python manage.py security_admin --recent-attacks

# Экстренный режим
python manage.py security_admin --emergency-mode
```

### 🧹 **Очистить все блокировки**
```bash
# Осторожно! Очистит ВСЕ блокировки
python manage.py security_admin --clear-all

# Очистить только старые (безопаснее)
python manage.py security_admin --clear-old
```

### 📊 **Проверить статистику**
```bash
# Основная статистика
python manage.py security_admin --stats

# Детальная статистика
python manage.py security_admin --detailed-stats

# Топ атакующих
python manage.py security_admin --top-attackers
```

### 🛑 **Управление блокировками**
```bash
# Заблокировать IP
python manage.py security_admin --block-ip 192.168.1.100 --reason "Spam attack"

# Заблокировать диапазон
python manage.py security_admin --block-range 192.168.1.0/24

# Добавить в whitelist
python manage.py security_admin --whitelist-ip 192.168.1.50
```

---

## 🚨 **Экстренные ситуации**

### 😱 **Паника-режим (если совсем плохо)**
```bash
# 1. Остановить сервер
python manage.py runserver --stop

# 2. Отключить безопасность в settings.py
# Закомментировать SecurityMiddleware

# 3. Запустить без защиты
python manage.py runserver

# 4. Исправить проблему
# 5. Включить защиту обратно
```

### 🔥 **Массовая DDoS атака**
```bash
# Экстренное блокирование
python manage.py security_admin --emergency-mode
python manage.py security_admin --block-all-new
python manage.py security_admin --registered-only

# Анализ атаки
python manage.py security_admin --attack-analysis
```

### 🛡️ **Подозрительная активность**
```bash
# Мониторинг в реальном времени
tail -f logs/security.log
tail -f logs/django.log | grep SECURITY

# Анализ последних атак
python manage.py security_admin --recent-attacks --count 100
```

---

## 🔧 **Настройка и тестирование**

### ⚙️ **Изменить настройки налету**
```bash
# Ужесточить лимиты
python manage.py security_admin --set-rate-limit 50/hour

# Смягчить лимиты
python manage.py security_admin --set-rate-limit 200/hour

# Изменить время блокировки
python manage.py security_admin --set-block-duration 7200  # 2 часа
```

### 🧪 **Тестирование системы**
```bash
# Базовый тест
python test_security.py

# Полный тест
python test_security.py --full

# Тест производительности
python test_security.py --performance
```

---

## 📱 **Мониторинг через телефон**

### 📊 **Быстрая проверка по SSH**
```bash
# Подключиться к серверу
ssh user@your-server.com

# Быстрая статистика
python manage.py security_admin --stats --brief

# Проверить логи
tail -20 logs/security.log
```

### 🚨 **Экстренное отключение**
```bash
# Если нужно срочно отключить защиту
cp config/settings.py config/settings_backup.py
sed -i 's/SecurityMiddleware/#SecurityMiddleware/' config/settings.py
sudo systemctl restart django
```

---

## 🎯 **Специальные команды для православного портала**

### ⛪ **Защита религиозного контента**
```bash
# Включить фильтр религиозного контента
python manage.py security_admin --enable-religious-filter

# Проверить блокировки по религиозным причинам
python manage.py security_admin --religious-blocks
```

### 👨‍👩‍👧‍👦 **Семейная безопасность**
```bash
# Включить детский режим
python manage.py security_admin --family-mode

# Проверить безопасность сказок
python manage.py security_admin --check-fairy-tales
```

### 📚 **Защита контента**
```bash
# Сканировать комментарии
python manage.py security_admin --scan-comments

# Проверить загруженные файлы
python manage.py security_admin --scan-uploads
```

---

## ⏰ **Автоматизация**

### 🤖 **Cron задачи**
```bash
# Добавить в crontab:
# Проверка каждые 5 минут
*/5 * * * * /path/to/python /path/to/manage.py security_admin --auto-check

# Очистка старых блокировок раз в день
0 2 * * * /path/to/python /path/to/manage.py security_admin --clear-old

# Еженедельный отчет
0 9 * * 1 /path/to/python /path/to/manage.py security_admin --weekly-report
```

---

## 📋 **Чек-лист быстрых действий**

### ✅ **При проблемах (по порядку):**
1. [ ] `python manage.py security_admin --stats`
2. [ ] `python manage.py security_admin --show-blocked`
3. [ ] `tail -20 logs/security.log`
4. [ ] `python manage.py security_admin --unblock-ip YOUR_IP`
5. [ ] `python manage.py security_admin --clear-old`

### ✅ **При атаке (по порядку):**
1. [ ] `python manage.py security_admin --emergency-mode`
2. [ ] `python manage.py security_admin --recent-attacks`
3. [ ] `python manage.py security_admin --top-attackers`
4. [ ] `python manage.py security_admin --block-all-new`
5. [ ] Связаться с хостинг-провайдером

---

**🚨 Помни: В экстренной ситуации лучше отключить защиту и исправить проблему, чем оставить сайт недоступным!**

*Быстрые команды безопасности православного портала "Добрые истории"*  
*v1.0 | Август 2025*

### ✅ **Добавить в whitelist**
```bash
python manage.py security_admin --whitelist-ip 203.0.113.1
```

### 🧪 **Тест системы**
```bash
python test_security.py
```

---

## 📱 **Телефон команды поддержки**

1. Проверить статистику
2. Очистить блокировки если нужно  
3. Изменить лимиты в settings.py
4. Перезапустить сервер

**🚀 В 90% случаев помогает очистка блокировок!**
