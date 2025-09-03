# 🐳 Православный портал - Docker Infrastructure

## 🎯 Docker Setup Complete!

Ваш православный портал теперь полностью готов к работе в Docker контейнерах! 

### 📦 Что было создано:

#### 🏗️ **Основная инфраструктура:**
- **`Dockerfile`** - Production образ Django приложения
- **`Dockerfile.dev`** - Development образ с дополнительными инструментами
- **`docker-compose.yml`** - Production стек (Django + PostgreSQL + Redis + Nginx + Celery)
- **`docker-compose.dev.yml`** - Development стек с дополнительными сервисами

#### ⚙️ **Конфигурации:**
- **`docker/nginx/`** - Nginx конфигурации с SSL и оптимизацией
- **`docker/postgres/`** - PostgreSQL инициализация и настройки
- **`docker/redis/`** - Redis конфигурация для кеширования
- **`docker/ssl/`** - Директория для SSL сертификатов

#### 🔧 **Environment файлы:**
- **`.env.production`** - Production настройки
- **`.env.development`** - Development настройки

#### 📋 **Скрипты и утилиты:**
- **`scripts/setup-dev.bat`** - Windows скрипт для запуска development
- **`scripts/deploy-production.sh`** - Linux скрипт для production деплоя
- **`Makefile`** - Команды для управления Docker
- **`core/health_views.py`** - Health check эндпоинты

---

## 🚀 Быстрый старт

### 🛠️ Development (для разработки):

```bash
# Windows
scripts\setup-dev.bat

# Linux/Mac
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh

# Или с Makefile
make setup
```

### 🌐 Доступные сервисы (Development):
- **Django App:** http://localhost:8000
- **pgAdmin:** http://localhost:5050 (admin@pravoslavie-portal.local / admin123)
- **MailHog:** http://localhost:8025 (для тестирования email)
- **Redis:** localhost:6379

### 🚀 Production (на сервере):

```bash
# Подготовка
cp .env.production .env
# Отредактируйте .env с реальными значениями

# Запуск
make prod

# Или вручную
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📋 Полезные команды

### 🏗️ **Управление контейнерами:**
```bash
make dev          # Запуск development окружения
make prod         # Запуск production окружения  
make build        # Пересборка образов
make logs         # Просмотр логов
make stop         # Остановка всех контейнеров
make clean        # Очистка контейнеров и томов
```

### 🗄️ **База данных:**
```bash
make migrate      # Применение миграций
make backup       # Создание бэкапа БД
make restore      # Восстановление БД
make shell        # Django shell
```

### 👤 **Пользователи:**
```bash
make superuser    # Создание суперпользователя
```

### 🎨 **Статика:**
```bash
make collectstatic # Сборка статических файлов
```

### 🔍 **Мониторинг:**
```bash
make status       # Статус контейнеров
make health       # Проверка здоровья приложения
make stats        # Статистика использования ресурсов
```

---

## 🌍 Архитектура Docker стека

### 🚀 **Production стек:**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Nginx         │────│   Django Web     │────│   PostgreSQL    │
│   (Port 80/443) │    │   (Port 8000)    │    │   (Port 5432)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Celery Worker  │────│     Redis       │
                       │   (Background)   │    │   (Port 6379)   │
                       └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │   Celery Beat    │
                       │   (Scheduler)    │
                       └──────────────────┘
```

### 🛠️ **Development стек:**
Добавляется:
- **pgAdmin** (Port 5050) - Администрирование БД
- **MailHog** (Port 8025) - Тестирование email

---

## 🔧 Конфигурация

### 📋 **Обязательные настройки для production:**

Отредактируйте `.env.production`:

```bash
# 🔑 Security
SECRET_KEY=your_super_secret_django_key_here_generate_new_one
POSTGRES_PASSWORD=your_secure_postgres_password_here
ALLOWED_HOSTS=pravoslavie-portal.ru,www.pravoslavie-portal.ru

# 📧 Email
EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_email_password

# 🎬 APIs
YOUTUBE_API_KEY=your_youtube_api_key_here
YOOKASSA_SHOP_ID=your_yookassa_shop_id
YOOKASSA_SECRET_KEY=your_yookassa_secret_key
```

