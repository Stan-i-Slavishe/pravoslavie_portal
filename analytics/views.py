# analytics/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Avg
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import timedelta
import requests

def get_content_title(content_type, object_id):
    """Получаем человекопонятное название контента с короткими пометками"""
    try:
        if content_type == 'book':
            from books.models import Book
            book = Book.objects.get(id=object_id)
            return f"{book.title} (книги)"
        elif content_type == 'fairy_tale':
            from fairy_tales.models import FairyTaleTemplate
            fairy_tale = FairyTaleTemplate.objects.get(id=object_id)
            return f"{fairy_tale.title} (подробно)"
        elif content_type == 'audio':
            from audio.models import AudioTrack
            audio = AudioTrack.objects.get(id=object_id)
            return f"{audio.title} (аудио)"
        elif content_type == 'subscription':
            from subscriptions.models import Subscription
            subscription = Subscription.objects.get(id=object_id)
            return f"{subscription.name} (подписка)"
        elif content_type == 'product':
            from shop.models import Product
            product = Product.objects.get(id=object_id)
            
            # Для персонализированных сказок показываем только название сказки
            if product.product_type == 'fairy_tale' and product.fairy_tale_template_id:
                try:
                    from fairy_tales.models import FairyTaleTemplate
                    fairy_tale = FairyTaleTemplate.objects.get(id=product.fairy_tale_template_id)
                    return f"{fairy_tale.title} (магазин)"
                except:
                    pass
            
            return f"{product.title} (магазин)"
        else:
            return f"{content_type.title()} #{object_id}"
    except Exception as e:
        print(f"\n❌ Ошибка получения названия для {content_type} #{object_id}: {e}")
        return f"{content_type.title()} #{object_id} (ошибка)"

from .models import PurchaseIntent, PopularContent, UserBehavior, EmailSubscription

