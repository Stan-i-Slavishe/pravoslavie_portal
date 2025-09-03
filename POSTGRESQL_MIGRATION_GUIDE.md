# 🐘 Перевод на PostgreSQL - Православный портал

## 🎯 Цель
Перевод проекта с SQLite на PostgreSQL для повышения стабильности и подготовки к Docker контейнеризации.

## 🚀 Быстрый старт

### Вариант 1: Автоматический (рекомендуется)
```cmd
# Запустите мастер-скрипт
postgresql_master.bat
```

### Вариант 2: Пошаговый
```cmd
# 1. Установка PostgreSQL
setup_postgresql.bat

# 2. Миграция данных
migrate_to_postgresql.bat  

# 3. Проверка результата
python check_migration.py

# 4. Создание бэкапа
create_postgresql_backup.bat
```

## 📋 Что делают скрипты

### 🔧 `setup_postgresql.bat`
- Помогает установить PostgreSQL
- Создает базу данных `pravoslavie_local_db`  
- Создает пользователя `pravoslavie_user`
- Настраивает права доступа

### 🔄 `migrate_to_postgresql.bat`
- Экспортирует данные из SQLite
- Обновляет настройки Django для PostgreSQL
- Применяет миграции к новой БД
- Импортирует все данные
- Создает суперпользователя
- Запускает сайт для проверки

### ✅ `check_migration.py`
- Проверяет подключение к PostgreSQL
- Подсчитывает записи во всех таблицах
- Проверяет ключевые данные
- Показывает статистику по медиа-файлам

### 💾 `create_postgresql_backup.bat`
- Создает SQL дамп БД
- Создает сжатый дамп для хранения  
- Копирует медиа-файлы
- Создает информационный файл

### 🎛️ `postgresql_master.bat`
- Интерактивное меню для всех операций
- Показывает статус системы
- Управляет всем процессом миграции

## ⚙️ Настройки

После миграции в `.env.local` будут обновлены настройки:
```env
# Переключение на PostgreSQL
USE_SQLITE=False

# Настройки подключения
DB_NAME=pravoslavie_local_db
DB_USER=pravoslavie_user  
DB_PASSWORD=local_strong_password_2024
DB_HOST=localhost
DB_PORT=5432
```

## 🔍 Проверка результата

После миграции проверьте:
1. 🌐 Сайт работает: http://127.0.0.1:8000/
2. 👑 Админка доступна: http://127.0.0.1:8000/admin/
3. 🎬 Рассказы отображаются
4. 📚 Книги доступны
5. 🛒 Магазин функционирует
6. 🧚 Терапевтические сказки работают

## 📁 Структура бэкапов

```
backups/
├── sqlite_full_YYYYMMDD_HHMM.json    # Полный экспорт SQLite
├── sqlite_clean_YYYYMMDD_HHMM.json   # Чистый экспорт SQLite  
└── postgresql_YYYY-MM-DD_HH-MM-SS/   # Бэкап PostgreSQL
    ├── database.sql                   # SQL дамп
    ├── database.dump                  # Сжатый дамп
    ├── media/                         # Медиа-файлы
    └── backup_info.txt               # Информация о бэкапе
```

## 🛠️ Устранение проблем

### PostgreSQL не подключается
```cmd
# Проверьте что PostgreSQL запущен
net start postgresql-x64-15

# Проверьте настройки в .env.local
# Убедитесь что пароль правильный
```

### Ошибки импорта данных
```cmd
# Попробуйте импорт с подробным выводом
python manage.py loaddata backups\sqlite_clean_*.json --verbosity=2

# Или импортируйте по частям
python manage.py dumpdata stories -o stories_backup.json
python manage.py loaddata stories_backup.json
```

### Проблемы с кодировкой
```sql
-- При создании БД укажите кодировку
CREATE DATABASE pravoslavie_local_db 
  WITH ENCODING 'UTF8' 
  LC_COLLATE='Russian_Russia.1251' 
  LC_CTYPE='Russian_Russia.1251';
```

## ✅ Контрольный список

- [ ] PostgreSQL установлен и запущен
- [ ] База данных `pravoslavie_local_db` создана
- [ ] Пользователь `pravoslavie_user` создан
- [ ] Данные из SQLite экспортированы
- [ ] Настройки `.env.local` обновлены  
- [ ] Django подключается к PostgreSQL
- [ ] Миграции применены
- [ ] Данные импортированы корректно
- [ ] Суперпользователь создан
- [ ] Сайт работает на PostgreSQL
- [ ] Создан бэкап PostgreSQL

## 🚀 Следующие шаги

После успешного перевода на PostgreSQL:
1. 🐳 **Docker контейнеризация** - упаковка в контейнеры
2. 🌐 **Деплой на сервер** - размещение на продакшн
3. 🔄 **CI/CD настройка** - автоматизация деплоя

## 💡 Полезные команды

```cmd
# Подключение к PostgreSQL
psql -U pravoslavie_user -d pravoslavie_local_db

# Просмотр таблиц
\dt

# Создание дампа
pg_dump -U pravoslavie_user -d pravoslavie_local_db -f backup.sql

# Восстановление из дампа  
psql -U pravoslavie_user -d pravoslavie_local_db -f backup.sql

# Запуск Django на PostgreSQL
python manage.py runserver

# Проверка подключения Django к БД
python manage.py dbshell
```

---

**🎉 Успешная миграция на PostgreSQL означает стабильную основу для дальнейшего развития проекта!**