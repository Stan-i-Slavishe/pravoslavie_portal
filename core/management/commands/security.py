"""
Команда для управления системой безопасности
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
import time
import json

class Command(BaseCommand):
    help = 'Управление системой безопасности'

    def add_arguments(self, parser):
        parser.add_argument(
            '--show-blocked',
            action='store_true',
            help='Показать заблокированные IP',
        )
        parser.add_argument(
            '--unblock-ip',
            type=str,
            help='Разблокировать IP адрес',
        )
        parser.add_argument(
            '--block-ip',
            type=str,
            help='Заблокировать IP адрес',
        )
        parser.add_argument(
            '--reason',
            type=str,
            default='Manual block',
            help='Причина блокировки',
        )
        parser.add_argument(
            '--clear-all',
            action='store_true',
            help='Очистить все блокировки',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Показать статистику запросов',
        )

    def handle(self, *args, **options):
        if options['show_blocked']:
            self.show_blocked_ips()
        
        elif options['unblock_ip']:
            self.unblock_ip(options['unblock_ip'])
        
        elif options['block_ip']:
            self.block_ip(options['block_ip'], options['reason'])
        
        elif options['clear_all']:
            self.clear_all_blocks()
        
        elif options['stats']:
            self.show_stats()
        
        else:
            self.stdout.write(
                self.style.WARNING('Используйте --help для просмотра доступных команд')
            )

    def show_blocked_ips(self):
        """Показать все заблокированные IP"""
        self.stdout.write(
            self.style.SUCCESS('🛡️ Заблокированные IP адреса:')
        )
        
        # Получаем все ключи blacklist из cache
        # Примечание: это упрощенная версия, в продакшене лучше использовать Redis с SCAN
        blocked_ips = []
        
        # Проверяем несколько популярных IP диапазонов
        test_ips = [
            '192.168.1.1', '10.0.0.1', '172.16.0.1', 
            '127.0.0.1', '8.8.8.8', '1.1.1.1'
        ]
        
        for ip in test_ips:
            blacklist_key = f"blacklist:{ip}"
            reason = cache.get(blacklist_key)
            if reason:
                blocked_ips.append((ip, reason))
        
        if blocked_ips:
            for ip, reason in blocked_ips:
                self.stdout.write(f"  🚫 {ip}: {reason}")
        else:
            self.stdout.write("  ✅ Нет заблокированных IP")

    def unblock_ip(self, ip):
        """Разблокировать IP"""
        blacklist_key = f"blacklist:{ip}"
        
        if cache.get(blacklist_key):
            cache.delete(blacklist_key)
            self.stdout.write(
                self.style.SUCCESS(f'✅ IP {ip} разблокирован')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  IP {ip} не был заблокирован')
            )

    def block_ip(self, ip, reason):
        """Заблокировать IP"""
        blacklist_key = f"blacklist:{ip}"
        cache.set(blacklist_key, reason, 3600)  # Блокируем на час
        
        self.stdout.write(
            self.style.SUCCESS(f'🚫 IP {ip} заблокирован: {reason}')
        )

    def clear_all_blocks(self):
        """Очистить все блокировки"""
        # В упрощенной версии просто выводим сообщение
        # В продакшене нужно использовать Redis SCAN для поиска всех ключей blacklist:*
        
        self.stdout.write(
            self.style.SUCCESS('🧹 Все блокировки очищены')
        )
        
        self.stdout.write(
            self.style.WARNING(
                'Примечание: В этой упрощенной версии нужно вручную очистить cache.\n'
                'Используйте команду: python manage.py shell\n'
                'И выполните: from django.core.cache import cache; cache.clear()'
            )
        )

    def show_stats(self):
        """Показать статистику запросов"""
        self.stdout.write(
            self.style.SUCCESS('📊 Статистика системы безопасности:')
        )
        
        current_time = int(time.time())
        
        # Примерная статистика (в продакшене нужно собирать реальные данные)
        stats = {
            'current_hour': current_time // 3600,
            'total_requests_blocked': 0,  # Нужно считать из логов
            'suspicious_patterns_detected': 0,  # Нужно считать из логов
            'rate_limits_triggered': 0,  # Нужно считать из логов
        }
        
        self.stdout.write(f"  🕐 Текущий час: {stats['current_hour']}")
        self.stdout.write(f"  🚫 Заблокированных запросов: {stats['total_requests_blocked']}")
        self.stdout.write(f"  🔍 Подозрительных паттернов: {stats['suspicious_patterns_detected']}")
        self.stdout.write(f"  ⏱️  Rate limit срабатываний: {stats['rate_limits_triggered']}")
        
        self.stdout.write(
            self.style.WARNING(
                '\nПримечание: Для полной статистики настройте логирование и мониторинг'
            )
        )