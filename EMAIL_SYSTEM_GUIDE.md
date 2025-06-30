# 📧 Email система аналитики - Руководство

## 🎯 Что реализовано

### ✅ 1. Уведомления админу о кликах на покупку
- **Автоматическая отправка** email при каждом новом клике на "Купить"
- **Подробная информация**: контент, пользователь, время, IP, страница
- **HTML и текстовые версии** писем
- **Защита от спама**: только новые клики, не повторы

### ✅ 2. Система подписок на уведомления
- **Форма подписки** `/analytics/subscribe/`
- **AJAX виджет** для быстрой подписки (можно встроить везде)
- **Подтверждение подписки** email
- **Управление подписками** (отписка)

### ✅ 3. Еженедельные отчеты
- **Автоматическая генерация** статистики за неделю
- **Отправка админам и подписчикам**
- **Красивые HTML шаблоны** с графиками и анализом
- **Management команды** для автоматизации

## 🛠️ Настройка

### 1. Обновите модели
```bash
python manage.py makemigrations analytics
python manage.py migrate
```

### 2. Настройте email в .env
```env
# Для разработки (консоль)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Для продакшена (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@pravoslavie-portal.ru

# Администраторы для уведомлений
ADMIN_EMAIL_LIST=admin@pravoslavie-portal.ru,owner@pravoslavie-portal.ru
```

### 3. Тестирование
```bash
python test_email_system.py
```

## 📝 Использование

### Формы подписки

**Полная форма:**
```html
<a href="/analytics/subscribe/" class="btn btn-primary">
    🔔 Подписаться на уведомления
</a>
```

**Быстрый виджет:**
```html
{% include 'analytics/widgets/subscribe_button.html' %}

<!-- Кнопка для вызова попапа -->
<button onclick="showSubscribePopup('fairy_tales')">
    Уведомить о запуске
</button>
```

### Management команды

**Еженедельный отчет:**
```bash
# Создать и отправить отчет за прошлую неделю
python manage.py send_weekly_report

# Отчет за конкретную неделю
python manage.py send_weekly_report --week-start 2024-01-15

# Принудительная отправка
python manage.py send_weekly_report --force
```

**Уведомление о запуске платежей:**
```bash
# Сухой запуск (посмотреть количество)
python manage.py send_payment_launch --dry-run

# Реальная отправка всем подписчикам
python manage.py send_payment_launch
```

### Админ панель

**Управление подписками:**
- `/admin/analytics/emailsubscription/`
- Просмотр, редактирование, экспорт

**Управление кампаниями:**
- `/analytics/email-campaigns/` (только для staff)
- Статистика, отправка, управление

**Дашборд аналитики:**
- `/analytics/dashboard/` (только для staff)
- Полная статистика кликов и подписок

## 🚀 Автоматизация для продакшена

### Cron задачи
```bash
# Еженедельные отчеты каждый понедельник в 9:00
0 9 * * 1 cd /path/to/project && python manage.py send_weekly_report

# Проверка неотправленных уведомлений каждый час
0 * * * * cd /path/to/project && python manage.py check_pending_notifications
```

### Celery задачи (опционально)
```python
# В будущем можно добавить асинхронную отправку
from celery import shared_task

@shared_task
def send_email_notification_async(intent_id):
    # Асинхронная отправка уведомлений
    pass
```

## 📊 Мониторинг

### Логи
- Все email операции логируются
- Ошибки отправки не ломают основной функционал
- Детальная информация об отправленных письмах

### Статистика в админке
- Количество отправленных писем на подписчика
- Даты последних отправок
- Статус доставки отчетов

## 🎯 Результат

После настройки вы получите:

1. **📧 Мгновенные уведомления** админу о каждом интересе к покупке
2. **📋 База заинтересованных** пользователей с их email
3. **📊 Еженедельную аналитику** с трендами и инсайтами
4. **🚀 Готовность к запуску** платежей с уведомлением всех подписчиков

**Система полностью готова для месячного сбора аналитики!** 🎉

## 🔄 Следующие шаги

1. **Запустить сайт** в аналитическом режиме
2. **Собирать данные** в течение месяца
3. **Анализировать еженедельные отчеты**
4. **Принять решение** о запуске платежей на основе данных
5. **Уведомить всех подписчиков** командой `send_payment_launch`
