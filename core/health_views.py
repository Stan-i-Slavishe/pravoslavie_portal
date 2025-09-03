# 🩺 Православный портал - Health Check Views
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.core.cache import cache
import redis
import json
from datetime import datetime
import os

class HealthCheckView(View):
    """
    🩺 Health check endpoint for monitoring
    Returns system status and health information
    """
    
    def get(self, request):
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0',
            'checks': {}
        }
        
        # 🗄️ Database Health Check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                health_data['checks']['database'] = {
                    'status': 'healthy',
                    'response_time_ms': self._measure_db_response_time()
                }
        except Exception as e:
            health_data['status'] = 'unhealthy'
            health_data['checks']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # 🚀 Redis Health Check
        try:
            cache.set('health_check', 'ok', 30)
            value = cache.get('health_check')
            if value == 'ok':
                health_data['checks']['redis'] = {'status': 'healthy'}
            else:
                raise Exception('Redis test failed')
        except Exception as e:
            health_data['status'] = 'unhealthy'
            health_data['checks']['redis'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # 📁 Disk Space Check
        try:
            disk_usage = self._get_disk_usage()
            if disk_usage['percent'] < 90:
                health_data['checks']['disk'] = {
                    'status': 'healthy',
                    'usage_percent': disk_usage['percent'],
                    'free_gb': disk_usage['free_gb']
                }
            else:
                health_data['status'] = 'unhealthy'
                health_data['checks']['disk'] = {
                    'status': 'unhealthy',
                    'usage_percent': disk_usage['percent'],
                    'free_gb': disk_usage['free_gb'],
                    'error': 'Low disk space'
                }
        except Exception as e:
            health_data['checks']['disk'] = {
                'status': 'unknown',
                'error': str(e)
            }
        
        # 🌐 Environment Info
        health_data['environment'] = {
            'debug': os.environ.get('DEBUG', 'False'),
            'allowed_hosts': os.environ.get('ALLOWED_HOSTS', '').split(','),
            'django_version': self._get_django_version(),
            'python_version': self._get_python_version()
        }
        
        # 📊 Application Stats
        health_data['stats'] = {
            'uptime_seconds': self._get_uptime(),
            'active_connections': self._get_active_connections()
        }
        
        # 🎯 Return appropriate HTTP status
        status_code = 200 if health_data['status'] == 'healthy' else 503
        
        return JsonResponse(health_data, status=status_code)
    
    def _measure_db_response_time(self):
        """Measure database response time"""
        import time
        start = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            end = time.time()
            return round((end - start) * 1000, 2)  # milliseconds
        except:
            return None
    
    def _get_disk_usage(self):
        """Get disk usage statistics"""
        import shutil
        total, used, free = shutil.disk_usage('/')
        percent = (used / total) * 100
        return {
            'percent': round(percent, 2),
            'free_gb': round(free / (1024**3), 2)
        }
    
    def _get_django_version(self):
        """Get Django version"""
        import django
        return django.get_version()
    
    def _get_python_version(self):
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _get_uptime(self):
        """Get application uptime (simplified)"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            return round(uptime_seconds, 2)
        except:
            return None
    
    def _get_active_connections(self):
        """Get active database connections"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_activity 
                    WHERE datname = current_database()
                """)
                return cursor.fetchone()[0]
        except:
            return None

class ReadinessCheckView(View):
    """
    ⚡ Readiness check for Kubernetes/Docker
    Quick check if application is ready to serve traffic
    """
    
    def get(self, request):
        try:
            # Quick database check
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            # Quick cache check
            cache.set('readiness_check', 'ok', 5)
            if cache.get('readiness_check') != 'ok':
                raise Exception('Cache not ready')
            
            return JsonResponse({
                'status': 'ready',
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'not_ready',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }, status=503)

class LivenessCheckView(View):
    """
    💓 Liveness check for Kubernetes/Docker
    Basic check if application is alive
    """
    
    def get(self, request):
        return JsonResponse({
            'status': 'alive',
            'timestamp': datetime.utcnow().isoformat()
        })
