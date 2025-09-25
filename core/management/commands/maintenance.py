from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Управление режимом технического обслуживания'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['on', 'off', 'status'],
            help='Действие: включить (on), выключить (off), или проверить статус (status)'
        )
        
        parser.add_argument(
            '--message',
            type=str,
            help='Сообщение для отображения на странице обслуживания'
        )
        
        parser.add_argument(
            '--hours',
            type=int,
            default=2,
            help='Ориентировочное время обслуживания в часах (по умолчанию 2)'
        )
        
        parser.add_argument(
            '--allow-ip',
            type=str,
            action='append',
            help='IP-адреса, которым разрешен доступ во время обслуживания'
        )
    
    def handle(self, *args, **options):
        action = options['action']
        
        # Путь к файлу конфигурации режима обслуживания
        config_file = os.path.join(settings.BASE_DIR, 'maintenance_config.json')
        
        if action == 'on':
            # Включаем режим обслуживания
            config = {
                'enabled': True,
                'message': options.get('message') or 'Сайт находится на техническом обслуживании. Мы скоро вернёмся!',
                'start_time': datetime.now().isoformat(),
                'estimated_end_time': (datetime.now() + timedelta(hours=options['hours'])).isoformat(),
                'allowed_ips': options.get('allow_ip') or []
            }
            
            # Сохраняем конфигурацию
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Режим обслуживания ВКЛЮЧЕН\n'
                    f'   Сообщение: {config["message"]}\n'
                    f'   Ориентировочное время завершения: {config["estimated_end_time"]}\n'
                    f'   Разрешенные IP: {", ".join(config["allowed_ips"]) if config["allowed_ips"] else "только администраторы"}'
                )
            )
            
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Не забудьте перезапустить сервер для применения изменений:\n'
                    '   python manage.py runserver'
                )
            )
            
        elif action == 'off':
            # Выключаем режим обслуживания
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                config['enabled'] = False
                config['end_time'] = datetime.now().isoformat()
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                # Вычисляем продолжительность обслуживания
                if 'start_time' in config:
                    start = datetime.fromisoformat(config['start_time'])
                    end = datetime.now()
                    duration = end - start
                    duration_str = str(duration).split('.')[0]  # Убираем микросекунды
                else:
                    duration_str = "неизвестно"
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Режим обслуживания ВЫКЛЮЧЕН\n'
                        f'   Продолжительность обслуживания: {duration_str}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Режим обслуживания уже выключен')
                )
            
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Не забудьте перезапустить сервер для применения изменений:\n'
                    '   python manage.py runserver'
                )
            )
            
        elif action == 'status':
            # Проверяем статус режима обслуживания
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if config.get('enabled', False):
                    self.stdout.write(
                        self.style.WARNING(
                            f'🔧 Режим обслуживания: ВКЛЮЧЕН\n'
                            f'   Начало: {config.get("start_time", "неизвестно")}\n'
                            f'   Ориентировочное завершение: {config.get("estimated_end_time", "неизвестно")}\n'
                            f'   Сообщение: {config.get("message", "")}\n'
                            f'   Разрешенные IP: {", ".join(config.get("allowed_ips", [])) if config.get("allowed_ips") else "только администраторы"}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('✅ Режим обслуживания: ВЫКЛЮЧЕН')
                    )
                    if 'end_time' in config:
                        self.stdout.write(
                            f'   Последнее обслуживание завершено: {config["end_time"]}'
                        )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ Режим обслуживания: ВЫКЛЮЧЕН (конфигурация не найдена)')
                )
