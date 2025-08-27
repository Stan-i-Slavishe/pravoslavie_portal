# core/context_processors.py
# Контекстные процессоры для добавления переменных во все шаблоны

from django.conf import settings

def cart_context(request):
    """Добавляет информацию о корзине в контекст всех шаблонов"""
    cart_count = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            from shop.models import Cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_count = cart.items.count()
            cart_total = cart.get_total_price()
        except ImportError:
            # Если модель корзины не доступна
            pass
        except Exception:
            # На случай ошибок БД
            pass
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }

def analytics_context(request):
    """Добавляет аналитические переменные в контекст"""
    return {
        'ANALYTICS_ENABLED': getattr(settings, 'ANALYTICS_ENABLED', False),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        'YANDEX_METRIKA_ID': getattr(settings, 'YANDEX_METRIKA_ID', ''),
    }

def site_context(request):
    """Добавляет общие переменные сайта"""
    return {
        'SITE_NAME': 'Добрые истории',
        'SITE_DESCRIPTION': 'Православный портал с духовными рассказами, книгами и терапевтическими сказками',
        'SITE_URL': request.build_absolute_uri('/'),
        'CURRENT_PATH': request.path,
        'DEBUG': settings.DEBUG,
    }
