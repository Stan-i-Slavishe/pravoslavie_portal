"""
Система защиты от DDoS и различных атак
"""
import time
import logging
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
import hashlib
import re

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    """
    Комплексная система защиты от различных атак
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Настройки защиты (можно выносить в settings.py)
        self.rate_limits = {
            'requests_per_minute': 60,      # Запросов в минуту для обычных пользователей
            'requests_per_hour': 1000,      # Запросов в час
            'mobile_feedback_per_hour': 10, # Мобильная обратная связь в час
            'login_attempts_per_hour': 10,  # Попытки входа в час
            'suspicious_patterns_per_hour': 5, # Подозрительные паттерны
        }
        
        # Подозрительные паттерны в URL и данных
        self.suspicious_patterns = [
            r'\.\./',           # Path traversal
            r'<script',         # XSS attempts
            r'javascript:',     # XSS attempts
            r'union.*select',   # SQL injection
            r'drop.*table',     # SQL injection
            r'exec\(',          # Code injection
            r'eval\(',          # Code injection
            r'system\(',        # Command injection
            r'\.php',           # PHP file attempts
            r'\.asp',           # ASP file attempts
            r'\.jsp',           # JSP file attempts
            r'wp-admin',        # WordPress admin attempts
            r'phpmyadmin',      # phpMyAdmin attempts
            r'\.env',           # Environment file attempts
            r'\.git',           # Git directory attempts
            r'admin\.php',      # Admin PHP attempts
        ]
        
        super().__init__(get_response)
    
    def process_request(self, request):
        """Обработка входящих запросов"""
        
        # Получаем IP адрес клиента
        client_ip = self.get_client_ip(request)
        
        # Проверяем подозрительные паттерны
        if self.check_suspicious_patterns(request):
            logger.warning(f"Подозрительный запрос от {client_ip}: {request.path}")
            return self.block_request(client_ip, "Suspicious patterns detected")
        
        # Проверяем rate limiting
        if self.check_rate_limits(request, client_ip):
            logger.warning(f"Rate limit превышен для {client_ip}")
            return self.block_request(client_ip, "Rate limit exceeded")
        
        # Проверяем специфичные API endpoints
        if self.check_api_limits(request, client_ip):
            logger.warning(f"API rate limit превышен для {client_ip} на {request.path}")
            return self.block_request(client_ip, "API rate limit exceeded")
        
        return None
    
    def get_client_ip(self, request):
        """Получение реального IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_suspicious_patterns(self, request):
        """Проверка на подозрительные паттерны"""
        # Проверяем URL
        full_url = request.get_full_path().lower()
        
        # Проверяем POST данные
        post_data = ""
        if request.method == 'POST':
            try:
                post_data = str(request.body.decode('utf-8', errors='ignore')).lower()
            except:
                pass
        
        # Проверяем User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        combined_data = f"{full_url} {post_data} {user_agent}"
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, combined_data, re.IGNORECASE):
                return True
        
        return False
    
    def check_rate_limits(self, request, client_ip):
        """Проверка общих ограничений по скорости"""
        current_time = int(time.time())
        
        # Ключи для кеширования
        minute_key = f"rate_limit:{client_ip}:{current_time // 60}"
        hour_key = f"rate_limit_hour:{client_ip}:{current_time // 3600}"
        
        # Получаем текущие счетчики
        minute_count = cache.get(minute_key, 0)
        hour_count = cache.get(hour_key, 0)
        
        # Проверяем лимиты
        if minute_count >= self.rate_limits['requests_per_minute']:
            return True
        
        if hour_count >= self.rate_limits['requests_per_hour']:
            return True
        
        # Увеличиваем счетчики
        cache.set(minute_key, minute_count + 1, 60)  # TTL 60 секунд
        cache.set(hour_key, hour_count + 1, 3600)    # TTL 1 час
        
        return False
    
    def check_api_limits(self, request, client_ip):
        """Проверка лимитов для специфичных API endpoints"""
        current_time = int(time.time())
        hour_key_base = f"api_limit:{client_ip}:{current_time // 3600}"
        
        # Мобильная обратная связь
        if '/api/mobile-feedback/' in request.path:
            feedback_key = f"{hour_key_base}:mobile_feedback"
            feedback_count = cache.get(feedback_key, 0)
            
            if feedback_count >= self.rate_limits['mobile_feedback_per_hour']:
                return True
            
            cache.set(feedback_key, feedback_count + 1, 3600)
        
        # Попытки входа
        if '/accounts/login/' in request.path or '/admin/login/' in request.path:
            login_key = f"{hour_key_base}:login"
            login_count = cache.get(login_key, 0)
            
            if login_count >= self.rate_limits['login_attempts_per_hour']:
                return True
            
            cache.set(login_key, login_count + 1, 3600)
        
        return False
    
    def block_request(self, client_ip, reason):
        """Блокировка запроса"""
        # Записываем в лог
        logger.error(f"Заблокирован запрос от {client_ip}: {reason}")
        
        # Добавляем IP в blacklist на час
        blacklist_key = f"blacklist:{client_ip}"
        cache.set(blacklist_key, reason, 3600)
        
        # Возвращаем 429 Too Many Requests
        return JsonResponse({
            'error': 'Too many requests',
            'message': 'Ваш IP адрес временно заблокирован из-за подозрительной активности',
            'blocked_until': time.time() + 3600  # Заблокирован на час
        }, status=429)
    
    def process_response(self, request, response):
        """Обработка ответов"""
        # Добавляем security заголовки
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (базовый)
        if not response.get('Content-Security-Policy'):
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https:; "
                "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )
        
        return response


class BlacklistMiddleware(MiddlewareMixin):
    """Middleware для проверки черного списка IP"""
    
    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        
        # Проверяем, есть ли IP в blacklist
        blacklist_key = f"blacklist:{client_ip}"
        blocked_reason = cache.get(blacklist_key)
        
        if blocked_reason:
            logger.warning(f"Заблокированный IP {client_ip} пытается получить доступ")
            
            return JsonResponse({
                'error': 'Access denied',
                'message': f'Ваш IP адрес заблокирован: {blocked_reason}',
                'contact': 'Если вы считаете это ошибкой, обратитесь к администратору'
            }, status=403)
        
        return None
    
    def get_client_ip(self, request):
        """Получение реального IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class MonitoringMiddleware(MiddlewareMixin):
    """Middleware для мониторинга и логирования"""
    
    def process_request(self, request):
        request.start_time = time.time()
        
        # Логируем все POST запросы
        if request.method == 'POST':
            client_ip = self.get_client_ip(request)
            logger.info(f"POST запрос от {client_ip} к {request.path}")
    
    def process_response(self, request, response):
        # Логируем медленные запросы
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            if duration > 2.0:  # Запросы дольше 2 секунд
                client_ip = self.get_client_ip(request)
                logger.warning(f"Медленный запрос ({duration:.2f}s) от {client_ip} к {request.path}")
        
        # Логируем ошибки
        if response.status_code >= 400:
            client_ip = self.get_client_ip(request)
            logger.error(f"Ошибка {response.status_code} от {client_ip} к {request.path}")
        
        return response
    
    def get_client_ip(self, request):
        """Получение реального IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip