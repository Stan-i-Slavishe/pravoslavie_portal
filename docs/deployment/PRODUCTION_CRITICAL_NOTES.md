# 🚀 КРИТИЧЕСКИ ВАЖНЫЕ ЗАМЕТКИ ДЛЯ ПРОДАКШЕН ДЕПЛОЯ

## ⚠️ НЕ ТРОГАТЬ БЕЗ ПОНИМАНИЯ КОНТЕКСТА!

### 🗄️ Настройки базы данных (settings.py строки ~100-120)

```python
# Для продакшена можно добавить пул соединений (только для PostgreSQL)
if not config('DEBUG', default=True, cast=bool):
    # Добавляем настройки только если используется PostgreSQL
    if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        DATABASES['default']['CONN_MAX_AGE'] = 60
        # Инициализируем OPTIONS если его нет
        if 'OPTIONS' not in DATABASES['default']:
            DATABASES['default']['OPTIONS'] = {}
        DATABASES['default']['OPTIONS'].update({
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        })
    elif DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        # Для SQLite добавляем только базовые настройки
        DATABASES['default']['CONN_MAX_AGE'] = 60
```

**ИСТОРИЯ ПРОБЛЕМЫ:**
- 07.02.2025: После Git отката возникла ошибка `KeyError: 'OPTIONS'`
- Причина: код пытался обновить несуществующий ключ OPTIONS
- Решение: добавили проверку существования ключа
- 07.02.2025: Вторая ошибка `'MAX_CONNS' is an invalid keyword argument`
- Причина: SQLite не поддерживает параметры пула соединений PostgreSQL
- Решение: добавили проверку типа БД

**ВАЖНО:**
- MAX_CONNS и MIN_CONNS работают ТОЛЬКО с PostgreSQL
- SQLite поддерживает только CONN_MAX_AGE
- НЕ упрощать эту логику без тестирования!

### 🔧 Переменные окружения

**ДЛЯ РАЗРАБОТКИ (.env):**
```env
DEBUG=True  # Подробные ошибки для отладки
DB_ENGINE=django.db.backends.sqlite3
```

**ДЛЯ ПРОДАКШЕНА (.env.production):**
```env
DEBUG=False  # Скрытие ошибок от пользователей
DB_ENGINE=django.db.backends.postgresql
DATABASE_URL=postgresql://user:pass@localhost:5432/pravoslavie_db
```

### 🐛 Типичные ошибки при деплое

1. **Забыли переключить .env файл**
   - Симптом: SQLite ошибки на продакшене
   - Решение: проверить DATABASE_URL

2. **OPTIONS ключ отсутствует**
   - Симптом: KeyError: 'OPTIONS'
   - Решение: код уже исправлен, проверка добавлена

3. **Неправильный ENGINE для настроек пула**
   - Симптом: 'MAX_CONNS' is an invalid keyword argument
   - Решение: код уже исправлен, проверка типа БД добавлена

### 📋 Чеклист перед деплоем

- [ ] Переключить на .env.production
- [ ] Проверить DATABASE_URL
- [ ] Убедиться что PostgreSQL запущен
- [ ] Выполнить миграции
- [ ] Собрать статические файлы
- [ ] Протестировать подключение к БД

### 🔒 Безопасность

- Никогда не коммитить .env файлы в Git
- Использовать разные SECRET_KEY для разработки и продакшена
- Проверить ALLOWED_HOSTS для продакшена

---

**Создано:** 07.02.2025  
**Последнее обновление:** 07.02.2025  
**Статус:** Критически важно для стабильности