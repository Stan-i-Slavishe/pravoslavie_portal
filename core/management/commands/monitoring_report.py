# 📊 Команда создания отчета мониторинга
# Сохранить как: core/management/commands/monitoring_report.py

import json
import psutil
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Создание отчета мониторинга'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Период для отчета в часах (по умолчанию: 24)',
        )
        parser.add_argument(
            '--email',
            action='store_true',
            help='Отправить отчет по email',
        )
        parser.add_argument(
            '--save',
            type=str,
            help='Сохранить отчет в файл',
        )
    
    def handle(self, *args, **options):
        """Создание отчета мониторинга"""
        hours = options['hours']
        
        self.stdout.write(f'📊 Создание отчета за последние {hours} часов...')
        
        report_data = self.collect_metrics(hours)
        report_text = self.generate_report(report_data, hours)
        
        if options['save']:
            with open(options['save'], 'w', encoding='utf-8') as f:
                f.write(report_text)
            self.stdout.write(f'💾 Отчет сохранен в {options["save"]}')
        
        if options['email']:
            self.send_email_report(report_text, hours)
        
        # Вывод в консоль
        self.stdout.write('\n' + report_text)
    
    def collect_metrics(self, hours):
        """Сбор метрик за указанный период"""
        now = datetime.now()
        metrics = {
            'system': self.get_current_system_metrics(),
            'requests': [],
            'errors': [],
            'hourly_stats': {}
        }
        
        # Собираем данные за каждый час
        for i in range(hours):
            hour = now - timedelta(hours=i)
            hour_key = hour.strftime('%Y%m%d_%H')
            
            hour_metrics = cache.get(f"metrics_{hour_key}", {})
            if hour_metrics:
                metrics['hourly_stats'][hour_key] = hour_metrics
        
        # Последние запросы
        metrics['requests'] = cache.get('recent_requests', [])[-50:]
        
        return metrics
    
    def get_current_system_metrics(self):
        """Получение текущих системных метрик"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100,
            'load_average': psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0,
        }
    
    def generate_report(self, data, hours):
        """Генерация текстового отчета"""
        report = f"""
🔍 ОТЧЕТ МОНИТОРИНГА ПРАВОСЛАВНОГО ПОРТАЛА
{'=' * 50}
📅 Период: {datetime.now().strftime('%Y-%m-%d %H:%M')} (последние {hours} часов)

📊 ТЕКУЩИЕ СИСТЕМНЫЕ МЕТРИКИ:
   CPU: {data['system']['cpu_percent']:.1f}%
   Память: {data['system']['memory_percent']:.1f}%
   Диск: {data['system']['disk_percent']:.1f}%
   Загрузка: {data['system']['load_average']:.2f}

📈 СТАТИСТИКА ЗА ПЕРИОД:
"""
        
        if data['hourly_stats']:
            total_requests = sum(stats.get('total_requests', 0) for stats in data['hourly_stats'].values())
            total_errors = sum(stats.get('error_count', 0) for stats in data['hourly_stats'].values())
            avg_response_times = [stats.get('avg_response_time', 0) for stats in data['hourly_stats'].values() if stats.get('avg_response_time')]
            
            avg_response_time = sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0
            error_rate = (total_errors / max(total_requests, 1)) * 100
            
            report += f"""   Всего запросов: {total_requests}
   Всего ошибок: {total_errors}
   Процент ошибок: {error_rate:.2f}%
   Среднее время ответа: {avg_response_time:.3f}с
"""
        else:
            report += "   Нет данных за указанный период\n"
        
        if data['requests']:
            report += f"""
🕐 ПОСЛЕДНИЕ ЗАПРОСЫ ({len(data['requests'])}):
"""
            for req in data['requests'][-10:]:
                status_emoji = "✅" if req.get('status_code', 0) < 400 else "❌"
                report += f"   {status_emoji} {req.get('method', 'GET')} {req.get('path', 'N/A')} - {req.get('response_time', 0):.3f}с\n"
        
        report += f"""
📝 Отчет создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def send_email_report(self, report_text, hours):
        """Отправка отчета по email"""
        try:
            from django.core.mail import mail_admins
            
            mail_admins(
                subject=f"[Православный портал] Отчет мониторинга за {hours}ч",
                message=report_text,
                fail_silently=False
            )
            
            self.stdout.write(self.style.SUCCESS('📧 Отчет отправлен по email'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка отправки email: {e}'))
