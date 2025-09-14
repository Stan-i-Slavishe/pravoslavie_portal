# shop/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """
    Отправляет email подтверждение заказа покупателю
    """
    try:
        if not order.user.email:
            logger.warning(f"No email for order {order.id}")
            return False
        
        # Контекст для шаблона
        context = {
            'order': order,
            'site_name': 'Православный портал',
            'site_url': 'https://dobrist.com',
        }
        
        # Рендерим тему письма
        subject = render_to_string('shop/email/order_confirmation_subject.txt', context).strip()
        
        # Рендерим содержание письма
        message = render_to_string('shop/email/order_confirmation_message.txt', context)
        
        # Отправляем email
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False
        )
        
        if result:
            logger.info(f"Order confirmation email sent for order {order.id}")
            return True
        else:
            logger.error(f"Failed to send email for order {order.id}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending order confirmation email: {e}")
        return False


def send_order_email(order, template_type='order_confirmation', recipient_email=None):
    """
    Универсальная функция для отправки email уведомлений о заказах
    Для совместимости со старым кодом
    """
    if template_type == 'order_confirmation':
        return send_order_confirmation_email(order)
    else:
        logger.warning(f"Unknown email template type: {template_type}")
        return False


def send_welcome_email(user_email, activation_url):
    """
    Отправляет приветственное письмо при регистрации
    """
    try:
        context = {
            'activate_url': activation_url,
            'site_name': 'Православный портал',
            'site_url': 'https://dobrist.com',
        }
        
        # Рендерим тему письма
        subject = render_to_string('registration/email/email_confirmation_subject.txt', context).strip()
        
        # Рендерим содержание письма
        message = render_to_string('registration/email/email_confirmation_message.txt', context)
        
        # Отправляем email
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False
        )
        
        if result:
            logger.info(f"Welcome email sent to {user_email}")
            return True
        else:
            logger.error(f"Failed to send welcome email to {user_email}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending welcome email: {e}")
        return False