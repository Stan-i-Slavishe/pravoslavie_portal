# Окончательное решение проблемы неактивных настроек

## Выполните команды по порядку:

### 1. Диагностика проблемы:
```bash
python diagnose_settings.py
```

### 2. Принудительное исправление:
```bash
python force_fix_admin.py
```

### 3. Если нужен суперпользователь:
```bash
python manage.py createsuperuser --settings=config.settings_minimal
```

### 4. Запуск сервера:
```bash
python manage.py runserver --settings=config.settings_minimal
```

### 5. Если всё ещё не работает - альтернативный способ:

Удалите базу данных и пересоздайте:
```bash
del db.sqlite3
python manage.py migrate --settings=config.settings_minimal
python manage.py createsuperuser --settings=config.settings_minimal
python force_fix_admin.py
python manage.py runserver --settings=config.settings_minimal
```

## Проверка результата:
1. Откройте http://127.0.0.1:8000/admin/
2. Войдите под админом
3. Нажмите на "Настройки сайта" - должно открыться
4. Если всё ещё серое - обновите страницу (Ctrl+F5)

## Если проблема в правах доступа:
Проверьте, что вы вошли как суперпользователь (is_superuser=True).

Раздел может быть неактивным если:
- Нет записи в базе данных ✅ (исправлено)
- Нет прав у пользователя ❓ (проверьте)
- Ошибка в admin.py ✅ (исправлено)
- Проблемы с миграциями ✅ (исправлено)
