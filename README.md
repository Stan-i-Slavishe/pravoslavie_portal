# 🏛️ Православный семейный портал "Dobrist"

![Status](https://img.shields.io/badge/status-production-success)
![Django](https://img.shields.io/badge/Django-5.2-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![OAuth](https://img.shields.io/badge/OAuth-Google%20%7C%20VK%20%7C%20Telegram-orange)

Семейный православный портал с терапевтическими сказками, книгами, аудио-контентом и интернет-магазином.

🌐 **Сайт:** [dobrist.com](https://dobrist.com)

---

## ✨ Основные возможности

### 📚 Контент
- **Терапевтические сказки** - фильтрация по возрасту и проблемам
- **Видео-рассказы** - YouTube интеграция с плейлистами
- **Электронные книги** - PDF reader с закладками
- **Аудио-контент** - плейлисты и аудиосказки

### 🛒 Интернет-магазин
- Корзина и оформление заказов
- Система промокодов и скидок
- Цифровые товары с защищенным скачиванием
- Личный кабинет с историей покупок

### 👤 Аутентификация
- **Регистрация** с reCAPTCHA защитой
- **OAuth 2.0** авторизация через:
  - 🔵 **Telegram** ⭐ (новое!)
  - 🔴 Google
  - 🔵 ВКонтакте
  - 📧 Mail.ru
  - 🟡 Яндекс

### 📱 PWA (Progressive Web App)
- Установка как нативное приложение
- Push-уведомления
- Офлайн режим
- Синхронизация между устройствами

### 🔍 SEO и аналитика
- Мета-теги и Schema.org разметка
- Sitemap и robots.txt
- Google Analytics & Yandex.Metrika
- Отслеживание активности пользователей

---

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- PostgreSQL 14+
- Redis 6+ (опционально, для кеширования)

### Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/pravoslavie_portal.git
cd pravoslavie_portal
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте базу данных:**
```bash
# Создайте PostgreSQL базу данных
createdb pravoslavie_portal_db

# Создайте пользователя
psql -c "CREATE USER pravoslavie_user WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE pravoslavie_portal_db TO pravoslavie_user;"
```

5. **Настройте переменные окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл
```

Пример `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=pravoslavie_portal_db
DB_USER=pravoslavie_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# OAuth keys
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_SECRET=your-google-secret
VK_CLIENT_ID=your-vk-client-id
VK_SECRET=your-vk-secret
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
```

6. **Выполните миграции:**
```bash
python manage.py migrate
```

7. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

8. **Соберите статические файлы:**
```bash
python manage.py collectstatic --noinput
```

9. **Запустите сервер:**
```bash
python manage.py runserver
```

Откройте: http://localhost:8000

---

## 🔵 Настройка Telegram OAuth

### Быстрая настройка (5 минут)

См. полную инструкцию: **[TELEGRAM_OAUTH_QUICKSTART.md](TELEGRAM_OAUTH_QUICKSTART.md)**

**Краткая версия:**

1. **Создайте бота** через [@BotFather](https://t.me/BotFather):
```
/newbot
Имя: Dobrist Login Bot
Username: dobrist_login_bot
```

2. **Установите домен:**
```
/setdomain
Выберите бота → https://dobrist.com
```

3. **Добавьте в Django Admin:**
- Откройте: `/admin/socialaccount/socialapp/add/`
- Provider: `Telegram`
- Client ID: `dobrist_login_bot`
- Secret key: токен от BotFather
- Sites: выберите ваш сайт

4. **Проверьте настройки:**
```bash
python check_telegram_oauth.bat
```

✅ Готово! Теперь пользователи могут войти через Telegram!

**Подробная документация:** [TELEGRAM_OAUTH_SETUP.md](TELEGRAM_OAUTH_SETUP.md)

---

## 🏗️ Структура проекта

```
pravoslavie_portal/
├── accounts/          # Пользователи и профили
├── analytics/         # Аналитика и метрики
├── audio/            # Аудио-контент
├── books/            # Электронные книги
├── core/             # Основная навигация
├── config/           # Настройки Django
├── fairy_tales/      # Терапевтические сказки ⭐
├── pwa/              # Progressive Web App
├── shop/             # Интернет-магазин
├── stories/          # Видео-рассказы
├── subscriptions/    # Премиум подписки
├── templates/        # HTML шаблоны
├── static/           # CSS, JS, изображения
├── media/            # Загружаемые файлы
└── manage.py
```

---

## 🔧 Конфигурация окружений

Проект поддерживает несколько окружений:

- **local** (по умолчанию) - локальная разработка
- **staging** - тестовый сервер
- **production** - продакшн сервер

Переключение через `.env`:
```env
DJANGO_ENV=production  # или local, staging
```

Файлы настроек:
- `config/settings_base.py` - базовые настройки
- `config/settings_local_postgresql.py` - локальная разработка
- `config/settings_production.py` - продакшн

---

## 📦 Основные зависимости

- **Django 5.2** - веб-фреймворк
- **PostgreSQL** - основная БД
- **Redis** - кеширование
- **Celery** - фоновые задачи
- **django-allauth** - OAuth аутентификация
- **Bootstrap 5** - UI фреймворк
- **Gunicorn** - WSGI сервер
- **Nginx** - веб-сервер (продакшн)

Полный список: [requirements.txt](requirements.txt)

---

## 📚 Документация

### Общая документация
- [Быстрый старт](QUICK_START.md)
- [Структура проекта](PROJECT_STRUCTURE.md)
- [План разработки](plan_updated.md)

### OAuth интеграции
- [Telegram OAuth - Быстрый старт](TELEGRAM_OAUTH_QUICKSTART.md) ⭐
- [Telegram OAuth - Полная инструкция](TELEGRAM_OAUTH_SETUP.md)
- [Google OAuth](GOOGLE_OAUTH_SETUP_GUIDE.md)
- [OAuth шпаргалка](OAUTH_CHEATSHEET.md)

### Функциональность
- [PWA реализация](PWA_IMPLEMENTATION_COMPLETE.md)
- [SEO интеграция](SEO_INTEGRATION_GUIDE.md)
- [Мониторинг](MONITORING_READY.md)
- [Безопасность](SECURITY_GUIDE.md)

### API интеграции
- [YouTube API](docs/api_integrations.md)
- [Платежные системы](docs/api_integrations.md)

---

## 🧪 Тестирование

Запуск тестов:
```bash
python manage.py test
```

Запуск с покрытием:
```bash
coverage run --source='.' manage.py test
coverage report
```

---

## 🚢 Деплой на продакшн

### Подготовка

1. **Обновите .env на сервере:**
```env
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=dobrist.com,www.dobrist.com
SECRET_KEY=your-production-secret-key
```

2. **Выполните миграции:**
```bash
python manage.py migrate
```

3. **Соберите статику:**
```bash
python manage.py collectstatic --noinput
```

4. **Перезапустите сервисы:**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Проверка деплоя
```bash
./check_deploy_ready.sh
```

**Подробнее:** [PRODUCTION_DEPLOY.md](PRODUCTION_DEPLOY.md)

---

## 🛠️ Полезные команды

### Разработка
```bash
# Запуск сервера разработки
python manage.py runserver

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сброс кеша
python manage.py clear_cache
```

### Проверки
```bash
# Проверка Telegram OAuth
python check_telegram_oauth.bat

# Проверка настроек OAuth
python check_oauth_status.py

# Проверка окружения
python check_environment.py

# Проверка готовности к деплою
./check_deploy_ready.sh
```

### Бэкапы
```bash
# Создать бэкап БД
python create_postgresql_backup.py

# Создать полный бэкап
./create_full_backup.sh

# Восстановить из бэкапа
python restore_from_backup.bat
```

---

## 🎨 Дизайн

### Цветовая палитра

```css
:root {
  --orthodox-blue: #2B5AA0;   /* Основной синий */
  --gold-accent: #D4AF37;     /* Золотой акцент */
  --child-pink: #FF6B9D;      /* Детский розовый */
  --warm-white: #FEFEFE;      /* Теплый белый */
  --soft-gray: #F8F9FA;       /* Мягкий серый */
}
```

Подробнее: [docs/ui_components.md](docs/ui_components.md)

---

## 📊 Статус проекта

**Текущая версия:** 1.0 (Production)  
**Готовность:** 94% до полного коммерческого запуска

### ✅ Завершено
- ✅ Все основные модули (Core, Stories, Books, Shop, etc.)
- ✅ OAuth аутентификация (Google, VK, Telegram, Mail.ru, Яндекс)
- ✅ Интернет-магазин с корзиной и заказами
- ✅ PWA с push-уведомлениями
- ✅ SEO оптимизация
- ✅ reCAPTCHA защита
- ✅ Продакшн сервер работает на dobrist.com

### 🔄 В разработке
- 🔄 Интеграция реальных платежных систем (YooKassa/Stripe)
- 🔄 Полнотекстовый поиск (Elasticsearch)
- 🔄 Telegram bot для уведомлений

Подробный статус: [plan_updated.md](plan_updated.md)

---

## 🤝 Вклад в проект

Если вы хотите внести свой вклад:

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📝 Лицензия

Этот проект является проприетарным ПО. Все права защищены.

---

## 📞 Контакты

**Веб-сайт:** [dobrist.com](https://dobrist.com)  
**Email:** admin@dobrist.com

---

## 🙏 Благодарности

- Django команде за отличный фреймворк
- Bootstrap за UI компоненты
- Всем контрибьюторам open-source библиотек

---

**Сделано с ❤️ для православных семей**
