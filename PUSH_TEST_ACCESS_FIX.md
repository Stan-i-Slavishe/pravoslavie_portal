# Изменения для скрытия кнопки тестирования push-уведомлений

## Проблема
Кнопка "Протестировать уведомления" была доступна всем пользователям, но возвращала "Access denied" для обычных пользователей на продакшен сервере.

## Решение
Скрыть кнопку от обычных пользователей и оставить только для администраторов.

## Внесенные изменения:

### 1. pwa/views.py - исправление логики доступа
```python
@require_http_methods(["GET"])
def push_test_page(request):
    """Тестовая страница для push-уведомлений (только для администраторов)"""
    # Доступ только для администраторов
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    context = {
        'total_subscriptions': 0,
        'active_subscriptions': 0, 
        'today_subscriptions': 0,
    }
    
    try:
        from .models import PushSubscription
        context['total_subscriptions'] = PushSubscription.objects.count()
        context['active_subscriptions'] = PushSubscription.objects.filter(is_active=True).count()
        context['today_subscriptions'] = PushSubscription.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
    except Exception as e:
        logger.error(f"Error getting push statistics: {e}")
    
    return render(request, 'pwa/push_test.html', context)
```

### 2. templates/pwa/notification_settings.html - условный показ кнопки
```html
<!-- Кнопка перехода к тестированию (только для администраторов) -->
{% if user.is_staff %}
<div class="text-center mt-4">
    <a href="{% url 'pwa:push_test' %}" class="btn btn-outline-info">
        <i class="fas fa-flask"></i> Протестировать уведомления
    </a>
    <small class="d-block text-muted mt-2">
        <i class="fas fa-user-shield"></i> Инструмент для администраторов
    </small>
</div>
{% endif %}
```

### 3. Добавление функции notification_settings_page (если отсутствует)
```python
@login_required
@require_http_methods(["GET"])
def notification_settings_page(request):
    """Страница настроек уведомлений"""
    try:
        # Получаем настройки пользователя
        user_settings, created = UserNotificationSettings.objects.get_or_create(user=request.user)
        
        # Получаем активные категории уведомлений
        active_categories = NotificationCategory.objects.filter(is_active=True)
        
        # Получаем подписки пользователя
        subscriptions = UserNotificationSubscription.objects.filter(user=request.user)
        subscriptions_dict = {sub.category.name: sub for sub in subscriptions}
        
        context = {
            'user_settings': user_settings,
            'active_categories': active_categories,
            'subscriptions': subscriptions_dict,
            'title': 'Настройки уведомлений',
            'show_admin_tools': request.user.is_staff
        }
        
        return render(request, 'pwa/notification_settings.html', context)
        
    except Exception as e:
        logger.error(f"Error loading notification settings page: {e}")
        context = {
            'title': 'Настройки уведомлений',
            'error': 'Произошла ошибка при загрузке настроек',
            'show_admin_tools': request.user.is_staff
        }
        return render(request, 'pwa/notification_settings.html', context)
```

## Результат изменений:

### Для обычных пользователей:
- Кнопка "Протестировать уведомления" не отображается
- Чистый интерфейс без технических инструментов
- Нет путаницы с недоступными функциями

### Для администраторов (is_staff=True):
- Кнопка "Протестировать уведомления" видна
- Подпись "Инструмент для администраторов" 
- Полный доступ к странице тестирования

### Безопасность:
- Доступ к странице тестирования только для администраторов
- Правильная обработка прав доступа на сервере
- Никаких технических ошибок для обычных пользователей

## Деплой изменений:

1. Загрузить изменения через git
2. Перезапустить gunicorn на сервере:
   ```bash
   systemctl restart gunicorn
   ```

## Проверка работы:

1. **Обычный пользователь**: кнопка тестирования не видна
2. **Администратор**: кнопка видна и работает
3. **Прямой доступ**: `/pwa/push/test/` доступен только администраторам

Теперь интерфейс станет более понятным для пользователей и сохранит функциональность для администраторов.
