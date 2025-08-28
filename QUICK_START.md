# 🚀 Православный портал - Быстрый старт

## 🎯 **Что было сделано:**

✅ Настроены отдельные окружения для разработки и продакшена  
✅ Созданы автоматические скрипты для запуска  
✅ Разделены настройки безопасности  
✅ Подготовлены файлы для деплоя  

## 🔧 **Локальная разработка (запуск одной командой):**

### Windows:
```cmd
run_local.bat
```

### Linux/Mac:
```bash
chmod +x run_local.sh
./run_local.sh
```

**Это автоматически:**
- ✅ Настроит локальные переменные окружения
- ✅ Активирует виртуальное окружение  
- ✅ Установит зависимости
- ✅ Применит миграции
- ✅ Соберет статику
- ✅ Создаст суперпользователя (admin/admin123)
- ✅ Запустит сервер на http://localhost:8000

## 🚀 **Деплой на продакшен:**

На продакшен сервере:
```bash
# Сделать скрипт исполняемым (один раз)
chmod +x deploy_production.sh

# Деплой
sudo ./deploy_production.sh
```

**Это автоматически:**
- ✅ Создаст бэкап текущей версии
- ✅ Обновит код из Git
- ✅ Применит продакшен настройки
- ✅ Обновит базу данных
- ✅ Соберет статику
- ✅ Обновит PWA (Service Worker)
- ✅ Проверит иконки
- ✅ Перезапустит сервисы
- ✅ Проверит доступность сайта

## ⚙️ **Настройка переменных окружения:**

### Локальная разработка:
Файл `.env.local` уже настроен с тестовыми значениями.

### Продакшен:
Отредактируйте `.env.production` на сервере:
```env
SECRET_KEY=ваш-супер-секретный-ключ
DB_PASSWORD=ваш-пароль-от-бд  
EMAIL_HOST_USER=ваша-почта@yandex.ru
EMAIL_HOST_PASSWORD=пароль-от-почты
YOUTUBE_API_KEY=ваш-ключ-youtube
YOOKASSA_SHOP_ID=ваш-магазин-id
YOOKASSA_SECRET_KEY=ваш-секретный-ключ
```

## 🔄 **Рабочий процесс:**

1. **Разработка:** `run_local.bat` → работаете локально
2. **Коммит:** `git add . && git commit -m "..." && git push`  
3. **Деплой:** `sudo ./deploy_production.sh` на сервере
4. **Проверка:** https://dobrist.com

## 📁 **Структура проекта:**

```
📂 pravoslavie_portal/
├── 📁 config/                  # Настройки Django
│   ├── settings.py            # Автовыбор окружения  
│   ├── settings_base.py       # Общие настройки
│   ├── settings_local.py      # Локальная разработка
│   └── settings_production.py # Продакшен
├── 📁 core/                   # Основное приложение
├── 📁 stories/                # Видео-рассказы
├── 📁 fairy_tales/            # Терапевтические сказки  
├── 📁 books/                  # Книги
├── 📁 shop/                   # Интернет-магазин
├── 📁 accounts/               # Пользователи
├── 📁 static/                 # Статические файлы
├── 📁 templates/              # HTML шаблоны
├── .env.local                # Настройки разработки
├── .env.production           # Настройки продакшена (не в Git!)
├── run_local.bat             # Запуск разработки (Windows)
├── run_local.sh              # Запуск разработки (Linux/Mac)  
└── deploy_production.sh      # Деплой на продакшен
```

## 🛠️ **Полезные команды:**

### Разработка:
```bash
# Создание миграций
python manage.py makemigrations

# Создание суперпользователя
python manage.py createsuperuser

# Тестирование
python manage.py test

# Shell Django
python manage.py shell
```

### Продакшен:
```bash
# Логи Django
journalctl -u dobrist -f

# Логи Nginx  
tail -f /var/log/nginx/error.log

# Статус сервисов
systemctl status dobrist nginx

# Перезапуск
sudo systemctl restart dobrist nginx
```

## 📞 **Поддержка:**

### Проверить окружение:
```python
python manage.py shell
>>> from django.conf import settings  
>>> print("DEBUG:", settings.DEBUG)
>>> print("DB:", settings.DATABASES['default']['NAME'])
```

### Если что-то не работает:
1. 🔍 Проверьте логи: `journalctl -u dobrist -n 20`
2. 🔧 Перезапустите: `sudo systemctl restart dobrist nginx`  
3. 🗄️ Проверьте БД: `python manage.py migrate --check`
4. 📁 Проверьте статику: `ls -la staticfiles/`

## 🎉 **Готово!**

Теперь у вас есть полностью настроенная среда разработки:
- 🔧 Локальный сервер для разработки
- 🚀 Автоматический деплой на продакшен  
- 🔐 Безопасное разделение настроек
- 📱 Готовый PWA функционал
- 🛒 Полнофункциональный интернет-магазин
- 🧚 Уникальные терапевтические сказки

**Используйте `run_local.bat` для разработки и `deploy_production.sh` для обновления сайта!** 🎊
