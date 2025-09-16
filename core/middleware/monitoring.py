# 📊 Middleware для мониторинга производительности
# Сохранить как: core/middleware/monitoring.py

import time
import logging
import traceback
import psutil
import json
from datetime import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse

logger = logging.getLogger('monitoring')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware для отслеживания производительности запросов
    """
    
    def process_request(self, request):
        """Начало обработки запроса"""
        request.start_time = time.time()
        request.start_queries = len(connection.queries)
        
        # Записываем начальные метрики
        try:
            request.memory_start = psutil.virtual_memory().percent
        except:
            request.memory_start = 0
        
        return None
    
    def process_response(self, request, response):
        """Обработка ответа и логирование метрик"""
        if not hasattr(request, 'start_time'):
            return response
            
        # Вычисляем метрики
        total_time = time.time() - request.start_time
        total_queries = len(connection.queries) - request.start_queries
        
        try:
            memory_end = psutil.virtual_memory().percent
            memory_used = memory_end - request.memory_start
        except:
            memory_used = 0
        
        # Получаем информацию о пользователе
        user_info = {
            'user_id': request.user.id if request.user.is_authenticated else None,
            'user_email': request.user.email if request.user.is_authenticated else None,
            'is_authenticated': request.user.is_authenticated,
        }
        
        # Формируем данные для логирования
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'response_time': round(total_time, 3),
            'db_queries': total_queries,
            'memory_usage': round(memory_used, 2),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'remote_addr': self.get_client_ip(request),
            'user': user_info,
        }
        
        # Логируем в зависимости от порогов
        if total_time > getattr(settings, 'PERFORMANCE_MONITORING', {}).get('SLOW_QUERY_THRESHOLD', 1.0):
            logger.warning(f"Медленный запрос: {json.dumps(metrics, ensure_ascii=False)}")
        else:
            logger.info(f"Запрос: {json.dumps(metrics, ensure_ascii=False)}")
        
        # Сохраняем метрики в кеш для дашборда
        self.save_metrics_to_cache(metrics)
        
        # Проверяем пороги для алертов
        self.check_performance_alerts(metrics)
        
        return response
    
    def process_exception(self, request, exception):
        """Обработка исключений"""
        if not hasattr(request, 'start_time'):
            return None
            
        total_time = time.time() - request.start_time
        
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'response_time': round(total_time, 3),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': traceback.format_exc(),
            'user_id': request.user.id if request.user.is_authenticated else None,
            'remote_addr': self.get_client_ip(request),
        }
        
        logger.error(f"Ошибка в запросе: {json.dumps(error_data, ensure_ascii=False)}")
        
        # Увеличиваем счетчик ошибок
        cache_key = f"error_count_{datetime.now().strftime('%Y%m%d_%H')}"
        cache.set(cache_key, cache.get(cache_key, 0) + 1, 3600)
        
        return None
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def save_metrics_to_cache(self, metrics):
        """Сохранение метрик в кеш для дашборда"""
        try:
            # Сохраняем последние 100 запросов
            cache_key = 'recent_requests'
            recent_requests = cache.get(cache_key, [])
            recent_requests.append(metrics)
            
            # Оставляем только последние 100
            if len(recent_requests) > 100:
                recent_requests = recent_requests[-100:]
            
            cache.set(cache_key, recent_requests, 3600)  # 1 час
            
            # Агрегированные метрики за час
            hour_key = f"metrics_{datetime.now().strftime('%Y%m%d_%H')}"
            hour_metrics = cache.get(hour_key, {
                'total_requests': 0,
                'avg_response_time': 0,
                'total_response_time': 0,
                'max_response_time': 0,
                'error_count': 0,
                'status_codes': {},
            })
            
            hour_metrics['total_requests'] += 1
            hour_metrics['total_response_time'] += metrics['response_time']
            hour_metrics['avg_response_time'] = hour_metrics['total_response_time'] / hour_metrics['total_requests']
            hour_metrics['max_response_time'] = max(hour_metrics['max_response_time'], metrics['response_time'])
            
            status_code = str(metrics['status_code'])
            hour_metrics['status_codes'][status_code] = hour_metrics['status_codes'].get(status_code, 0) + 1
            
            if metrics['status_code'] >= 400:
                hour_metrics['error_count'] += 1
            
            cache.set(hour_key, hour_metrics, 3600)  # 1 час
            
        except Exception as e:
            logger.error(f"Ошибка сохранения метрик в кеш: {e}")
    
    def check_performance_alerts(self, metrics):
        """Проверка порогов для отправки алертов"""
        try:
            alerts_config = getattr(settings, 'ALERTS_CONFIG', {})
            
            # Проверяем время ответа
            if metrics['response_time'] > alerts_config.get('RESPONSE_TIME_THRESHOLD', 2.0):
                self.send_alert(f"⚠️ Медленный ответ: {metrics['response_time']}s на {metrics['path']}")
            
            # Проверяем количество ошибок за час
            hour_key = f"error_count_{datetime.now().strftime('%Y%m%d_%H')}"
            error_count = cache.get(hour_key, 0)
            
            if error_count > alerts_config.get('ERROR_THRESHOLD', 10):
                alert_sent_key = f"alert_sent_{hour_key}"
                if not cache.get(alert_sent_key):
                    self.send_alert(f"🚨 Много ошибок: {error_count} за час")
                    cache.set(alert_sent_key, True, 3600)
            
        except Exception as e:
            logger.error(f"Ошибка проверки алертов: {e}")
    
    def send_alert(self, message):
        """Отправка алерта администраторам"""
        try:
            # Email алерт
            if getattr(settings, 'ALERTS_CONFIG', {}).get('SEND_EMAIL_ALERTS'):
                from django.core.mail import mail_admins
                mail_admins(
                    subject=f"[Православный портал] Алерт мониторинга",
                    message=f"{message}\n\nВремя: {datetime.now()}",
                    fail_silently=True
                )
            
            # Telegram алерт (если настроен)
            if hasattr(settings, 'TELEGRAM_CONFIG'):
                self.send_telegram_alert(message)
                
        except Exception as e:
            logger.error(f"Ошибка отправки алерта: {e}")
    
    def send_telegram_alert(self, message):
        """Отправка алерта в Telegram"""
        try:
            import requests
            telegram_config = settings.TELEGRAM_CONFIG
            
            url = f"https://api.telegram.org/bot{telegram_config['BOT_TOKEN']}/sendMessage"
            data = {
                'chat_id': telegram_config['CHAT_ID'],
                'text': f"🔔 {message}",
                'parse_mode': 'HTML'
            }
            
            requests.post(url, data=data, timeout=5)
            
        except Exception as e:
            logger.error(f"Ошибка отправки Telegram алерта: {e}")


class SecurityMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware для мониторинга безопасности
    """
    
    def process_request(self, request):
        """Проверка подозрительной активности"""
        client_ip = self.get_client_ip(request)
        
        # Проверяем подозрительные паттерны
        suspicious_patterns = [
            'wp-admin', 'wp-login', '.php', 'admin.php',
            'shell', 'cmd', 'eval', 'exec',
            '../', '..\\', 'etc/passwd'
        ]
        
        path_lower = request.path.lower()
        for pattern in suspicious_patterns:
            if pattern in path_lower:
                self.log_security_event(request, f"Подозрительный путь: {pattern}")
                break
        
        # Проверяем частоту запросов
        self.check_request_frequency(request, client_ip)
        
        return None
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_request_frequency(self, request, client_ip):
        """Проверка частоты запросов (защита от DDoS)"""
        cache_key = f"requests_{client_ip}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        request_count = cache.get(cache_key, 0)
        
        if request_count > 100:  # Лимит запросов в минуту
            self.log_security_event(request, f"Превышение лимита запросов: {request_count}/мин")
        
        cache.set(cache_key, request_count + 1, 60)  # TTL 1 минута
    
    def log_security_event(self, request, event_type):
        """Логирование события безопасности"""
        security_logger = logging.getLogger('django.security')
        
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'method': request.method,
            'path': request.path,
            'remote_addr': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'user_id': request.user.id if request.user.is_authenticated else None,
        }
        
        security_logger.warning(f"Событие безопасности: {json.dumps(event_data, ensure_ascii=False)}")


