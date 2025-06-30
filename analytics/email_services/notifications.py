# analytics/email_services/notifications.py

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_admin_emails():
    """Получить список email администраторов"""
    # Можно настроить в settings или брать из User.is_staff
    admin_emails = getattr(settings, 'ADMIN_EMAIL_LIST', ['admin@pravoslavie-portal.ru'])
    
    # Дополнительно можем взять из базы данных staff пользователей
    from django.contrib.auth.models import User
    staff_emails = User.objects.filter(is_staff=True, email__isnull=False).values_list('email', flat=True)
    
    # Объединяем и убираем дубли
    all_emails = list(set(list(admin_emails) + list(staff_emails)))
    return [email for email in all_emails if email]  # Убираем пустые

def send_purchase_intent_notification(purchase_intent):
    """Отправить уведомление админу о клике на покупку"""
    try:
        from ..views import get_content_title
        
        # Получаем данные для email
        content_title = get_content_title(purchase_intent.content_type, purchase_intent.object_id)
        user_info = f"Пользователь: {purchase_intent.user.username}" if purchase_intent.user else f"Анонимный (сессия: {purchase_intent.session_key[:8]})"
        
        # Тема письма
        subject = f"🛒 Новый клик на покупку: {content_title}"
        
        # Создаем контекст для шаблона
        context = {
            'purchase_intent': purchase_intent,
            'content_title': content_title,
            'user_info': user_info,
            'admin_url': f"http://localhost:8000/admin/analytics/purchaseintent/{purchase_intent.id}/change/",
            'analytics_url': "http://localhost:8000/analytics/dashboard/",
        }
        
        # Рендерим шаблоны
        html_content = render_to_string('analytics/emails/purchase_intent_notification.html', context)
        text_content = render_to_string('analytics/emails/purchase_intent_notification.txt', context)
        
        # Отправляем email
        admin_emails = get_admin_emails()
        if admin_emails:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            # Обновляем статус уведомления
            purchase_intent.admin_notified = True
            purchase_intent.notification_sent_at = timezone.now()
            purchase_intent.save(update_fields=['admin_notified', 'notification_sent_at'])
            
            logger.info(f"Отправлено уведомление о покупке {purchase_intent.id} на {len(admin_emails)} адресов")
            return True
        else:
            logger.warning("Нет email адресов администраторов для уведомлений")
            return False
            
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления о покупке {purchase_intent.id}: {e}")
        return False

def send_subscription_confirmation(subscription):
    """Отправить подтверждение подписки"""
    try:
        subject = "✅ Подписка на уведомления оформлена"
        
        context = {
            'subscription': subscription,
            'unsubscribe_url': f"http://localhost:8000/analytics/unsubscribe/{subscription.id}/",
        }
        
        html_content = render_to_string('analytics/emails/subscription_confirmation.html', context)
        text_content = render_to_string('analytics/emails/subscription_confirmation.txt', context)
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscription.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f"Отправлено подтверждение подписки для {subscription.email}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка отправки подтверждения подписки {subscription.id}: {e}")
        return False

def generate_weekly_report(week_start, week_end):
    """Генерация недельного отчета"""
    from ..models import PurchaseIntent, PopularContent, EmailSubscription, WeeklyReport
    from django.db.models import Count, Q
    
    try:
        # Собираем статистику за неделю
        week_intents = PurchaseIntent.objects.filter(
            clicked_at__date__gte=week_start,
            clicked_at__date__lte=week_end
        )
        
        total_intents = week_intents.count()
        unique_users = week_intents.values('user', 'session_key').distinct().count()
        
        # Новые подписки за неделю
        new_subscriptions = EmailSubscription.objects.filter(
            subscribed_at__date__gte=week_start,
            subscribed_at__date__lte=week_end
        ).count()
        
        # Топ контента
        from ..views import get_content_title
        top_content_data = []
        
        # Группируем по типу контента и ID
        content_stats = week_intents.values('content_type', 'object_id').annotate(
            clicks=Count('id')
        ).order_by('-clicks')[:10]
        
        for stat in content_stats:
            title = get_content_title(stat['content_type'], stat['object_id'])
            top_content_data.append({
                'title': title,
                'content_type': stat['content_type'],
                'object_id': stat['object_id'],
                'clicks': stat['clicks']
            })
        
        # Создаем или обновляем отчет
        report, created = WeeklyReport.objects.get_or_create(
            week_start=week_start,
            week_end=week_end,
            defaults={
                'total_purchase_intents': total_intents,
                'unique_users': unique_users,
                'new_subscriptions': new_subscriptions,
                'top_content': top_content_data,
            }
        )
        
        if not created:
            # Обновляем существующий отчет
            report.total_purchase_intents = total_intents
            report.unique_users = unique_users
            report.new_subscriptions = new_subscriptions
            report.top_content = top_content_data
            report.save()
        
        return report
        
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        return None

