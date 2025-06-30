# shop/utils.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_email(order, template_type, recipient_email, context=None):
    """
    Универсальная функция для отправки email уведомлений о заказах
    
    Args:
        order: Объект заказа
        template_type: Тип шаблона ('order_created', 'order_paid', etc.)
        recipient_email: Email получателя или список email'ов
        context: Дополнительный контекст для шаблона
    """
    try:
        # Базовый контекст
        email_context = {
            'order': order,
            'site_name': 'Православный портал',
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            'support_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'support@pravoslavie-portal.ru'),
        }
        
        # Добавляем дополнительный контекст
        if context:
            email_context.update(context)
        
        # Определяем шаблоны и тему на основе типа
        templates = get_email_templates(template_type)
        
        if not templates:
            logger.error(f"Unknown email template type: {template_type}")
            return False
        
        # Рендерим шаблоны
        html_content = render_to_string(templates['html'], email_context)
        text_content = render_to_string(templates['text'], email_context)
        
        # Формируем тему письма
        subject = templates['subject'].format(
            order_id=order.short_id,
            site_name=email_context['site_name']
        )
        
        # Подготавливаем список получателей
        if isinstance(recipient_email, str):
            recipient_list = [recipient_email]
        else:
            recipient_list = recipient_email
        
        # Создаем и отправляем email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        
        # Отправляем
        result = email.send()
        
        if result:
            logger.info(f"Email sent successfully: {template_type} to {recipient_list}")
            return True
        else:
            logger.error(f"Failed to send email: {template_type} to {recipient_list}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending order email: {e}")
        return False


def get_email_templates(template_type):
    """
    Возвращает пути к шаблонам и тему для разных типов email
    """
    templates = {
        'order_created': {
            'html': 'shop/emails/order_created.html',
            'text': 'shop/emails/order_created.txt',
            'subject': 'Заказ #{order_id} создан - {site_name}'
        },
        'order_created_admin': {
            'html': 'shop/emails/order_created_admin.html',
            'text': 'shop/emails/order_created_admin.txt',
            'subject': 'Новый заказ #{order_id} - {site_name}'
        },
        'order_status_changed': {
            'html': 'shop/emails/order_status_changed.html',
            'text': 'shop/emails/order_status_changed.txt',
            'subject': 'Статус заказа #{order_id} изменен - {site_name}'
        },
        'order_paid_download_instructions': {
            'html': 'shop/emails/order_paid_download.html',
            'text': 'shop/emails/order_paid_download.txt',
            'subject': 'Заказ #{order_id} оплачен - инструкции по скачиванию'
        },
        'order_completed': {
            'html': 'shop/emails/order_completed.html',
            'text': 'shop/emails/order_completed.txt',
            'subject': 'Заказ #{order_id} завершен - {site_name}'
        },
        'fairy_tale_ready': {
            'html': 'shop/emails/fairy_tale_ready.html',
            'text': 'shop/emails/fairy_tale_ready.txt',
            'subject': 'Ваша персонализированная сказка готова! - {site_name}'
        }
    }
    
    return templates.get(template_type)


def get_order_download_links(order):
    """
    Возвращает список ссылок для скачивания товаров из заказа
    """
    download_links = []
    
    for item in order.items.all():
        if item.product.is_digital:
            download_url = f"/shop/download/{item.id}/"
            download_links.append({
                'title': item.product_title,
                'url': download_url,
                'product_type': item.product.get_product_type_display()
            })
    
    return download_links


def format_order_items_for_email(order):
    """
    Форматирует элементы заказа для отображения в email
    """
    items = []
    
    for item in order.items.all():
        item_info = {
            'title': item.product_title,
            'quantity': item.quantity,
            'price': item.product_price,
            'total': item.total_price,
            'type': item.product.get_product_type_display(),
            'is_digital': item.product.is_digital,
            'is_fairy_tale': item.is_fairy_tale,
        }
        
        # Добавляем информацию о персонализации для сказок
        if item.is_fairy_tale and item.personalization_data:
            item_info['personalization'] = item.get_personalization_summary()
            item_info['fairy_tale_status'] = item.fairy_tale_status_display
        
        items.append(item_info)
    
    return items
