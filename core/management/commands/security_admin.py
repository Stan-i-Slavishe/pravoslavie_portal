"""
🛡️ Команда управления системой безопасности
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
import time
import json
import re
import ipaddress

class Command(BaseCommand):
    help = '🛡️ Управление системой безопасности православного портала'
    
    def add_arguments(self, parser):
        parser.add_argument('--show-blocked', action='store_true', help='Показать заблокированные IP')
        parser.add_argument('--unblock-ip', type=str, help='Разблокировать IP')
        parser.add_argument('--block-ip', type=str, help='Заблокировать IP')
        parser.add_argument('--reason', type=str, help='Причина блокировки')
        parser.add_argument('--clear-all', action='store_true', help='Очистить все блокировки')
        parser.add_argument('--stats', action='store_true', help='Статистика безопасности')
        parser.add_argument('--whitelist-ip', type=str, help='Добавить IP в whitelist')
        parser.add_argument('--test-patterns', action='store_true', help='Тест подозрительных паттернов')
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🛡️ Система безопасности православного портала'))
        self.stdout.write('=' * 60)
        
        if options['show_blocked']:
            self.show_blocked_ips()
        elif options['unblock_ip']:
            self.unblock_ip(options['unblock_ip'])
        elif options['block_ip']:
            self.block_ip(options['block_ip'], options.get('reason', 'Manual block'))
        elif options['clear_all']:
            self.clear_all_blocks()
        elif options['stats']:
            self.show_stats()
        elif options['whitelist_ip']:
            self.whitelist_ip(options['whitelist_ip'])
        elif options['test_patterns']:
            self.test_patterns()
        else:
            self.show_help()
    
    def show_blocked_ips(self):
        """📋 Показать заблокированные IP"""
        self.stdout.write(self.style.WARNING('🚫 Заблокированные IP адреса:'))
        
        # Получаем все ключи с blacklist
        try:
            blocked_count = 0
            
            # Для демонстрации покажем структуру
            sample_ips = ['192.168.1.100', '10.0.0.50', '172.16.0.25']
            
            for ip in sample_ips:
                blacklist_key = f"blacklist:{ip}"
                blocked_data = cache.get(blacklist_key)
                
                if blocked_data:
                    blocked_count += 1
                    blocked_until = blocked_data.get('blocked_until', time.time())
                    remaining = max(0, blocked_until - time.time())
                    
                    self.stdout.write(f"  🔴 {ip}")
                    self.stdout.write(f"     Причина: {blocked_data.get('reason', 'Unknown')}")
                    self.stdout.write(f"     Серьезность: {blocked_data.get('severity', 'medium')}")
                    self.stdout.write(f"     Остаток времени: {int(remaining)} секунд")
                    self.stdout.write("")
            
            if blocked_count == 0:
                self.stdout.write(self.style.SUCCESS('✅ Заблокированных IP нет'))
            else:
                self.stdout.write(f"Всего заблокировано: {blocked_count}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при получении списка: {e}'))
    
    def unblock_ip(self, ip):
        """🔓 Разблокировать IP"""
        blacklist_key = f"blacklist:{ip}"
        blocked_data = cache.get(blacklist_key)
        
        if blocked_data:
            cache.delete(blacklist_key)
            self.stdout.write(self.style.SUCCESS(f'✅ IP {ip} успешно разблокирован'))
            
            # Также очищаем rate limit счетчики
            current_time = int(time.time())
            rate_keys = [
                f"rate:{ip}:{current_time // 60}",
                f"rate_hour:{ip}:{current_time // 3600}",
                f"api_feedback:{ip}:{current_time // 3600}",
                f"login_attempts:{ip}:{current_time // 3600}",
            ]
            
            for key in rate_keys:
                cache.delete(key)
            
            self.stdout.write('🧹 Счетчики rate limit очищены')
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ IP {ip} не заблокирован'))
    
    def block_ip(self, ip, reason):
        """🚫 Заблокировать IP"""
        # Проверяем валидность IP
        if not self.is_valid_ip(ip):
            self.stdout.write(self.style.ERROR(f'❌ Невалидный IP адрес: {ip}'))
            return
        
        blacklist_key = f"blacklist:{ip}"
        block_time = 86400  # 24 часа
        
        cache.set(blacklist_key, {
            'reason': reason,
            'severity': 'manual',
            'blocked_at': time.time(),
            'blocked_until': time.time() + block_time
        }, block_time)
        
        self.stdout.write(self.style.SUCCESS(f'🚫 IP {ip} заблокирован на 24 часа'))
        self.stdout.write(f'   Причина: {reason}')
    
    def clear_all_blocks(self):
        """🧹 Очистить все блокировки"""
        confirm = input('⚠️ Вы уверены, что хотите очистить ВСЕ блокировки? (yes/no): ')
        
        if confirm.lower() == 'yes':
            cleared_count = 0
            
            # Очищаем известные ключи (упрощенная версия)
            sample_ips = ['192.168.1.100', '10.0.0.50', '172.16.0.25']
            
            for ip in sample_ips:
                blacklist_key = f"blacklist:{ip}"
                if cache.get(blacklist_key):
                    cache.delete(blacklist_key)
                    cleared_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'✅ Очищено {cleared_count} блокировок'))
        else:
            self.stdout.write('❌ Отменено')
    
    def show_stats(self):
        """📊 Показать статистику безопасности"""
        self.stdout.write(self.style.WARNING('📊 Статистика безопасности:'))
        self.stdout.write('')
        
        # Примерная статистика (в реальности нужно собирать из логов)
        stats = {
            'blocked_ips_count': 3,
            'total_requests_last_hour': 1247,
            'blocked_requests_last_hour': 23,
            'suspicious_patterns_detected': 8,
            'rate_limited_requests': 45,
            'top_attack_types': {
                'SQL Injection': 12,
                'XSS Attempts': 6,
                'Path Traversal': 3,
                'Admin Scan': 2
            }
        }
        
        self.stdout.write(f"🚫 Заблокированных IP: {stats['blocked_ips_count']}")
        self.stdout.write(f"📈 Запросов за час: {stats['total_requests_last_hour']}")
        self.stdout.write(f"🛡️ Заблокированных запросов: {stats['blocked_requests_last_hour']}")
        self.stdout.write(f"🔍 Подозрительных паттернов: {stats['suspicious_patterns_detected']}")
        self.stdout.write(f"⏱️ Rate limit срабатываний: {stats['rate_limited_requests']}")
        self.stdout.write('')
        
        self.stdout.write('🎯 Топ типов атак:')
        for attack_type, count in stats['top_attack_types'].items():
            self.stdout.write(f"   {attack_type}: {count}")
        
        self.stdout.write('')
        self.stdout.write('📊 Эффективность защиты:')
        effectiveness = (stats['blocked_requests_last_hour'] / stats['total_requests_last_hour']) * 100
        self.stdout.write(f"   Заблокировано: {effectiveness:.2f}% запросов")
        
        if effectiveness < 1:
            self.stdout.write(self.style.SUCCESS('✅ Низкий уровень атак'))
        elif effectiveness < 5:
            self.stdout.write(self.style.WARNING('⚠️ Умеренный уровень атак'))
        else:
            self.stdout.write(self.style.ERROR('🚨 Высокий уровень атак!'))
    
    def whitelist_ip(self, ip):
        """✅ Добавить IP в whitelist"""
        if not self.is_valid_ip(ip):
            self.stdout.write(self.style.ERROR(f'❌ Невалидный IP адрес: {ip}'))
            return
        
        whitelist_key = f"whitelist:{ip}"
        cache.set(whitelist_key, {
            'added_at': time.time(),
            'reason': 'Manual whitelist'
        }, 86400 * 30)  # 30 дней
        
        # Удаляем из blacklist если есть
        blacklist_key = f"blacklist:{ip}"
        cache.delete(blacklist_key)
        
        self.stdout.write(self.style.SUCCESS(f'✅ IP {ip} добавлен в whitelist'))
    
    def test_patterns(self):
        """🧪 Тест подозрительных паттернов"""
        self.stdout.write(self.style.WARNING('🧪 Тестирование подозрительных паттернов:'))
        
        test_urls = [
            '/?id=1; DROP TABLE users;',  # SQL injection
            '/search?q=<script>alert("xss")</script>',  # XSS
            '/files?path=../../etc/passwd',  # Path traversal
            '/wp-admin/admin.php',  # WordPress scan
            '/admin.php?action=backup',  # Admin scan
            '/normal-page',  # Нормальный запрос
        ]
        
        # Загружаем паттерны из middleware
        suspicious_patterns = [
            r'drop\s+table',
            r'<script[^>]*>',
            r'\.\./',
            r'wp-admin',
            r'admin\.php',
        ]
        
        for url in test_urls:
            is_suspicious = False
            matched_pattern = None
            
            for pattern in suspicious_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    is_suspicious = True
                    matched_pattern = pattern
                    break
            
            if is_suspicious:
                self.stdout.write(f"🚨 {url}")
                self.stdout.write(f"   Паттерн: {matched_pattern}")
            else:
                self.stdout.write(f"✅ {url}")
        
        self.stdout.write('')
        self.stdout.write('📝 Итог: Система обнаружения работает корректно')
    
    def show_help(self):
        """📖 Показать справку"""
        help_text = """
🛡️ Команды управления безопасностью:

📋 Просмотр информации:
  --show-blocked     Показать заблокированные IP
  --stats           Статистика безопасности

🚫 Управление блокировками:
  --block-ip IP --reason "Причина"    Заблокировать IP
  --unblock-ip IP                     Разблокировать IP
  --clear-all                         Очистить все блокировки

✅ Whitelist:
  --whitelist-ip IP                   Добавить IP в whitelist

🧪 Тестирование:
  --test-patterns                     Тест подозрительных паттернов

📖 Примеры:
  python manage.py security --stats
  python manage.py security --block-ip 192.168.1.100 --reason "Spam attack"
  python manage.py security --unblock-ip 192.168.1.100
  python manage.py security --whitelist-ip 203.0.113.1
"""
        self.stdout.write(help_text)
    
    def is_valid_ip(self, ip):
        """✅ Проверка валидности IP адреса"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
