# analytics/production_views.py - НОВЫЕ VIEW ДЛЯ ПРОДАКШЕНА

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Avg, Sum
from django.shortcuts import render
from datetime import timedelta, datetime

# Импортируем все модели из models.py
from .models import (
    # Legacy модели
    PurchaseIntent, PopularContent, UserBehavior, 
    EmailSubscription, WeeklyReport,
    # Production модели
    AnalyticsEvent, ConversionFunnel
)

# VIEWS

@csrf_exempt
@require_http_methods(["POST"])
def track_event(request):
    """Универсальный endpoint для отслеживания событий"""
    try:
        data = json.loads(request.body)
        
        # Создаем событие
        event = AnalyticsEvent.objects.create(
            event_type=data['event_type'],
            session_id=data['session_id'],
            user=request.user if request.user.is_authenticated else None,
            data=data.get('data', {}),
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            page_url=data.get('data', {}).get('page_url', ''),
        )
        
        # Обновляем агрегированную статистику
        update_aggregated_stats(event)
        
        return JsonResponse({
            'success': True,
            'event_id': event.id,
            'timestamp': event.timestamp.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=400)

def update_aggregated_stats(event):
    """Обновление агрегированной статистики"""
    
    # Обновляем воронку конверсии
    today = timezone.now().date()
    
    if event.event_type == 'page_view':
        ConversionFunnel.objects.get_or_create(
            date=today,
            step='visit',
            defaults={'count': 0}
        )
        ConversionFunnel.objects.filter(
            date=today,
            step='visit'
        ).update(count=F('count') + 1)
    
    elif event.event_type == 'add_to_cart':
        product_type = event.data.get('product_type', '')
        ConversionFunnel.objects.get_or_create(
            date=today,
            step='add_to_cart',
            product_type=product_type,
            defaults={'count': 0}
        )
        ConversionFunnel.objects.filter(
            date=today,
            step='add_to_cart',
            product_type=product_type
        ).update(count=F('count') + 1)
    
    elif event.event_type == 'purchase_complete':
        product_items = event.data.get('items', [])
        for item in product_items:
            ConversionFunnel.objects.get_or_create(
                date=today,
                step='purchase',
                product_type=item.get('type', ''),
                defaults={'count': 0}
            )
            ConversionFunnel.objects.filter(
                date=today,
                step='purchase',
                product_type=item.get('type', '')
            ).update(count=F('count') + 1)

@staff_member_required
def production_dashboard(request):
    """Дашборд аналитики для продакшена"""
    
    # Период анализа
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Общая статистика
    stats = {
        'total_events': AnalyticsEvent.objects.count(),
        'unique_sessions': AnalyticsEvent.objects.values('session_id').distinct().count(),
        'registered_users': AnalyticsEvent.objects.filter(user__isnull=False).values('user').distinct().count(),
        
        'events_today': AnalyticsEvent.objects.filter(timestamp__date=today).count(),
        'events_week': AnalyticsEvent.objects.filter(timestamp__date__gte=week_ago).count(),
        'events_month': AnalyticsEvent.objects.filter(timestamp__date__gte=month_ago).count(),
    }
    
    # Статистика по типам событий
    event_stats = AnalyticsEvent.objects.values('event_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Популярные страницы
    popular_pages = AnalyticsEvent.objects.filter(
        event_type='page_view'
    ).values('page_url').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Воронка конверсии
    funnel_data = ConversionFunnel.objects.filter(
        date__gte=week_ago
    ).values('step').annotate(
        total=Sum('count')
    ).order_by('step')
    
    # Топ поисковых запросов
    search_queries = AnalyticsEvent.objects.filter(
        event_type='search',
        timestamp__date__gte=week_ago
    ).values('data__query').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Активность по часам
    hourly_activity = []
    for hour in range(24):
        count = AnalyticsEvent.objects.filter(
            timestamp__hour=hour,
            timestamp__date__gte=week_ago
        ).count()
        hourly_activity.append({
            'hour': hour,
            'count': count
        })
    
    # Статистика скачиваний
    downloads_stats = AnalyticsEvent.objects.filter(
        event_type='download',
        timestamp__date__gte=week_ago
    ).values('data__item_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Статистика покупок
    purchases_stats = AnalyticsEvent.objects.filter(
        event_type='purchase_complete',
        timestamp__date__gte=week_ago
    ).aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('data__total_amount')
    )
    
    # IP статистика (legacy совместимость)
    ip_stats = []
    
    context = {
        'stats': stats,
        'event_stats': list(event_stats),
        'popular_pages': popular_pages,
        'funnel_data': list(funnel_data),
        'search_queries': search_queries,
        'hourly_activity': hourly_activity,
        'downloads_stats': list(downloads_stats),
        'purchases_stats': purchases_stats,
        'ip_stats': ip_stats,
    }
    
    return render(request, 'analytics/production_dashboard.html', context)

@staff_member_required
def real_time_stats(request):
    """Статистика в реальном времени"""
    
    # Последние 5 минут
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    
    recent_stats = {
        'events_5min': AnalyticsEvent.objects.filter(
            timestamp__gte=five_minutes_ago
        ).count(),
        
        'active_sessions': AnalyticsEvent.objects.filter(
            timestamp__gte=five_minutes_ago
        ).values('session_id').distinct().count(),
        
        'recent_purchases': AnalyticsEvent.objects.filter(
            event_type='purchase_complete',
            timestamp__gte=five_minutes_ago
        ).count(),
        
        'recent_errors': AnalyticsEvent.objects.filter(
            event_type='error',
            timestamp__gte=five_minutes_ago
        ).count(),
    }
    
    # Последние события
    recent_events = AnalyticsEvent.objects.select_related('user').filter(
        timestamp__gte=five_minutes_ago
    ).order_by('-timestamp')[:20]
    
    # Форматируем события
    formatted_events = []
    for event in recent_events:
        formatted_events.append({
            'type': event.get_event_type_display(),
            'user': event.user.username if event.user else 'Анонимный',
            'timestamp': event.timestamp.strftime('%H:%M:%S'),
            'page_url': event.page_url,
            'data': event.data
        })
    
    return JsonResponse({
        'stats': recent_stats,
        'events': formatted_events,
        'timestamp': timezone.now().isoformat()
    })

def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@staff_member_required  
def export_analytics(request):
    """Экспорт данных аналитики"""
    
    # Параметры экспорта
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    event_type = request.GET.get('event_type')
    
    # Фильтруем события
    events = AnalyticsEvent.objects.all()
    
    if start_date:
        events = events.filter(timestamp__date__gte=start_date)
    if end_date:
        events = events.filter(timestamp__date__lte=end_date)
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Ограничиваем количество записей
    events = events.order_by('-timestamp')[:10000]
    
    # Подготавливаем данные для экспорта
    export_data = []
    for event in events:
        export_data.append({
            'timestamp': event.timestamp.isoformat(),
            'event_type': event.get_event_type_display(),
            'user': event.user.username if event.user else 'Анонимный',
            'session_id': event.session_id,
            'page_url': event.page_url,
            'ip_address': event.ip_address,
            'data': event.data
        })
    
    return JsonResponse({
        'success': True,
        'count': len(export_data),
        'data': export_data
    })
