# shop/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import logging

from .models import Order, OrderItem
from .utils import send_order_email

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    """
    Отправка email при создании нового заказа
    """
    if created and instance.status == 'pending':
        try:
            # Отправляем email покупателю
            send_order_email(
                order=instance,
                template_type='order_created',
                recipient_email=instance.email
            )
            
            # Отправляем уведомление администраторам
            admin_emails = getattr(settings, 'ADMIN_EMAIL_LIST', [])
            if admin_emails:
                send_order_email(
                    order=instance,
                    template_type='order_created_admin',
                    recipient_email=admin_emails
                )
                
            logger.info(f"Order created emails sent for order {instance.short_id}")
            
        except Exception as e:
            logger.error(f"Failed to send order created email for {instance.short_id}: {e}")


@receiver(pre_save, sender=Order)
def order_status_changed_notification(sender, instance, **kwargs):
    """
    Отправка email при изменении статуса заказа
    """
    if instance.pk:  # Только для существующих заказов
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            
            # Проверяем, изменился ли статус
            if old_instance.status != instance.status:
                
                # Отправляем email покупателю о смене статуса
                send_order_email(
                    order=instance,
                    template_type='order_status_changed',
                    recipient_email=instance.email,
                    context={'old_status': old_instance.status}
                )
                
                # Специальные уведомления для определенных статусов
                if instance.status == 'paid':
                    # Заказ оплачен - отправляем инструкции по скачиванию
                    send_order_email(
                        order=instance,
                        template_type='order_paid_download_instructions',
                        recipient_email=instance.email
                    )
                    
                    # Обновляем время оплаты
                    instance.paid_at = timezone.now()
                    
                elif instance.status == 'completed':
                    # Заказ завершен
                    send_order_email(
                        order=instance,
                        template_type='order_completed',
                        recipient_email=instance.email
                    )
                    
                    # Обновляем время завершения
                    instance.completed_at = timezone.now()
                
                logger.info(f"Order status changed email sent for order {instance.short_id}: {old_instance.status} -> {instance.status}")
                
        except Order.DoesNotExist:
            # Новый заказ, обрабатывается в post_save
            pass
        except Exception as e:
            logger.error(f"Failed to send order status email for {instance.short_id}: {e}")


@receiver(post_save, sender=OrderItem)
def fairy_tale_status_changed_notification(sender, instance, **kwargs):
    """
    Отправка email при изменении статуса терапевтической сказки
    """
    if instance.is_fairy_tale and instance.fairy_tale_status:
        try:
            # Отправляем уведомление только для определенных статусов
            if instance.fairy_tale_status in ['ready', 'delivered']:
                send_order_email(
                    order=instance.order,
                    template_type='fairy_tale_ready',
                    recipient_email=instance.order.email,
                    context={'order_item': instance}
                )
                
                logger.info(f"Fairy tale ready email sent for order {instance.order.short_id}")
                
        except Exception as e:
            logger.error(f"Failed to send fairy tale ready email: {e}")
