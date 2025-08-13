"""
🛡️ Усиленная система защиты от DDoS, инъекций и других атак
Православный портал - комплексная защита
"""
import time
import logging
import re
import hashlib
import ipaddress
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('security')

class AdvancedSecurityMiddleware(MiddlewareMixin):
    """
    🔥 Продвинутая система защиты от DDoS, инъекций и других атак
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Получаем настройки из Django settings или используем дефолтные
        self.rate_limits = getattr(settings, 'SECURITY_RATE_LIMITS', {
            'requests_per_minute': 60,
            'requests_per_hour': 1000,
            'mobile_feedback_per_hour': 10,
            'login_attempts_per_hour': 10,
            'admin_attempts_per_hour': 5,
            'api_requests_per_minute': 30,
        })
        
        # 🚨 Подозрительные паттерны (расширенный список)
        self.suspicious_patterns = [
            # Path traversal
            r'\.\./',
            r'\.\.\\',
            r'\/\.\.\/',
            r'\\\.\.\\',
            
            # XSS attempts
            r'<script[^>]*>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'<iframe[^>]*>',
            
            # SQL injection
            r'union\s+select',
            r'drop\s+table',
            r'delete\s+from',
            r'insert\s+into',
            r'update\s+.*set',
            r'exec\s*\(',
            r'sp_executesql',
            r'xp_cmdshell',
            
            # Code injection
            r'eval\s*\(',
            r'system\s*\(',
            r'exec\s*\(',
            r'passthru\s*\(',
            r'shell_exec\s*\(',
            r'base64_decode\s*\(',
            
            # File inclusion
            r'include\s*\(',
            r'require\s*\(',
            r'file_get_contents\s*\(',
            r'fopen\s*\(',
            r'readfile\s*\(',
            
            # Admin/sensitive paths
            r'wp-admin',
            r'wp-login',
            r'phpmyadmin',
            r'admin\.php',
            r'config\.php',
            r'\.env',
            r'\.git',
            r'\.svn',
            r'backup\.sql',
            r'database\.sql',
            
            # File types that shouldn't be accessed
            r'\.php\d*$',
            r'\.asp$',
            r'\.aspx$',
            r'\.jsp$',
            r'\.cgi$',
            r'\.pl$',
            r'\.py$',
            r'\.sh$',
            r'\.bat$',
            
            # Suspicious parameters
            r'cmd\s*=',
            r'exec\s*=',
            r'command\s*=',
            r'shell\s*=',
            r'file\s*=.*\.\.',
        ]
        
        # 🤖 Whitelist для поисковых ботов
        self.bot_whitelist = [
            'googlebot',
            'bingbot',
            'yandexbot',
            'slurp',
            'facebookexternalhit',
            'twitterbot',
            'linkedinbot',
        ]
        
        super().__init__(get_response)
    
    def process_request(self, request):
        """🛡️ Главная обработка запросов"""
        
        # Получаем IP клиента
        client_ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Проверяем whitelist для ботов
        if self.is_whitelisted_bot(user_agent):
            return None
        
        # Проверяем blacklist
        if self.is_blacklisted(client_ip):
            return self.block_request(client_ip, "IP in blacklist")
        
        # Проверяем подозрительные паттерны
        if self.detect_suspicious_patterns(request):
            logger.warning(f"SUSPICIOUS PATTERNS DETECTED from {client_ip}: {request.path}")
            return self.block_request(client_ip, "Suspicious patterns detected", severity="high")
        
        # Проверяем размер запроса
        if self.check_request_size(request):
            logger.warning(f"🚨 Oversized request from {client_ip}: {len(request.body)} bytes")
            return self.block_request(client_ip, "Request too large")
        
        # Rate limiting
        if self.check_rate_limits(request, client_ip):
            logger.warning(f"⚠️ Rate limit exceeded for {client_ip}")
            return self.rate_limit_response(client_ip)
        
        # Специфичные проверки API
        if self.check_api_limits(request, client_ip):
            logger.warning(f"⚠️ API rate limit exceeded for {client_ip} on {request.path}")
            return self.rate_limit_response(client_ip, "API rate limit exceeded")
        
        return None
    
    def get_client_ip(self, request):
        """📍 Получение реального IP адреса"""
        # Проверяем различные заголовки
        headers = [
            'HTTP_CF_CONNECTING_IP',      # Cloudflare
            'HTTP_X_FORWARDED_FOR',       # Standard
            'HTTP_X_REAL_IP',             # Nginx
            'HTTP_X_FORWARDED',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_FORWARDED_FOR',
            'HTTP_FORWARDED',
            'REMOTE_ADDR'                 # Fallback
        ]
        
        for header in headers:
            ip = request.META.get(header)
            if ip:
                # X-Forwarded-For может содержать несколько IP
                ip = ip.split(',')[0].strip()
                if self.is_valid_ip(ip):
                    return ip
        
        return request.META.get('REMOTE_ADDR', 'unknown')
    
    def is_valid_ip(self, ip):
        """✅ Проверка валидности IP адреса"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def is_whitelisted_bot(self, user_agent):
        """🤖 Проверка, является ли запрос от поискового бота"""
        return any(bot in user_agent for bot in self.bot_whitelist)
    
    def is_blacklisted(self, client_ip):
        """🚫 Проверка IP в черном списке"""
        blacklist_key = f"blacklist:{client_ip}"
        return cache.get(blacklist_key) is not None
    
    def detect_suspicious_patterns(self, request):
        """🔍 Детекция подозрительных паттернов"""
        # Получаем данные для анализа
        url = request.get_full_path()
        
        # POST данные
        post_data = ""
        if request.method == 'POST':
            try:
                post_data = request.body.decode('utf-8', errors='ignore')
            except:
                pass
        
        # GET параметры
        get_params = request.GET.urlencode()
        
        # Заголовки
        suspicious_headers = ['HTTP_USER_AGENT', 'HTTP_REFERER', 'HTTP_COOKIE']
        headers_data = ' '.join([
            request.META.get(header, '') for header in suspicious_headers
        ])
        
        # Объединяем все данные
        combined_data = f"{url} {post_data} {get_params} {headers_data}".lower()
        
        # Проверяем каждый паттерн
        for pattern in self.suspicious_patterns:
            if re.search(pattern, combined_data, re.IGNORECASE):
                logger.error(f"SUSPICIOUS PATTERN: {pattern} in data from {self.get_client_ip(request)}")
                return True
        
        return False
    
    def check_request_size(self, request):
        """📏 Проверка размера запроса"""
        max_size = 10 * 1024 * 1024  # 10MB
        
        content_length = request.META.get('CONTENT_LENGTH')
        if content_length:
            try:
                if int(content_length) > max_size:
                    return True
            except ValueError:
                pass
        
        # Проверяем размер body
        if hasattr(request, 'body') and len(request.body) > max_size:
            return True
        
        return False
    
    def check_rate_limits(self, request, client_ip):
        """⏱️ Общие лимиты скорости"""
        current_time = int(time.time())
        
        # Минутные лимиты
        minute_key = f"rate:{client_ip}:{current_time // 60}"
        minute_count = cache.get(minute_key, 0)
        
        if minute_count >= self.rate_limits['requests_per_minute']:
            return True
        
        # Часовые лимиты
        hour_key = f"rate_hour:{client_ip}:{current_time // 3600}"
        hour_count = cache.get(hour_key, 0)
        
        if hour_count >= self.rate_limits['requests_per_hour']:
            return True
        
        # Увеличиваем счетчики
        cache.set(minute_key, minute_count + 1, 60)
        cache.set(hour_key, hour_count + 1, 3600)
        
        return False
    
    def check_api_limits(self, request, client_ip):
        """🔌 Специфичные API лимиты"""
        current_time = int(time.time())
        
        # Мобильная обратная связь
        if '/api/mobile-feedback/' in request.path:
            key = f"api_feedback:{client_ip}:{current_time // 3600}"
            count = cache.get(key, 0)
            
            if count >= self.rate_limits.get('mobile_feedback_per_hour', 10):
                return True
            
            cache.set(key, count + 1, 3600)
        
        # Формы входа
        if any(path in request.path for path in ['/accounts/login/', '/admin/login/']):
            key = f"login_attempts:{client_ip}:{current_time // 3600}"
            count = cache.get(key, 0)
            
            limit = self.rate_limits.get('admin_attempts_per_hour' if '/admin/' in request.path else 'login_attempts_per_hour', 10)
            
            if count >= limit:
                return True
            
            cache.set(key, count + 1, 3600)
        
        # API запросы
        if request.path.startswith('/api/'):
            key = f"api_requests:{client_ip}:{current_time // 60}"
            count = cache.get(key, 0)
            
            if count >= self.rate_limits.get('api_requests_per_minute', 30):
                return True
            
            cache.set(key, count + 1, 60)
        
        return False
    
    def block_request(self, client_ip, reason, severity="medium"):
        """🚫 Блокировка IP адреса"""
        # Определяем время блокировки в зависимости от серьезности
        block_times = {
            "low": 300,      # 5 минут
            "medium": 3600,  # 1 час
            "high": 86400,   # 24 часа
            "critical": 604800  # 7 дней
        }
        
        block_time = block_times.get(severity, 3600)
        
        # Добавляем в blacklist
        blacklist_key = f"blacklist:{client_ip}"
        cache.set(blacklist_key, {
            'reason': reason,
            'severity': severity,
            'blocked_at': time.time(),
            'blocked_until': time.time() + block_time
        }, block_time)
        
        # Логируем
        logger.error(f"BLOCKED IP {client_ip}: {reason} (severity: {severity}, duration: {block_time}s)")
        
        # Возвращаем ответ
        return JsonResponse({
            'error': 'Access Denied',
            'message': 'Ваш IP адрес заблокирован из-за подозрительной активности',
            'code': 'SECURITY_BLOCK',
            'blocked_until': time.time() + block_time,
            'contact': 'Если вы считаете это ошибкой, обратитесь к администратору'
        }, status=403)
    
    def rate_limit_response(self, client_ip, message="Rate limit exceeded"):
        """🚦 Ответ при превышении лимитов"""
        logger.warning(f"RATE LIMITED IP {client_ip}: {message}")
        
        return JsonResponse({
            'error': 'Too Many Requests',
            'message': 'Слишком много запросов. Пожалуйста, попробуйте позже.',
            'code': 'RATE_LIMIT',
            'retry_after': 60
        }, status=429)
    
    def process_response(self, request, response):
        """🔒 Добавление security заголовков"""
        
        # Базовые security заголовки
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }
        
        for header, value in security_headers.items():
            if not response.get(header):
                response[header] = value
        
        # Content Security Policy
        if not response.get('Content-Security-Policy'):
            csp_directives = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
                "img-src 'self' data: https:",
                "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
                "connect-src 'self'",
                "frame-ancestors 'none'",
                "base-uri 'self'",
                "form-action 'self'",
                "upgrade-insecure-requests"
            ]
            response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        return response


class MonitoringMiddleware(MiddlewareMixin):
    """📊 Middleware для мониторинга и логирования"""
    
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
                logger.warning(f"SLOW REQUEST ({duration:.2f}s) от {client_ip} к {request.path}")
        
        # Логируем ошибки
        if response.status_code >= 400:
            client_ip = self.get_client_ip(request)
            logger.error(f"ERROR {response.status_code} от {client_ip} к {request.path}")
        
        return response
    
    def get_client_ip(self, request):
        """📍 Получение реального IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlacklistMiddleware(MiddlewareMixin):
    """🚫 Middleware для проверки черного списка IP"""
    
    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        
        # Проверяем, есть ли IP в blacklist
        blacklist_key = f"blacklist:{client_ip}"
        blocked_reason = cache.get(blacklist_key)
        
        if blocked_reason:
            logger.warning(f"BLOCKED IP {client_ip} trying to access")
            
            return JsonResponse({
                'error': 'Access denied',
                'message': f'Ваш IP адрес заблокирован: {blocked_reason.get("reason", "Unknown")}',
                'contact': 'Если вы считаете это ошибкой, обратитесь к администратору'
            }, status=403)
        
        return None
    
    def get_client_ip(self, request):
        """📍 Получение реального IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