### 🔐 **Генерация секретных ключей:**
```bash
make secrets
```

---

## 📁 Структура томов Docker

### 💾 **Постоянные данные:**
```
/var/lib/docker/volumes/
├── pravoslavie_postgres_data/     # База данных PostgreSQL
├── pravoslavie_redis_data/        # Cache Redis
├── pravoslavie_media_files/       # Загруженные файлы
└── pravoslavie_static_files/      # Статические файлы
```

### 📂 **Монтированные директории:**
```
./logs/        -> /app/logs/          # Логи приложения
./media/       -> /app/media/         # Медиа файлы (в dev)
./docker/ssl/  -> /etc/ssl/certs/     # SSL сертификаты
```

---

## 🚀 Деплой на сервер

### 1️⃣ **Подготовка сервера:**
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2️⃣ **Деплой проекта:**
```bash
# Загрузка на сервер
git clone https://github.com/yourusername/pravoslavie-portal.git /opt/pravoslavie-portal
cd /opt/pravoslavie-portal

# Настройка окружения
cp .env.production .env
nano .env  # Отредактируйте настройки

# Первый запуск
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

### 3️⃣ **SSL сертификаты (Let's Encrypt):**
```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --webroot -w /opt/pravoslavie-portal/docker/ssl -d pravoslavie-portal.ru -d www.pravoslavie-portal.ru

# Копирование сертификатов
sudo cp /etc/letsencrypt/live/pravoslavie-portal.ru/fullchain.pem docker/ssl/pravoslavie-portal.crt
sudo cp /etc/letsencrypt/live/pravoslavie-portal.ru/privkey.pem docker/ssl/pravoslavie-portal.key

# Перезапуск Nginx
docker-compose restart nginx
```

---

## 🔍 Мониторинг и отладка

### 🩺 **Health Check эндпоинты:**
- **Full health:** `GET /health/` - Полная проверка системы
- **Readiness:** `GET /health/ready/` - Готовность к приему трафика  
- **Liveness:** `GET /health/live/` - Базовая проверка жизнеспособности

### 📊 **Просмотр логов:**
```bash
# Все логи
make logs

# Конкретный сервис
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f nginx
```

### 🔧 **Отладка контейнеров:**
```bash
# Подключение к контейнеру
docker-compose exec web bash
docker-compose exec postgres psql -U pravoslavie_user -d pravoslavie_portal_db

# Перезапуск сервиса
docker-compose restart web
```

---

## 🔄 Обновление и бэкапы

### 📈 **Обновление кода:**
```bash
make update
# Или:
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

### 💾 **Автоматические бэкапы:**
```bash
# Создать cron job для ежедневного бэкапа
echo "0 2 * * * cd /opt/pravoslavie-portal && make backup" | sudo crontab -
```

### 🔄 **Восстановление:**
```bash
# Восстановление из бэкапа
make restore

# Или вручную
docker-compose exec -T postgres psql -U pravoslavie_user -d pravoslavie_portal_db < backups/backup_20240901_120000.sql
```

---

## ⚠️ Важные примечания

### 🔒 **Безопасность:**
- Всегда меняйте дефолтные пароли в `.env.production`
- Используйте HTTPS в production
- Регулярно обновляйте Docker образы
- Ограничьте доступ к админ панели по IP

### 📊 **Производительность:**
- Для высоких нагрузок увеличьте количество Gunicorn workers
- Настройте горизонтальное масштабирование через Docker Swarm
- Используйте внешний Redis/PostgreSQL для критических нагрузок

### 🔧 **Поддержка:**
- Логи находятся в `./logs/django.log`
- Health check доступен по `/health/`
- Используйте `make help` для списка команд

---

## 🎉 Готово!

✅ **Ваш православный портал готов к запуску в Docker!**

**Следующие шаги:**
1. Запустите development окружение: `make setup`
2. Проверьте работу всех компонентов
3. Настройте production переменные в `.env.production` 
4. Задеплойте на сервер используя `scripts/deploy-production.sh`

🚀 **Этап 1.3 "Создание Docker инфраструктуры" завершен!**

Теперь можно переходить к **Этапу 2.1 - Локальная сборка Docker-стека**.
