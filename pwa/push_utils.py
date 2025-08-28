# Push-уведомления utils

from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

def send_push_notification(subscription_data, title, body, url="/", icon=None):
    """
    Отправляет push-уведомление конкретному пользователю
    """
    try:
        from pywebpush import webpush, WebPushException
        
        if not settings.VAPID_PRIVATE_KEY or not settings.VAPID_PUBLIC_KEY:
            logger.warning("VAPID ключи не настроены. Push-уведомления отключены.")
            return False
        
        # Подготавливаем данные уведомления
        notification_data = {
            "title": title,
            "body": body,
            "icon": icon or "/static/icons/icon-192x192.png",
            "badge": "/static/icons/icon-72x72.png",
            "url": url,
            "tag": f"notification_{hash(title)}",
            "requireInteraction": False,
            "silent": False,
            "vibrate": [200, 100, 200],
            "data": {
                "url": url,
                "timestamp": str(timezone.now().timestamp())
            }
        }
        
        # Отправляем уведомление
        response = webpush(
            subscription_info=subscription_data,
            data=json.dumps(notification_data),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": f"mailto:{settings.VAPID_EMAIL}",
                "aud": subscription_data.get('endpoint', '').split('/')[2] if subscription_data.get('endpoint') else ''
            }
        )
        
        logger.info(f"Push-уведомление отправлено: {title}")
        return True
        
    except WebPushException as e:
        logger.error(f"Ошибка отправки push-уведомления: {e}")
        return False
    except ImportError:
        logger.error("pywebpush не установлен. Установите: pip install pywebpush")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка push-уведомления: {e}")
        return False

def send_bedtime_story_notification():
    """
    Отправляет напоминание о сказке перед сном (19:00)
    """
    from .models import PushSubscription
    from django.utils import timezone
    
    # Получаем все активные подписки
    subscriptions = PushSubscription.objects.filter(is_active=True)
    
    sent_count = 0
    
    for subscription in subscriptions:
        subscription_data = {
            'endpoint': subscription.endpoint,
            'keys': {
                'p256dh': subscription.p256dh_key,
                'auth': subscription.auth_key
            }
        }
        
        if send_push_notification(
            subscription_data=subscription_data,
            title="Время сказки! 🌙",
            body="Выберите добрую сказку для вашего малыша перед сном",
            url="/fairy-tales/",
            icon="/static/icons/icon-192x192.png"
        ):
            sent_count += 1
    
    logger.info(f"Напоминания о сказках отправлены {sent_count} подписчикам")
    return sent_count

def send_orthodox_calendar_notification(event_name, event_description, category_url):
    """
    Отправляет уведомление о православном празднике
    """
    from .models import PushSubscription
    
    subscriptions = PushSubscription.objects.filter(is_active=True)
    
    sent_count = 0
    
    for subscription in subscriptions:
        subscription_data = {
            'endpoint': subscription.endpoint,
            'keys': {
                'p256dh': subscription.p256dh_key,
                'auth': subscription.auth_key
            }
        }
        
        if send_push_notification(
            subscription_data=subscription_data,
            title=f"⛪ {event_name}",
            body=event_description,
            url=category_url,
            icon="/static/icons/icon-192x192.png"
        ):
            sent_count += 1
    
    logger.info(f"Уведомления о празднике '{event_name}' отправлены {sent_count} подписчикам")
    return sent_count

def send_new_content_notification(content_type, content_title, content_url):
    """
    Отправляет уведомление о новом контенте
    """
    from .models import PushSubscription
    
    subscriptions = PushSubscription.objects.filter(is_active=True)
    
    content_icons = {
        'story': '🎬',
        'book': '📚', 
        'fairy_tale': '🧚',
        'audio': '🎧'
    }
    
    icon = content_icons.get(content_type, '📚')
    
    sent_count = 0
    
    for subscription in subscriptions:
        subscription_data = {
            'endpoint': subscription.endpoint,
            'keys': {
                'p256dh': subscription.p256dh_key,
                'auth': subscription.auth_key
            }
        }
        
        if send_push_notification(
            subscription_data=subscription_data,
            title=f"Новый контент! {icon}",
            body=f"Добавлено: {content_title}",
            url=content_url,
            icon="/static/icons/icon-192x192.png"
        ):
            sent_count += 1
    
    logger.info(f"Уведомления о новом контенте отправлены {sent_count} подписчикам")
    return sent_count
