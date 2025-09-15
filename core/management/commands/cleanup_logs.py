# 🧹 Команда очистки логов
# Сохранить как: core/management/commands/cleanup_logs.py

from django.core.management.base import BaseCommand
from django.conf import settings
import os
import glob
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Очистка старых логов'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Удалить логи старше указанного количества дней (по умолчанию: 30)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать какие файлы будут удалены, но не удалять их',
        )
    
    def handle(self, *args, **options):
        """Очистка старых логов"""
        days = options['days']
        dry_run = options['dry_run']
        
        self.stdout.write(f'🧹 {"Проверка" if dry_run else "Очистка"} логов старше {days} дней...')
        
        logs_dir = getattr(settings, 'LOGS_DIR', '/app/logs/')
        if not os.path.exists(logs_dir):
            self.stdout.write(self.style.WARNING(f'Директория логов не найдена: {logs_dir}'))
            return
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        freed_space = 0
        
        # Найти все лог файлы
        log_patterns = [
            '*.log',
            '*.log.*',
            '*.json',
            '*.out',
            '*.err'
        ]
        
        for pattern in log_patterns:
            for log_file in glob.glob(os.path.join(logs_dir, pattern)):
                try:
                    file_stat = os.stat(log_file)
                    file_date = datetime.fromtimestamp(file_stat.st_mtime)
                    
                    if file_date < cutoff_date:
                        file_size = file_stat.st_size
                        
                        if dry_run:
                            self.stdout.write(f'   Будет удален: {log_file} ({file_size} байт)')
                        else:
                            os.remove(log_file)
                            self.stdout.write(f'   Удален: {log_file}')
                        
                        deleted_count += 1
                        freed_space += file_size
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка с файлом {log_file}: {e}'))
        
        if deleted_count > 0:
            freed_mb = freed_space / (1024 * 1024)
            action = "будет освобождено" if dry_run else "освобождено"
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ {"Найдено" if dry_run else "Удалено"} {deleted_count} файлов, '
                    f'{action} {freed_mb:.2f} МБ'
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS('✅ Старых логов не найдено'))
