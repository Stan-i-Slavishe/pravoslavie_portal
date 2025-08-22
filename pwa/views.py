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
    UserNotificationSubscription, OrthodoxEvent, DailyOrthodoxInfo
)
import json
import logging
from datetime import date

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
def orthodox_calendar_page(request):
    """Страница православного календаря"""
    context = {
        'title': 'Православный календарь'
    }
    return render(request, 'pwa/orthodox_calendar.html', context)

@require_http_methods(["GET"])
def daily_orthodox_page(request):
    """Страница ежедневного православного календаря"""
    context = {
        'title': 'Православный календарь на каждый день'
    }
    return render(request, 'pwa/daily_orthodox_calendar.html', context)

@require_http_methods(["GET"])
def daily_orthodox_info(request, year, month, day):
    """Получить ежедневную православную информацию"""
    
    try:
        target_date = date(year, month, day)
    except ValueError:
        return JsonResponse({'error': 'Invalid date'}, status=400)
    
    try:
        # Получаем ежедневную информацию
        daily_info = DailyOrthodoxInfo.get_info_for_date(target_date)
        
        # Получаем православные события
        events = OrthodoxEvent.get_events_for_date(target_date)
        
        response_data = {
            'date': target_date.strftime('%Y-%m-%d'),
            'date_display': target_date.strftime('%d.%m.%Y'),
            'daily_info': {
                'fasting_type': daily_info.fasting_type,
                'fasting_type_display': daily_info.get_fasting_type_display(),
                'fasting_description': daily_info.fasting_description,
                'allowed_food': daily_info.allowed_food,
                'spiritual_note': daily_info.spiritual_note,
                'gospel_reading': daily_info.gospel_reading,
                'epistle_reading': daily_info.epistle_reading,
            },
            'events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'event_type': event.event_type,
                    'event_type_display': event.get_event_type_display(),
                    'is_movable': event.is_movable
                }
                for event in events
            ],
            'weekday': target_date.strftime('%A'),
            'weekday_ru': [
                'Понедельник', 'Вторник', 'Среда', 'Четверг',
                'Пятница', 'Суббота', 'Воскресенье'
            ][target_date.weekday()]
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Daily orthodox info error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

# =============================================================================
# 📅 API ДЛЯ ПРАВОСЛАВНОГО КАЛЕНДАРЯ
# =============================================================================

@require_http_methods(["GET"])
def orthodox_calendar_today(request):
    """Получение православных событий на сегодня"""
    try:
        from datetime import date
        from .models import OrthodoxEvent
        
        today = date.today()
        events = OrthodoxEvent.get_events_for_date(today)
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_type': event.event_type,
                'event_type_display': event.get_event_type_display(),
                'is_movable': event.is_movable,
                'icon_url': event.icon_url,
                'reading_url': event.reading_url,
            })
        
        return JsonResponse({
            'date': today.strftime('%Y-%m-%d'),
            'date_display': today.strftime('%d.%m.%Y'),
            'events': events_data,
            'count': len(events_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting today's orthodox events: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@require_http_methods(["GET"])
def orthodox_calendar_date(request, year, month, day):
    """Получение православных событий на конкретную дату"""
    try:
        from datetime import date
        from .models import OrthodoxEvent
        
        target_date = date(year, month, day)
        events = OrthodoxEvent.get_events_for_date(target_date)
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_type': event.event_type,
                'event_type_display': event.get_event_type_display(),
                'is_movable': event.is_movable,
                'icon_url': event.icon_url,
                'reading_url': event.reading_url,
            })
        
        return JsonResponse({
            'date': target_date.strftime('%Y-%m-%d'),
            'date_display': target_date.strftime('%d.%m.%Y'),
            'events': events_data,
            'count': len(events_data)
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid date'}, status=400)
    except Exception as e:
        logger.error(f"Error getting orthodox events for {year}-{month}-{day}: {e}")
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
def orthodox_calendar_month(request, year, month):
    """API для получения информации о месяце для календарного виджета"""
    try:
        from datetime import date, timedelta
        import calendar
        
        # Проверяем валидность даты
        if not (1 <= month <= 12):
            return JsonResponse({'error': 'Invalid month'}, status=400)
            
        # Получаем все дни месяца
        month_days = calendar.monthrange(year, month)[1]
        days_data = {}
        
        for day in range(1, month_days + 1):
            try:
                target_date = date(year, month, day)
                
                # Получаем ежедневную информацию
                daily_info = DailyOrthodoxInfo.get_info_for_date(target_date)
                
                # Получаем православные события
                events = OrthodoxEvent.get_events_for_date(target_date)
                
                # Определяем тип дня для цветовой индикации (вечный алгоритм)
                day_type = get_day_type_for_calendar(target_date, daily_info, events)
                
                days_data[str(day)] = {
                    'day_type': day_type,
                    'fasting_type': daily_info.fasting_type,
                    'fasting_display': daily_info.get_fasting_type_display(),
                    'has_events': len(events) > 0,
                    'events_count': len(events),
                    'main_event': events[0].title if events else None
                }
                
            except Exception as e:
                logger.error(f"Error processing day {day}: {e}")
                days_data[str(day)] = {
                    'day_type': 'feast',
                    'fasting_type': 'no_fast',
                    'fasting_display': 'Обычный день',
                    'has_events': False,
                    'events_count': 0,
                    'main_event': None
                }
        
        return JsonResponse({
            'year': year,
            'month': month,
            'month_name': [
                'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
            ][month - 1],
            'days': days_data,
            'total_days': month_days
        })
        
    except Exception as e:
        logger.error(f"Error getting month calendar: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

def get_day_type_for_calendar(target_date, daily_info, events):
    """Определить тип дня для календарного виджета"""
    
    # 1. ПРИОРИТЕТ: Проверяем строгие постные дни (они превалируют над праздниками)
    # 29 августа - Усекновение главы Иоанна Предтечи (строгий пост)
    if target_date.month == 8 and target_date.day == 29:
        return 'fast-day'  # Строгий постный день
    
    # 11 сентября - Усекновение главы Иоанна Предтечи (по новому стилю)
    if target_date.month == 9 and target_date.day == 11:
        return 'fast-day'  # Строгий постный день
        
    # Крестовоздвижение (14/27 сентября) - строгий пост
    if target_date.month == 9 and target_date.day == 27:
        return 'fast-day'  # Строгий постный день
    
    # 2. Проверяем тип поста из алгоритма
    if daily_info.fasting_type in ['strict_fast', 'dry_eating', 'complete_fast']:
        return 'fast-day'
    elif daily_info.fasting_type in ['light_fast', 'with_oil', 'wine_oil']:
        return 'fast-day'  # Объединяем все посты под одним цветом
    
    # 3. Проверяем великие праздники (только если не пост)
    for event in events:
        if event.event_type in ['great_feast', 'major_feast']:
            return 'holiday'
    
    # 4. Обычный день
    return 'feast'

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
