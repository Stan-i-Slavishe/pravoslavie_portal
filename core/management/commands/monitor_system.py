# 📊 Команда мониторинга системы
# Сохранить как: core/management/commands/monitor_system.py

import psutil
import logging
import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import connection
from django.conf import settings
from django.core.mail import mail_admins

logger = logging.getLogger('monitoring')

class Command(BaseCommand):
    help = 'Мониторинг системных ресурсов и отправка алертов'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--check-all',
            action='store_true',
            help='Проверить все системные ресурсы',
        )
        parser.add_argument(
            '--send-alerts',
            action='store_true',
            help='Отправлять алерты при превышении порогов',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Подробный вывод информации',
        )
    
    def handle(self, *args, **options):
        """Основная логика команды"""
        self.stdout.write(self.style.SUCCESS('🔍 Запуск системного мониторинга...'))
        
        if options['check_all'] or not any([options['check_all']]):
            self.check_system_resources(options)
            self.check_database_health(options)
            self.check_cache_health(options)
            self.check_disk_space(options)
            self.check_application_metrics(options)
        
        self.stdout.write(self.style.SUCCESS('✅ Мониторинг завершен'))
    
    def check_system_resources(self, options):
        """Проверка системных ресурсов"""
        self.stdout.write('📊 Проверка системных ресурсов...')
        
        # Проверка CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.log_metric('cpu_usage', cpu_percent, '%')
        
        if cpu_percent > 80:
            self.send_alert(f"🔥 Высокая нагрузка CPU: {cpu_percent}%", options)
        
        # Проверка памяти
        memory = psutil.virtual_memory()
        self.log_metric('memory_usage', memory.percent, '%')
        
        if memory.percent > 85:
            self.send_alert(f"🔥 Высокое использование памяти: {memory.percent}%", options)
        
        # Проверка загрузки системы
        try:
            load_avg = psutil.getloadavg()
            self.log_metric('load_average', load_avg[0], '')
        except:
            load_avg = [0, 0, 0]  # Fallback для Windows
        
        if options['verbose']:
            self.stdout.write(f"   CPU: {cpu_percent}%")
            self.stdout.write(f"   Память: {memory.percent}%")
            self.stdout.write(f"   Загрузка: {load_avg[0]}")
    
    def check_database_health(self, options):
        """Проверка здоровья базы данных"""
        self.stdout.write('🗄️ Проверка базы данных...')
        
        try:
            # Проверка подключения
            start_time = datetime.now()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            db_response_time = (datetime.now() - start_time).total_seconds()
            
            self.log_metric('db_response_time', db_response_time, 'сек')
            
            if db_response_time > 1.0:
                self.send_alert(f"🐌 Медленный отклик БД: {db_response_time:.2f}с", options)
            
            # Проверка количества активных соединений
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_activity 
                    WHERE state = 'active' AND pid <> pg_backend_pid()
                """)
                active_connections = cursor.fetchone()[0]
            
            self.log_metric('db_active_connections', active_connections, '')
            
            if active_connections > 80:
                self.send_alert(f"📊 Много активных соединений БД: {active_connections}", options)
            
            # Проверка размера базы данных
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """)
                db_size = cursor.fetchone()[0]
            
            if options['verbose']:
                self.stdout.write(f"   Отклик БД: {db_response_time:.3f}с")
                self.stdout.write(f"   Активные соединения: {active_connections}")
                self.stdout.write(f"   Размер БД: {db_size}")
                
        except Exception as e:
            self.send_alert(f"❌ Ошибка БД: {str(e)}", options)
            logger.error(f"Database health check failed: {e}")
    
    def check_cache_health(self, options):
        """Проверка здоровья кеша"""
        self.stdout.write('🔄 Проверка кеша Redis...')
        
        try:
            # Тест записи/чтения
            test_key = 'health_check_test'
            test_value = datetime.now().isoformat()
            
            start_time = datetime.now()
            cache.set(test_key, test_value, 60)
            retrieved_value = cache.get(test_key)
            cache_response_time = (datetime.now() - start_time).total_seconds()
            
            self.log_metric('cache_response_time', cache_response_time, 'сек')
            
            if retrieved_value != test_value:
                self.send_alert("❌ Кеш не работает корректно", options)
            elif cache_response_time > 0.1:
                self.send_alert(f"🐌 Медленный отклик кеша: {cache_response_time:.3f}с", options)
            
            if options['verbose']:
                self.stdout.write(f"   Отклик кеша: {cache_response_time:.3f}с")
                self.stdout.write(f"   Тест чтения/записи: ✅")
                
        except Exception as e:
            self.send_alert(f"❌ Ошибка кеша: {str(e)}", options)
            logger.error(f"Cache health check failed: {e}")
    
    def check_disk_space(self, options):
        """Проверка дискового пространства"""
        self.stdout.write('💾 Проверка дискового пространства...')
        
        try:
            # Проверка основного диска
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            
            self.log_metric('disk_usage', disk_percent, '%')
            
            if disk_percent > 85:
                self.send_alert(f"💾 Мало места на диске: {disk_percent:.1f}%", options)
            elif disk_percent > 75:
                self.send_alert(f"⚠️ Диск заполняется: {disk_percent:.1f}%", options)
            
            if options['verbose']:
                self.stdout.write(f"   Использование диска: {disk_percent:.1f}%")
                self.stdout.write(f"   Свободно: {disk_usage.free // (1024**3)} ГБ")
                
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
    
    def check_application_metrics(self, options):
        """Проверка метрик приложения"""
        self.stdout.write('📱 Проверка метрик приложения...')
        
        try:
            # Проверка ошибок за последний час
            current_hour = datetime.now().strftime('%Y%m%d_%H')
            error_count = cache.get(f"error_count_{current_hour}", 0)
            
            self.log_metric('hourly_errors', error_count, '')
            
            if error_count > 50:
                self.send_alert(f"🚨 Много ошибок за час: {error_count}", options)
            
            # Проверка последних запросов
            recent_requests = cache.get('recent_requests', [])
            if recent_requests:
                avg_response_time = sum(req.get('response_time', 0) for req in recent_requests[-20:]) / min(20, len(recent_requests))
                self.log_metric('avg_response_time', avg_response_time, 'сек')
                
                if avg_response_time > 2.0:
                    self.send_alert(f"🐌 Медленные запросы: {avg_response_time:.2f}с", options)
            
            # Проверка метрик за час
            hour_metrics = cache.get(f"metrics_{current_hour}", {})
            if hour_metrics:
                total_requests = hour_metrics.get('total_requests', 0)
                error_rate = (hour_metrics.get('error_count', 0) / max(total_requests, 1)) * 100
                
                self.log_metric('hourly_requests', total_requests, '')
                self.log_metric('error_rate', error_rate, '%')
                
                if error_rate > 5:
                    self.send_alert(f"📊 Высокий процент ошибок: {error_rate:.1f}%", options)
            
            if options['verbose']:
                self.stdout.write(f"   Ошибки за час: {error_count}")
                self.stdout.write(f"   Последние запросы: {len(recent_requests)}")
                if recent_requests:
                    avg_response_time = sum(req.get('response_time', 0) for req in recent_requests[-20:]) / min(20, len(recent_requests))
                    self.stdout.write(f"   Среднее время ответа: {avg_response_time:.3f}с")
                
        except Exception as e:
            logger.error(f"Application metrics check failed: {e}")
    
    def log_metric(self, metric_name, value, unit):
        """Логирование метрики"""
        metric_data = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric_name,
            'value': value,
            'unit': unit
        }
        logger.info(f"Метрика: {json.dumps(metric_data, ensure_ascii=False)}")
        
        # Сохранение в кеш для графиков
        cache_key = f"metric_{metric_name}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        cache.set(cache_key, value, 86400)  # 24 часа
    
    def send_alert(self, message, options):
        """Отправка алерта"""
        if not options.get('send_alerts'):
            return
        
        try:
            # Email алерт
            alerts_config = getattr(settings, 'ALERTS_CONFIG', {})
            if alerts_config.get('SEND_EMAIL_ALERTS'):
                mail_admins(
                    subject=f"[Православный портал] Системный алерт",
                    message=f"{message}\n\nВремя: {datetime.now()}",
                    fail_silently=True
                )
            
            # Telegram алерт
            if alerts_config.get('SEND_TELEGRAM_ALERTS') and hasattr(settings, 'TELEGRAM_CONFIG'):
                self.send_telegram_alert(message)
            
            logger.warning(f"Alert sent: {message}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
    
    def send_telegram_alert(self, message):
        """Отправка алерта в Telegram"""
        try:
            import requests
            telegram_config = settings.TELEGRAM_CONFIG
            
            url = f"https://api.telegram.org/bot{telegram_config['BOT_TOKEN']}/sendMessage"
            data = {
                'chat_id': telegram_config['CHAT_ID'],
                'text': f"🔔 <b>Системный алерт</b>\n\n{message}\n\n⏰ {datetime.now().strftime('%H:%M:%S')}",
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=5)
            response.raise_for_status()
            
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