def send_weekly_report(report):
    """Отправить недельный отчет администраторам и подписчикам"""
    try:
        subject = f"📊 Недельный отчет: {report.week_start.strftime('%d.%m')} - {report.week_end.strftime('%d.%m.%Y')}"
        
        context = {
            'report': report,
            'period': f"{report.week_start.strftime('%d.%m')} - {report.week_end.strftime('%d.%m.%Y')}",
            'analytics_url': "http://localhost:8000/analytics/dashboard/",
        }
        
        html_content = render_to_string('analytics/emails/weekly_report.html', context)
        text_content = render_to_string('analytics/emails/weekly_report.txt', context)
        
        # Отправляем администраторам
        admin_emails = get_admin_emails()
        if admin_emails:
            msg = EmailMultiAlternatives(
                subject=f"[АДМИН] {subject}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            report.sent_to_admins = True
            logger.info(f"Недельный отчет отправлен администраторам: {len(admin_emails)} адресов")
        
        # Отправляем подписчикам
        from ..models import EmailSubscription
        subscribers = EmailSubscription.objects.filter(
            is_active=True,
            notify_weekly_reports=True
        )
        
        if subscribers.exists():
            subscriber_emails = list(subscribers.values_list('email', flat=True))
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscriber_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            # Обновляем статистику подписчиков
            from django.db import models
            subscribers.update(
                emails_sent=models.F('emails_sent') + 1,
                last_email_sent=timezone.now()
            )
            
            report.sent_to_subscribers = True
            logger.info(f"Недельный отчет отправлен подписчикам: {len(subscriber_emails)} адресов")
        
        report.save()
        return True
        
    except Exception as e:
        logger.error(f"Ошибка отправки недельного отчета: {e}")
        return False

def send_payment_launch_notification():
    """Отправить уведомление о запуске платежей всем подписчикам"""
    try:
        from ..models import EmailSubscription
        
        subscribers = EmailSubscription.objects.filter(
            is_active=True,
            notify_payment_launch=True
        )
        
        if not subscribers.exists():
            logger.info("Нет подписчиков для уведомления о запуске платежей")
            return True
        
        subject = "🎉 Запуск платежей на Православном портале!"
        
        context = {
            'shop_url': "http://localhost:8000/shop/",
            'site_name': "Православный портал",
        }
        
        html_content = render_to_string('analytics/emails/payment_launch.html', context)
        text_content = render_to_string('analytics/emails/payment_launch.txt', context)
        
        # Отправляем батчами по 50 адресов
        batch_size = 50
        total_sent = 0
        
        for i in range(0, subscribers.count(), batch_size):
            batch = subscribers[i:i + batch_size]
            batch_emails = list(batch.values_list('email', flat=True))
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=batch_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            total_sent += len(batch_emails)
            logger.info(f"Отправлен батч уведомлений о запуске платежей: {len(batch_emails)} адресов")
        
        # Обновляем статистику
        from django.db import models
        subscribers.update(
            emails_sent=models.F('emails_sent') + 1,
            last_email_sent=timezone.now()
        )
        
        logger.info(f"Всего отправлено уведомлений о запуске платежей: {total_sent}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка отправки уведомлений о запуске платежей: {e}")
        return False
