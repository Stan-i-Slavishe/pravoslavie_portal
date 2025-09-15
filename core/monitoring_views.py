# 📊 Views для Dashboard мониторинга
# Создано автоматически для интеграции системы мониторинга

import json
import psutil
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.db import connection
from django.views.decorators.cache import never_cache
from django.conf import settings

@staff_member_required
@never_cache
def monitoring_dashboard(request):
    """Главная страница дашборда мониторинга"""
    return render(request, 'admin/monitoring/dashboard.html', {
        'title': 'Мониторинг системы',
    })

@staff_member_required
def monitoring_api_system(request):
    """API для системных метрик"""
    try:
        # Текущие системные метрики
        data = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'usage': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
            },
            'memory': {
                'percent': psutil.virtual_memory().percent,
                'total': psutil.virtual_memory().total // (1024**3),  # GB
                'available': psutil.virtual_memory().available // (1024**3),  # GB
            },
            'disk': {
                'percent': (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100,
                'total': psutil.disk_usage('/').total // (1024**3),  # GB
                'free': psutil.disk_usage('/').free // (1024**3),  # GB
            },
            'processes': len(psutil.pids()),
        }
        
        # Добавляем load average если доступно
        if hasattr(psutil, 'getloadavg'):
            data['load_average'] = psutil.getloadavg()
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def monitoring_api_database(request):
    """API для метрик базы данных"""
    try:
        # Проверка подключения к БД
        start_time = datetime.now()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_response_time = (datetime.now() - start_time).total_seconds()
        
        # Активные соединения
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE state = 'active' AND pid <> pg_backend_pid()
            """)
            active_connections = cursor.fetchone()[0]
        
        # Размер базы данных
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pg_database_size(current_database())
            """)
            db_size_bytes = cursor.fetchone()[0]
            db_size_mb = db_size_bytes / (1024 * 1024)
        
        # Самые медленные запросы (если доступно)
        slow_queries = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT query, mean_exec_time, calls 
                    FROM pg_stat_statements 
                    ORDER BY mean_exec_time DESC 
                    LIMIT 5
                """)
                slow_queries = [
                    {
                        'query': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
                        'avg_time': round(row[1], 2),
                        'calls': row[2]
                    }
                    for row in cursor.fetchall()
                ]
        except:
            pass  # pg_stat_statements может быть недоступно
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'response_time': round(db_response_time, 3),
            'active_connections': active_connections,
            'database_size_mb': round(db_size_mb, 2),
            'slow_queries': slow_queries,
            'status': 'ok' if db_response_time < 1.0 else 'slow',
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def monitoring_api_cache(request):
    """API для метрик кеша"""
    try:
        # Тест кеша
        test_key = 'monitoring_cache_test'
        test_value = datetime.now().isoformat()
        
        start_time = datetime.now()
        cache.set(test_key, test_value, 60)
        retrieved_value = cache.get(test_key)
        cache_response_time = (datetime.now() - start_time).total_seconds()
        
        # Статистика кеша (если доступна)
        cache_stats = {}
        try:
            # Для Redis
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            info = redis_conn.info()
            
            cache_stats = {
                'connected_clients': info.get('connected_clients', 0),
                'used_memory_human': info.get('used_memory_human', 'N/A'),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
            }
            
            # Вычисляем hit rate
            hits = cache_stats['keyspace_hits']
            misses = cache_stats['keyspace_misses']
            total = hits + misses
            cache_stats['hit_rate'] = round((hits / total * 100), 2) if total > 0 else 0
            
        except:
            pass  # Статистика кеша недоступна
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'response_time': round(cache_response_time, 3),
            'test_successful': retrieved_value == test_value,
            'stats': cache_stats,
            'status': 'ok' if cache_response_time < 0.1 and retrieved_value == test_value else 'slow',
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def monitoring_api_application(request):
    """API для метрик приложения"""
    try:
        current_hour = datetime.now().strftime('%Y%m%d_%H')
        
        # Метрики текущего часа
        hour_metrics = cache.get(f"metrics_{current_hour}", {})
        
        # Ошибки за час
        error_count = cache.get(f"error_count_{current_hour}", 0)
        
        # Последние запросы
        recent_requests = cache.get('recent_requests', [])
        
        # Анализ последних запросов
        if recent_requests:
            last_20 = recent_requests[-20:]
            avg_response_time = sum(req.get('response_time', 0) for req in last_20) / len(last_20)
            
            # Группировка по статус кодам
            status_codes = {}
            for req in last_20:
                code = str(req.get('status_code', 'unknown'))
                status_codes[code] = status_codes.get(code, 0) + 1
        else:
            avg_response_time = 0
            status_codes = {}
        
        # Топ страниц по просмотрам
        page_views = {}
        for req in recent_requests[-100:]:
            path = req.get('path', 'unknown')
            page_views[path] = page_views.get(path, 0) + 1
        
        top_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)[:10]
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'hourly_metrics': hour_metrics,
            'error_count': error_count,
            'recent_requests_count': len(recent_requests),
            'avg_response_time': round(avg_response_time, 3),
            'status_codes': status_codes,
            'top_pages': [{'path': path, 'views': views} for path, views in top_pages],
            'last_requests': recent_requests[-10:] if recent_requests else [],
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def monitoring_api_logs(request):
    """API для просмотра логов"""
    try:
        log_type = request.GET.get('type', 'general')
        lines = int(request.GET.get('lines', 50))
        
        logs_dir = getattr(settings, 'LOGS_DIR', '/app/logs/')
        log_files = {
            'general': 'django.log',
            'errors': 'errors.log',
            'security': 'security.log',
            'shop': 'shop.log',
            'auth': 'auth.log',
        }
        
        log_file = log_files.get(log_type, 'django.log')
        log_path = f"{logs_dir}{log_file}"
        
        log_entries = []
        try:
            # Fallback для чтения файла
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    log_entries = [line.strip() for line in all_lines[-lines:]]
            except Exception as e:
                log_entries = [f"Ошибка чтения файла: {str(e)}"]
                
        except:
            log_entries = ["Лог файл не найден или недоступен"]
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'log_type': log_type,
            'entries': log_entries,
            'count': len(log_entries),
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def monitoring_api_alerts(request):
    """API для управления алертами"""
    try:
        # Получаем текущие алерты из кеша
        alerts = cache.get('monitoring_alerts', [])
        
        # Проверяем текущие пороги
        current_alerts = []
        
        # CPU
        cpu_percent = psutil.cpu_percent()
        if cpu_percent > 80:
            current_alerts.append({
                'type': 'warning',
                'message': f'Высокая нагрузка CPU: {cpu_percent}%',
                'timestamp': datetime.now().isoformat(),
                'category': 'system'
            })
        
        # Память
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 85:
            current_alerts.append({
                'type': 'error',
                'message': f'Критическое использование памяти: {memory_percent}%',
                'timestamp': datetime.now().isoformat(),
                'category': 'system'
            })
        
        # Диск
        disk_percent = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
        if disk_percent > 85:
            current_alerts.append({
                'type': 'warning',
                'message': f'Мало места на диске: {disk_percent:.1f}%',
                'timestamp': datetime.now().isoformat(),
                'category': 'storage'
            })
        
        # Ошибки приложения
        current_hour = datetime.now().strftime('%Y%m%d_%H')
        error_count = cache.get(f"error_count_{current_hour}", 0)
        if error_count > 10:
            current_alerts.append({
                'type': 'error',
                'message': f'Много ошибок за час: {error_count}',
                'timestamp': datetime.now().isoformat(),
                'category': 'application'
            })
        
        # Обновляем кеш алертов
        cache.set('monitoring_alerts', current_alerts, 300)  # 5 минут
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'alerts': current_alerts,
            'count': len(current_alerts),
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Health check views
from django.http import HttpResponse

def health_check(request):
    """Простая проверка здоровья сервиса"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return HttpResponse("OK", content_type="text/plain", status=200)
    except:
        return HttpResponse("ERROR", content_type="text/plain", status=500)

def health_check_detailed(request):
    """Детальная проверка здоровья"""
    from django.db import connection
    from django.core.cache import cache
    import psutil
    from datetime import datetime
    
    health_data = {
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    
    # Проверка БД
    try:
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
            health_data['checks']['cache'] = 'ERROR'
            health_data['status'] = 'WARNING'
    except Exception as e:
        health_data['checks']['cache'] = f'ERROR: {str(e)}'
        health_data['status'] = 'ERROR'
    
    # Проверка системных ресурсов
    try:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
        
        health_data['checks']['resources'] = {
            'cpu': f'{cpu}%',
            'memory': f'{memory}%',
            'disk': f'{disk:.1f}%'
        }
        
        if cpu > 90 or memory > 95 or disk > 95:
            health_data['status'] = 'WARNING'
            
    except Exception as e:
        health_data['checks']['resources'] = f'ERROR: {str(e)}'
    
    status_code = 200 if health_data['status'] == 'OK' else 503
    
    return HttpResponse(
        json.dumps(health_data, ensure_ascii=False, indent=2),
        content_type='application/json',
        status=status_code
    )
