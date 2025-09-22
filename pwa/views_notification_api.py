# API для управления уведомлениями

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import NotificationCategory
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def get_available_notification_categories(request):
    """Получение списка доступных категорий уведомлений с учетом активности"""
    try:
        # Получаем только АКТИВНЫЕ категории
        active_categories = NotificationCategory.objects.filter(is_active=True)
        
        categories_data = []
        for category in active_categories:
            categories_data.append({
                'name': category.name,
                'title': category.title,
                'description': category.description,
                'icon': category.icon,
                'default_enabled': category.default_enabled,
                'is_active': category.is_active
            })
        
        return JsonResponse({
            'categories': categories_data,
            'total_active': len(categories_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting notification categories: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)