@csrf_exempt
@require_http_methods(["POST"])
def track_purchase_intent(request):
    """Отслеживание клика на заглушку покупки"""
    try:
        data = json.loads(request.body)
        
        # Получаем или создаем пользовательское поведение
        user_behavior = None
        if request.user.is_authenticated:
            user_behavior, _ = UserBehavior.objects.get_or_create(user=request.user)
        else:
            session_key = data.get('session_key')
            if session_key:
                user_behavior, _ = UserBehavior.objects.get_or_create(session_key=session_key)
        
        # Получаем IP и геолокацию
        ip_address = get_client_ip(request)
        
        # Проверяем, есть ли уже запись для этого пользователя и объекта
        intent_filter = {
            'content_type': data['content_type'],
            'object_id': data['object_id'],
            'button_type': data['button_type'],
        }
        
        if request.user.is_authenticated:
            intent_filter['user'] = request.user
        else:
            intent_filter['session_key'] = data.get('session_key')
        
        # Получаем или создаем запись о намерении покупки
        intent, created = PurchaseIntent.objects.get_or_create(
            **intent_filter,
            defaults={
                'ip_address': ip_address,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referer': data.get('referer', ''),
                'page_url': data.get('page_url', ''),
            }
        )
        
        if not created:
            # Увеличиваем счетчик кликов
            intent.click_count = F('click_count') + 1
            intent.clicked_at = timezone.now()
            intent.save(update_fields=['click_count', 'clicked_at'])
            intent.refresh_from_db()
        
        # Обновляем статистику популярного контента
        popular_content, _ = PopularContent.objects.get_or_create(
            content_type=data['content_type'],
            object_id=data['object_id']
        )
        popular_content.purchase_intents = F('purchase_intents') + 1
        popular_content.save(update_fields=['purchase_intents'])
        popular_content.refresh_from_db()
        popular_content.update_conversion_rate()
        
        # Обновляем поведение пользователя
        if user_behavior:
            user_behavior.total_purchase_intents = F('total_purchase_intents') + 1
            user_behavior.save(update_fields=['total_purchase_intents'])
            user_behavior.refresh_from_db()
            user_behavior.calculate_purchase_probability()
        
        # 📧 Отправляем email уведомление админу (ОТКЛЮЧЕНО - спам)
        # if created:  # Только для новых кликов
        #     from .email_services.notifications import send_purchase_intent_notification
        #     # Отправляем асинхронно чтобы не тормозить ответ
        #     try:
        #         send_purchase_intent_notification(intent)
        #     except Exception as e:
        #         # Логируем ошибку, но не ломаем основной функционал
        #         print(f"⚠️ Ошибка отправки email уведомления: {e}")
        
        return JsonResponse({
            'success': True,
            'total_clicks': intent.click_count,
            'user_probability': user_behavior.purchase_probability if user_behavior else 0,
            'message': 'Purchase intent tracked successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def subscribe_notifications(request):
    """Подписка на уведомления о запуске платежей"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email required'})
        
        # Создаем подписку
        subscription, created = EmailSubscription.objects.get_or_create(
            email=email,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'interested_in': data.get('interested_in', ''),
                'source_page': data.get('source_page', ''),
                'notify_payment_launch': True,
                'notify_new_content': True,
            }
        )
        
        # 📧 Отправляем подтверждение подписки
        if created:
            from .email_services.notifications import send_subscription_confirmation
            try:
                send_subscription_confirmation(subscription)
                message = 'Подписка оформлена! Проверьте почту.'
            except Exception as e:
                print(f"⚠️ Ошибка отправки подтверждения: {e}")
                message = 'Подписка оформлена!'
        else:
            message = 'Email уже подписан'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'total_subscribers': EmailSubscription.objects.filter(is_active=True).count()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@staff_member_required
def analytics_dashboard(request):
    """Дашборд аналитики для администраторов"""
    
    # Статистика за разные периоды
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Общая статистика
    stats = {
        'total_intents': PurchaseIntent.objects.count(),
        'unique_users': PurchaseIntent.objects.values('user', 'session_key').distinct().count(),
        'total_subscribers': EmailSubscription.objects.filter(is_active=True).count(),
        
        'intents_today': PurchaseIntent.objects.filter(clicked_at__date=today).count(),
        'intents_week': PurchaseIntent.objects.filter(clicked_at__date__gte=week_ago).count(),
        'intents_month': PurchaseIntent.objects.filter(clicked_at__date__gte=month_ago).count(),
    }
    
    # Топ контента по намерениям покупки (с названиями)
    top_content = PopularContent.objects.order_by('-purchase_intents')[:10]
    
    # Добавляем названия к топ контенту
    for content in top_content:
        content.title = get_content_title(content.content_type, content.object_id)
    
    # Статистика по типам контента
    content_stats = PurchaseIntent.objects.values('content_type').annotate(
        total_clicks=Count('id'),
        unique_users=Count('session_key', distinct=True)
    ).order_by('-total_clicks')
    
    # Статистика по типам кнопок
    button_stats = PurchaseIntent.objects.values('button_type').annotate(
        total_clicks=Count('id')
    ).order_by('-total_clicks')
    
    # IP адреса пользователей (вместо географии)
    ip_stats = PurchaseIntent.objects.values('ip_address').annotate(
        clicks=Count('id')
    ).order_by('-clicks')[:10]
    
    # Пользователи с высокой вероятностью покупки
    hot_users = UserBehavior.objects.filter(
        purchase_probability__gte=70
    ).order_by('-purchase_probability')[:20]
    
    # Динамика по дням (последние 30 дней)
    daily_stats = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = PurchaseIntent.objects.filter(clicked_at__date=date).count()
        daily_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'clicks': count
        })
    daily_stats.reverse()
    
    context = {
        'stats': stats,
        'top_content': top_content,
        'content_stats': list(content_stats),
        'button_stats': list(button_stats),
        'ip_stats': ip_stats,
        'hot_users': hot_users,
        'daily_stats': daily_stats,
    }
    
    return render(request, 'analytics/dashboard.html', context)

def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@staff_member_required
def api_stats(request):
    """API для получения статистики в реальном времени"""
    
    stats = {
        'intents_today': PurchaseIntent.objects.filter(
            clicked_at__date=timezone.now().date()
        ).count(),
        
        'recent_subscribers': EmailSubscription.objects.filter(
            subscribed_at__gte=timezone.now() - timedelta(hours=24)
        ).count(),
        
        'purchase_ready_users': UserBehavior.objects.filter(
            purchase_probability__gte=80
        ).count(),
    }
    
    return JsonResponse(stats)

# 📧 Новые функции для Email подписок

def subscription_form(request):
    """Форма подписки на уведомления"""
    if request.method == 'POST':
        email = request.POST.get('email')
        interested_in = request.POST.get('interested_in', '')
        
        if not email:
            messages.error(request, 'Пожалуйста, укажите email адрес')
            return render(request, 'analytics/subscription_form.html')
        
        # Создаем подписку
        subscription, created = EmailSubscription.objects.get_or_create(
            email=email,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'interested_in': interested_in,
                'source_page': request.META.get('HTTP_REFERER', ''),
                'notify_payment_launch': True,
                'notify_new_content': True,
            }
        )
        
        if created:
            # Отправляем подтверждение
            from .email_services.notifications import send_subscription_confirmation
            try:
                send_subscription_confirmation(subscription)
                messages.success(request, 'Подписка оформлена! Проверьте почту.')
            except Exception as e:
                messages.success(request, 'Подписка оформлена!')
        else:
            messages.info(request, 'Вы уже подписаны на уведомления')
        
        return redirect('analytics:subscription_success')
    
    return render(request, 'analytics/subscription_form.html')

def subscription_success(request):
    """Страница успешной подписки"""
    return render(request, 'analytics/subscription_success.html')

def unsubscribe(request, subscription_id):
    """Отписка от уведомлений"""
    subscription = get_object_or_404(EmailSubscription, id=subscription_id)
    
    if request.method == 'POST':
        subscription.is_active = False
        subscription.save()
        messages.success(request, 'Вы успешно отписались от уведомлений')
        return render(request, 'analytics/unsubscribe_success.html')
    
    return render(request, 'analytics/unsubscribe_confirm.html', {
        'subscription': subscription
    })

@staff_member_required
def email_campaigns(request):
    """Управление email кампаниями для админов"""
    from .models import WeeklyReport
    
    # Последние отчеты
    recent_reports = WeeklyReport.objects.all()[:10]
    
    # Статистика подписок
    total_subscribers = EmailSubscription.objects.filter(is_active=True).count()
    payment_subscribers = EmailSubscription.objects.filter(
        is_active=True, notify_payment_launch=True
    ).count()
    
    context = {
        'recent_reports': recent_reports,
        'total_subscribers': total_subscribers,
        'payment_subscribers': payment_subscribers,
    }
    
    return render(request, 'analytics/email_campaigns.html', context)
