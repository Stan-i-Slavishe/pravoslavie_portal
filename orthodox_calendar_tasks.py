#!/usr/bin/env python
"""
Celery задачи для православного календаря
"""

from celery import shared_task
from datetime import datetime, date, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@shared_task
def send_orthodox_calendar_notifications():
    """Отправка уведомлений о православных событиях"""
    
    try:
        from orthodox_calendar_service import OrthodoxCalendarService
        from pwa.models import UserNotificationSettings, UserNotificationSubscription, NotificationCategory
        
        print("📅 Запуск задачи православного календаря...")
        
        # Получаем события на сегодня и завтра
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        calendar_service = OrthodoxCalendarService()
        
        # События на сегодня
        today_events = calendar_service.get_events_for_date(today)
        tomorrow_events = calendar_service.get_events_for_date(tomorrow)
        
        if not today_events and not tomorrow_events:
            print("📖 Нет православных событий на сегодня и завтра")
            return
        
        # Получаем категорию православного календаря
        try:
            calendar_category = NotificationCategory.objects.get(name='orthodox_calendar')
        except NotificationCategory.DoesNotExist:
            print("❌ Категория 'orthodox_calendar' не найдена")
            return
        
        # Получаем пользователей, подписанных на православный календарь
        subscriptions = UserNotificationSubscription.objects.filter(
            category=calendar_category,
            enabled=True
        ).select_related('user', 'user__notification_settings')
        
        notifications_sent = 0
        
        for subscription in subscriptions:
            user = subscription.user
            user_settings = getattr(user, 'notification_settings', None)
            
            # Проверяем, включены ли уведомления
            if not user_settings or not user_settings.notifications_enabled:
                continue
            
            # Проверяем тихие часы
            if user_settings.is_quiet_time_now():
                continue
            
            # Проверяем день недели
            current_weekday = timezone.now().weekday()
            if not user_settings.get_weekday_setting(current_weekday):
                continue
            
            # Формируем сообщение
            message_parts = []
            
            if today_events:
                message_parts.append("🕊️ Сегодня:")
                for event in today_events:
                    message_parts.append(f"• {event.get('title', 'Православное событие')}")
            
            if tomorrow_events:
                if message_parts:
                    message_parts.append("")
                message_parts.append("📅 Завтра:")
                for event in tomorrow_events:
                    message_parts.append(f"• {event.get('title', 'Православное событие')}")
            
            if message_parts:
                message = "\n".join(message_parts)
                title = "⛪ Православный календарь"
                
                # Отправляем уведомление
                success = send_push_notification_to_user(
                    user=user,
                    title=title,
                    message=message,
                    category='orthodox_calendar'
                )
                
                if success:
                    notifications_sent += 1
                    print(f"✅ Уведомление отправлено: {user.username}")
                else:
                    print(f"❌ Ошибка отправки: {user.username}")
        
        print(f"📊 Отправлено {notifications_sent} уведомлений о православном календаре")
        return notifications_sent
        
    except Exception as e:
        print(f"❌ Ошибка в задаче православного календаря: {e}")
        return 0

@shared_task  
def send_bedtime_story_reminders():
    """Напоминания о сказках на ночь"""
    
    try:
        from pwa.models import UserNotificationSettings, UserNotificationSubscription, NotificationCategory
        
        print("🌙 Запуск напоминаний о сказках на ночь...")
        
        # Получаем категорию сказок на ночь
        try:
            bedtime_category = NotificationCategory.objects.get(name='bedtime_stories')
        except NotificationCategory.DoesNotExist:
            print("❌ Категория 'bedtime_stories' не найдена")
            return
        
        # Получаем пользователей с включенным детским режимом
        subscriptions = UserNotificationSubscription.objects.filter(
            category=bedtime_category,
            enabled=True,
            user__notification_settings__child_mode=True
        ).select_related('user', 'user__notification_settings')
        
        notifications_sent = 0
        current_time = timezone.now().time()
        
        for subscription in subscriptions:
            user = subscription.user
            user_settings = user.notification_settings
            
            # Проверяем время сказки (±30 минут)
            bedtime = user_settings.child_bedtime
            
            # Простая проверка времени (можно улучшить)
            time_diff = abs(
                (current_time.hour * 60 + current_time.minute) - 
                (bedtime.hour * 60 + bedtime.minute)
            )
            
            if time_diff <= 30:  # В пределах 30 минут
                title = "🌙 Время сказки!"
                message = "Пора читать добрую сказку перед сном. Заходите в раздел терапевтических сказок!"
                
                success = send_push_notification_to_user(
                    user=user,
                    title=title,
                    message=message,
                    category='bedtime_stories'
                )
                
                if success:
                    notifications_sent += 1
                    print(f"✅ Напоминание отправлено: {user.username}")
        
        print(f"📊 Отправлено {notifications_sent} напоминаний о сказках")
        return notifications_sent
        
    except Exception as e:
        print(f"❌ Ошибка в напоминаниях о сказках: {e}")
        return 0

def send_push_notification_to_user(user, title, message, category):
    """Отправка push-уведомления конкретному пользователю"""
    
    try:
        from pwa.models import PushSubscription
        
        # Получаем активные push-подписки пользователя
        subscriptions = PushSubscription.objects.filter(
            user=user,
            is_active=True
        )
        
        if not subscriptions.exists():
            return False
        
        # Здесь будет реальная отправка push-уведомлений
        # Пока что имитируем успешную отправку
        print(f"📱 PUSH: {title} → {user.username}")
        print(f"💬 {message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка отправки push: {e}")
        return False

# Настройка периодических задач для celery beat
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'orthodox-calendar-morning': {
        'task': 'orthodox_calendar_tasks.send_orthodox_calendar_notifications',
        'schedule': crontab(hour=8, minute=0),  # Каждый день в 8:00
    },
    'bedtime-stories-evening': {
        'task': 'orthodox_calendar_tasks.send_bedtime_story_reminders', 
        'schedule': crontab(hour=20, minute=0),  # Каждый день в 20:00
    },
}

if __name__ == '__main__':
    print("🚀 Тестирование задач...")
    print("📅 Тест православного календаря:")
    send_orthodox_calendar_notifications()
    print("\n🌙 Тест напоминаний о сказках:")
    send_bedtime_story_reminders()
