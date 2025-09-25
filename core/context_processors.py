from django.conf import settings


def maintenance_context(request):
    """
    Context processor для режима обслуживания.
    Добавляет информацию о режиме обслуживания в контекст всех шаблонов.
    """
    from core.models import SiteSettings
    
    context = {
        'is_maintenance_mode': False,
        'is_admin_in_maintenance': False,
        'maintenance_message': '',
    }
    
    # Получаем настройки из базы данных
    try:
        site_settings = SiteSettings.get_settings()
        
        if site_settings.maintenance_mode:
            context['is_maintenance_mode'] = True
            context['maintenance_message'] = site_settings.maintenance_message or 'Сайт находится на техническом обслуживании'
            
            # Проверяем, является ли пользователь администратором
            if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
                context['is_admin_in_maintenance'] = True
    except Exception as e:
        # Если таблица не создана или произошла ошибка, игнорируем
        pass
    
    return context


def cart_context(request):
    """Context processor для корзины покупок"""
    from shop.models import Cart
    
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = cart.items.count()
        except Exception:
            pass
    
    return {
        'cart_count': cart_count,
    }


def site_context(request):
    """Context processor для общих настроек сайта"""
    from core.models import SiteSettings
    
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'site_settings': site_settings,
        }
    except Exception:
        return {
            'site_settings': None,
        }
