# 📁 Конфигурация окружений

## 🎯 Принцип работы

Проект использует **3 четких окружения**:

### 🔧 `.env.local` - Локальная разработка
- SQLite база данных (по умолчанию)
- DEBUG=True
- Письма в консоль
- Тестовые API ключи
- Возможность переключения на PostgreSQL

### 🧪 `.env.staging` - Тестирование
- PostgreSQL (отдельная база!)
- DEBUG=False
- Полные настройки безопасности
- Тестовые API ключи
- Домен: staging.dobrist.com

### 🚀 `.env.production` - Продакшн
- PostgreSQL продакшена
- DEBUG=False
- Максимальная безопасность
- Реальные API ключи
- Домен: dobrist.com

## 🔄 Как переключаться между окружениями

### Windows:
```powershell
# Локальная разработка
$env:DJANGO_ENV = "local"

# Staging тестирование
$env:DJANGO_ENV = "staging"

# Продакшн
$env:DJANGO_ENV = "production"
```

### Linux/Mac:
```bash
# Локальная разработка
export DJANGO_ENV=local

# Staging тестирование
export DJANGO_ENV=staging

# Продакшн
export DJANGO_ENV=production
```

## ⚙️ Гибкие настройки .env.local

### SQLite (по умолчанию):
```env
USE_SQLITE=True
```

### PostgreSQL для тестирования:
```env
USE_SQLITE=False
DB_NAME=pravoslavie_portal_dev
DB_USER=postgres
DB_PASSWORD=your_password
```

## 🚨 Правила безопасности

1. **НИКОГДА** не коммитьте .env файлы в Git!
2. **ВСЕГДА** тестируйте на staging перед продакшеном
3. **ИСПОЛЬЗУЙТЕ** разные пароли для каждого окружения
4. **СОЗДАВАЙТЕ** backup перед изменениями

## 🛠️ Команды для проверки

```bash
# Проверить текущие настройки
python manage.py check

# Проверить настройки продакшена
python manage.py check --deploy

# Посмотреть какое окружение загружено
python manage.py shell -c "from django.conf import settings; print(f'Environment: {getattr(settings, \"ENVIRONMENT\", \"НЕ ОПРЕДЕЛЕН\")}');"
```