from django.shortcuts import render
from django.conf import settings
from django.urls import reverse


class MaintenanceModeMiddleware:
    """
    Middleware для режима технического обслуживания.
    Показывает страницу обслуживания всем пользователям, кроме:
    - Суперпользователей (superuser)
    - Администраторов (staff)
    - IP-адресов из белого списка
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Импортируем здесь, чтобы избежать проблем с инициализацией
        from core.models import SiteSettings
        
        # Проверяем режим обслуживания из базы данных
        try:
            site_settings = SiteSettings.get_settings()
            maintenance_mode = site_settings.maintenance_mode
            maintenance_message = site_settings.maintenance_message or 'Сайт находится на техническом обслуживании. Пожалуйста, зайдите позже.'
        except Exception:
            # Если таблица не создана, режим обслуживания выключен
            maintenance_mode = False
            maintenance_message = 'Сайт находится на техническом обслуживании.'
        
        if not maintenance_mode:
            # Режим обслуживания выключен - пропускаем всех
            response = self.get_response(request)
            return response
        
        # Режим обслуживания включен - проверяем исключения
        
        # 1. ПРИОРИТЕТ: Суперпользователи и администраторы ВСЕГДА имеют доступ
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            response = self.get_response(request)
            return response
        
        # 2. Пути, которые должны быть доступны в режиме обслуживания
        allowed_paths = [
            '/accounts/login/',  # Страница входа на сайт (чтобы админ мог войти)
            '/admin/login/',  # Страница входа в админку
            '/admin/',  # Админка (для уже авторизованных)
            '/static/',  # Статические файлы
            '/media/',  # Медиа файлы
        ]
        
        # Проверяем разрешенные пути
        if any(request.path_info.startswith(path) for path in allowed_paths):
            response = self.get_response(request)
            return response
        
        # 3. Проверка IP-адреса в белом списке (опционально)
        if hasattr(settings, 'MAINTENANCE_MODE_ALLOWED_IPS'):
            client_ip = self.get_client_ip(request)
            if client_ip in settings.MAINTENANCE_MODE_ALLOWED_IPS:
                response = self.get_response(request)
                return response
        
        # Если не прошли ни одну проверку - показываем страницу обслуживания
        return self.show_maintenance_page(request, maintenance_message)
    
    def get_client_ip(self, request):
        """Получение IP-адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def show_maintenance_page(self, request, message):
        """Отображение страницы технического обслуживания"""
        context = {
            'maintenance_message': message,
        }
        return render(request, 'maintenance.html', context, status=503)
