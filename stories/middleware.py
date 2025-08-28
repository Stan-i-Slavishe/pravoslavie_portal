from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import time


class AdminPerformanceMiddleware(MiddlewareMixin):
    """Middleware для ускорения работы админки"""
    
    def process_request(self, request):
        # Только для админки
        if not request.path.startswith('/admin/'):
            return None
        
        # Устанавливаем параметры для оптимизации
        request.admin_optimized = True
        request.start_time = time.time()
        
        # Простое кеширование для GET запросов
        if (request.method == 'GET' and 
            'stories/story/' in request.path):
            
            cache_key = f"admin_stories_list_{request.GET.urlencode()}"
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response
    
    def process_response(self, request, response):
        # Добавляем информацию о времени выполнения
        if hasattr(request, 'start_time'):
            execution_time = time.time() - request.start_time
            if execution_time > 1.0:  # Если запрос выполнялся дольше секунды
                print(f"⚠️ Медленный запрос админки: {request.path} - {execution_time:.2f}с")
        
        # Простое кеширование ответов
        if (hasattr(request, 'admin_optimized') and 
            request.method == 'GET' and 
            response.status_code == 200 and
            'stories/story/' in request.path):
            
            cache_key = f"admin_stories_list_{request.GET.urlencode()}"
            cache.set(cache_key, response, 300)  # 5 минут
        
        return response


class DatabaseOptimizationMiddleware(MiddlewareMixin):
    """Middleware для оптимизации работы с базой данных"""
    
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Для админки используем базовые настройки
            # Убираем проблемные настройки MAX_CONNS для SQLite
            pass
    
    def process_response(self, request, response):
        return response
