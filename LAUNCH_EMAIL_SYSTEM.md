# 🎯 ЗАПУСК EMAIL СИСТЕМЫ АНАЛИТИКИ

## ✅ Что готово:

### 📧 Email система
- Уведомления админу о кликах на покупку
- Подписка пользователей на уведомления  
- Еженедельные отчеты
- Management команды
- Красивые HTML шаблоны

### 🛠️ Код готов:
- ✅ Модели обновлены (с полями для email)
- ✅ Views с интеграцией email
- ✅ URL маршруты настроены
- ✅ Шаблоны созданы
- ✅ Админка обновлена
- ✅ Команды управления готовы

## 🚀 Шаги для запуска:

### 1. Создайте миграции
```bash
# Запустите этот файл
create_analytics_migrations.bat
```

Или вручную:
```bash
python manage.py makemigrations analytics
python manage.py migrate
```

### 2. Протестируйте систему
```bash
python test_email_system.py
```

### 3. Проверьте админку
- Зайдите в `/admin/analytics/`
- Убедитесь, что все модели отображаются

### 4. Настройте email для продакшена
В `.env` файле:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL_LIST=admin@pravoslavie-portal.ru
```

### 5. Добавьте форму подписки на сайт

В любой шаблон добавьте:
```html
<!-- Полная форма -->
<a href="/analytics/subscribe/" class="btn btn-primary">
    🔔 Подписаться на уведомления
</a>

<!-- Быстрый виджет -->
{% include 'analytics/widgets/subscribe_button.html' %}
<button onclick="showSubscribePopup('fairy_tales')">
    Уведомить о запуске
</button>
```

### 6. Настройте кнопки "Купить" 

На страницах книг/сказок добавьте onclick:
```html
<button onclick="trackPurchaseIntent('fairy_tale', 1, 'buy')">
    Купить сказку
</button>
```

## 📊 Использование:

### Просмотр аналитики:
- `/analytics/dashboard/` - дашборд аналитики
- `/analytics/email-campaigns/` - управление email

### Еженедельные отчеты:
```bash
python manage.py send_weekly_report
```

### Запуск платежей (через месяц):
```bash
python manage.py send_payment_launch
```

## 🎯 Что получится:

1. **📧 Мгновенные уведомления** админу о каждом клике "Купить"
2. **📋 База подписчиков** с email адресами заинтересованных
3. **📊 Еженедельная аналитика** с трендами и рекомендациями
4. **🚀 Готовая система** для запуска платежей

**Система полностью готова для сбора аналитики в течение месяца!** 🎉

## 🆘 При проблемах:

1. **Ошибки миграций** - проверьте модели в `analytics/models.py`
2. **Email не отправляются** - проверьте настройки в `.env`
3. **Админка не работает** - проверьте `analytics/admin.py`

**Все файлы созданы и готовы к использованию!** ✅