class HealthCheckMiddleware(MiddlewareMixin):
    """
    Middleware для health check'ов
    """
    
    def process_request(self, request):
        """Обработка health check запросов"""
        if request.path == '/health/':
            return self.health_check()
        elif request.path == '/health/detailed/':
            return self.detailed_health_check()
        return None
    
    def health_check(self):
        """Простая проверка здоровья"""
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return HttpResponse("OK", content_type="text/plain", status=200)
        except:
            return HttpResponse("ERROR", content_type="text/plain", status=500)
    
    def detailed_health_check(self):
        """Детальная проверка здоровья"""
        health_data = {
            'status': 'OK',
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # Проверка базы данных
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_data['checks']['database'] = 'OK'
        except Exception as e:
            health_data['checks']['database'] = f'ERROR: {str(e)}'
            health_data['status'] = 'ERROR'
        
        # Проверка кеша
        try:
            cache.set('health_check', 'test', 60)
            if cache.get('health_check') == 'test':
                health_data['checks']['cache'] = 'OK'
            else:
                health_data['checks']['cache'] = 'ERROR: Cache read/write failed'
                health_data['status'] = 'WARNING'
        except Exception as e:
            health_data['checks']['cache'] = f'ERROR: {str(e)}'
            health_data['status'] = 'ERROR'
        
        # Проверка дискового пространства
        try:
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            if disk_percent < 80:
                health_data['checks']['disk_space'] = f'OK ({disk_percent:.1f}% used)'
            else:
                health_data['checks']['disk_space'] = f'WARNING ({disk_percent:.1f}% used)'
                health_data['status'] = 'WARNING'
        except Exception as e:
            health_data['checks']['disk_space'] = f'ERROR: {str(e)}'
        
        # Проверка памяти
        try:
            memory = psutil.virtual_memory()
            if memory.percent < 85:
                health_data['checks']['memory'] = f'OK ({memory.percent:.1f}% used)'
            else:
                health_data['checks']['memory'] = f'WARNING ({memory.percent:.1f}% used)'
                health_data['status'] = 'WARNING'
        except Exception as e:
            health_data['checks']['memory'] = f'ERROR: {str(e)}'
        
        status_code = 200 if health_data['status'] == 'OK' else 503
        
        return HttpResponse(
            json.dumps(health_data, ensure_ascii=False, indent=2),
            content_type="application/json",
            status=status_code
        )
