# PWA Views for Православный портал

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView
from .models import (
    PushSubscription, NotificationCategory, UserNotificationSettings,
    UserNotificationSubscription
)
import json
import logging

logger = logging.getLogger(__name__)

class OfflineView(TemplateView):
    """Офлайн страница для PWA"""
    template_name = 'offline/offline.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Нет подключения к интернету',
            'offline_features': [
                'Сохраненные терапевтические сказки',
                'Ваши избранные материалы', 
                'Созданные плейлисты',
                'Скачанные книги',
                'История просмотров'
            ]
        })
        return context

def manifest_view(request):
    """Служит манифест файл с правильными заголовками"""
    try:
        with open(settings.BASE_DIR / 'static' / 'manifest.json', 'r', encoding='utf-8') as f:
            manifest_content = f.read()
        
        response = HttpResponse(manifest_content, content_type='application/manifest+json')
        response['Cache-Control'] = 'public, max-age=86400'  # Кеш на 24 часа
        return response
    except FileNotFoundError:
        logger.error("Manifest file not found")
        return JsonResponse({'error': 'Manifest not found'}, status=404)

def service_worker_view(request):
    """Служит Service Worker файл из корня проекта"""
    try:
        with open(settings.BASE_DIR / 'sw.js', 'r', encoding='utf-8') as f:
            sw_content = f.read()
        
        response = HttpResponse(sw_content, content_type='application/javascript')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Не кешируем SW
        response['Service-Worker-Allowed'] = '/'
        return response
    except FileNotFoundError:
        logger.error("Service Worker file not found")
        return HttpResponse('// Service Worker not found', content_type='application/javascript', status=404)

@csrf_exempt
@require_http_methods(["POST"])
def push_subscribe(request):
    """Подписка на push-уведомления"""
    try:
        data = json.loads(request.body)
        subscription = data.get('subscription')
        user_agent = data.get('user_agent', '')
        
        if not subscription:
            return JsonResponse({'error': 'No subscription data'}, status=400)
        
        # Для демонстрации просто возвращаем успех
        # В продакшене здесь будет сохранение в БД
        logger.info(f"Push subscription received from user {request.user.id if request.user.is_authenticated else 'anonymous'}")
        
        return JsonResponse({
            'success': True,
            'message': 'Подписка на уведомления активирована'
        })
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Push subscription error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@require_http_methods(["GET"])
def get_csrf_token(request):
    """Возвращает CSRF токен для Service Worker"""
    from django.middleware.csrf import get_token
    
    return JsonResponse({
        'csrfToken': get_token(request)
    })

@require_http_methods(["HEAD", "GET"])
def ping(request):
    """Проверка соединения для Service Worker"""
    return HttpResponse('pong', content_type='text/plain')

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def sync_playlists(request):
    """Синхронизация плейлистов из офлайн режима"""
    try:
        data = json.loads(request.body)
        playlist_data = data.get('playlist')
        
        if not playlist_data:
            return JsonResponse({'error': 'No playlist data'}, status=400)
        
        # Для демонстрации просто возвращаем успех
        # В продакшене здесь будет реальная синхронизация
        logger.info(f"Playlist sync requested by user {request.user.id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Плейлист синхронизирован'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Playlist sync error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def sync_favorites(request):
    """Синхронизация избранного из офлайн режима"""
    try:
        data = json.loads(request.body)
        favorite_data = data.get('favorite')
        
        if not favorite_data:
            return JsonResponse({'error': 'No favorite data'}, status=400)
        
        # Для демонстрации просто возвращаем успех
        logger.info(f"Favorites sync requested by user {request.user.id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Избранное синхронизировано'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Favorites sync error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def sync_cart(request):
    """Синхронизация корзины из офлайн режима"""
    try:
        data = json.loads(request.body)
        cart_data = data.get('cart_item')
        
        if not cart_data:
            return JsonResponse({'error': 'No cart data'}, status=400)
        
        # Для демонстрации просто возвращаем успех
        logger.info(f"Cart sync requested")
        
        return JsonResponse({
            'success': True,
            'message': 'Корзина синхронизирована'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Cart sync error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@require_http_methods(["GET"])
def orthodoxy_calendar_today(request):
    """API для православного календаря"""
    from datetime import date
    
    today = date.today()
    events = []
    
    # Воскресенье - особый день
    if today.weekday() == 6:  # Воскресенье
        events.append({
            'id': 'sunday',
            'name': 'Воскресенье - день Господень',
            'description': 'Посетите богослужение и послушайте духовные рассказы',
            'category': 'duhovnye',
            'type': 'weekly'
        })
    
    # Рождественский период
    if today.month == 12 and today.day >= 25:
        events.append({
            'id': 'christmas',
            'name': 'Рождество Христово',
            'description': 'Великий праздник Рождества Господа нашего Иисуса Христа',
            'category': 'prazdniki',
            'type': 'major_feast'
        })
    
    # Новогодний период
    if today.month == 1 and today.day <= 7:
        events.append({
            'id': 'new_year',
            'name': 'Святки',
            'description': 'Святочные дни - время радости и духовного обновления',
            'category': 'prazdniki',
            'type': 'holy_days'
        })
    
    # Пост
    if today.month in [3, 4]:  # Великий пост примерно
        events.append({
            'id': 'great_lent',
            'name': 'Великий пост',
            'description': 'Время духовного очищения и подготовки к Пасхе',
            'category': 'posty',
            'type': 'fast'
        })
    
    return JsonResponse({
        'events': events,
        'date': today.isoformat()
    })

@require_http_methods(["GET"])
def push_test_page(request):
    """Тестовая страница для push-уведомлений"""
    # Только для администраторов в разработке
    if not settings.DEBUG or not request.user.is_staff:
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

# =============================================================================
# 🔔 НОВЫЕ API ДЛЯ НАСТРОЕК УВЕДОМЛЕНИЙ
# =============================================================================

@login_required
@require_http_methods(["GET"])
def notification_settings_page(request):
    """Страница настроек уведомлений"""
    # Получаем или создаем настройки пользователя
    user_settings, created = UserNotificationSettings.objects.get_or_create(user=request.user)
    
    # Получаем все категории
    categories = NotificationCategory.objects.filter(is_active=True)
    
    # Получаем подписки пользователя
    subscriptions = UserNotificationSubscription.objects.filter(user=request.user)
    subscriptions_dict = {sub.category.name: sub for sub in subscriptions}
    
    context = {
        'user_settings': user_settings,
        'categories': categories,
        'subscriptions': subscriptions_dict,
        'title': 'Настройки уведомлений'
    }
    
    return render(request, 'pwa/notification_settings.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def save_notification_settings(request):
    """Сохранение настроек уведомлений"""
    try:
        data = json.loads(request.body)
        
        # Получаем или создаем настройки пользователя
        user_settings, created = UserNotificationSettings.objects.get_or_create(user=request.user)
        
        # Обновляем общие настройки
        user_settings.notifications_enabled = data.get('notifications_enabled', True)
        user_settings.quiet_hours_enabled = data.get('quiet_hours_enabled', True)
        user_settings.quiet_start = data.get('quiet_start', '22:00')
        user_settings.quiet_end = data.get('quiet_end', '08:00')
        user_settings.child_mode = data.get('child_mode', False)
        user_settings.child_bedtime = data.get('child_bedtime', '20:00')
        
        # Обновляем дни недели
        weekdays = data.get('weekdays', {})
        user_settings.notify_monday = weekdays.get('notify_monday', True)
        user_settings.notify_tuesday = weekdays.get('notify_tuesday', True)
        user_settings.notify_wednesday = weekdays.get('notify_wednesday', True)
        user_settings.notify_thursday = weekdays.get('notify_thursday', True)
        user_settings.notify_friday = weekdays.get('notify_friday', True)
        user_settings.notify_saturday = weekdays.get('notify_saturday', True)
        user_settings.notify_sunday = weekdays.get('notify_sunday', True)
        
        user_settings.save()
        
        # Обновляем подписки на категории
        categories_data = data.get('categories', {})
        for category_name, category_settings in categories_data.items():
            try:
                category = NotificationCategory.objects.get(name=category_name)
                subscription, created = UserNotificationSubscription.objects.get_or_create(
                    user=request.user,
                    category=category,
                    defaults={
                        'enabled': category_settings.get('enabled', True),
                        'frequency': category_settings.get('frequency', 'daily'),
                        'preferred_time': category_settings.get('time'),
                        'max_daily_count': category_settings.get('max_daily', 3),
                        'priority': category_settings.get('priority', 5)
                    }
                )
                
                if not created:
                    subscription.enabled = category_settings.get('enabled', True)
                    subscription.frequency = category_settings.get('frequency', 'daily')
                    subscription.preferred_time = category_settings.get('time')
                    subscription.max_daily_count = category_settings.get('max_daily', 3)
                    subscription.priority = category_settings.get('priority', 5)
                    subscription.save()
                    
            except NotificationCategory.DoesNotExist:
                logger.warning(f"Category {category_name} not found")
                continue
        
        logger.info(f"Notification settings saved for user {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'message': 'Настройки успешно сохранены'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error saving notification settings: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@login_required
@require_http_methods(["GET"])
def get_notification_settings(request):
    """Получение текущих настроек уведомлений пользователя"""
    try:
        # Получаем настройки пользователя
        user_settings = UserNotificationSettings.objects.filter(user=request.user).first()
        subscriptions = UserNotificationSubscription.objects.filter(user=request.user)
        
        # Формируем ответ
        settings_data = {
            'notifications_enabled': user_settings.notifications_enabled if user_settings else True,
            'quiet_hours_enabled': user_settings.quiet_hours_enabled if user_settings else True,
            'quiet_start': str(user_settings.quiet_start) if user_settings else '22:00',
            'quiet_end': str(user_settings.quiet_end) if user_settings else '08:00',
            'child_mode': user_settings.child_mode if user_settings else False,
            'child_bedtime': str(user_settings.child_bedtime) if user_settings else '20:00',
            'categories': {}
        }
        
        # Добавляем настройки категорий
        for subscription in subscriptions:
            settings_data['categories'][subscription.category.name] = {
                'enabled': subscription.enabled,
                'frequency': subscription.frequency,
                'preferred_time': str(subscription.preferred_time) if subscription.preferred_time else None,
                'max_daily_count': subscription.max_daily_count,
                'priority': subscription.priority
            }
        
        return JsonResponse(settings_data)
        
    except Exception as e:
        logger.error(f"Error getting notification settings: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)
