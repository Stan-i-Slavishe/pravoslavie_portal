# analytics/management/commands/send_weekly_report.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from analytics.email_services.notifications import generate_weekly_report, send_weekly_report

class Command(BaseCommand):
    help = 'Генерирует и отправляет еженедельный отчет по аналитике'

    def add_arguments(self, parser):
        parser.add_argument(
            '--week-start',
            type=str,
            help='Дата начала недели в формате YYYY-MM-DD (по умолчанию - прошлая неделя)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно отправить отчет, даже если он уже был отправлен'
        )

    def handle(self, *args, **options):
        self.stdout.write('📊 Генерация еженедельного отчета...')
        
        # Определяем период
        if options['week_start']:
            try:
                week_start = datetime.strptime(options['week_start'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Неверный формат даты. Используйте YYYY-MM-DD')
                )
                return
        else:
            # По умолчанию - прошлая неделя (понедельник - воскресенье)
            today = timezone.now().date()
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday + 7)
            week_start = last_monday

        week_end = week_start + timedelta(days=6)
        
        self.stdout.write(f'Период отчета: {week_start.strftime(\"%d.%m.%Y\")} - {week_end.strftime(\"%d.%m.%Y\")}')
        
        # Генерируем отчет
        report = generate_weekly_report(week_start, week_end)
        
        if not report:
            self.stdout.write(self.style.ERROR('Ошибка генерации отчета'))
            return
        
        self.stdout.write(f'✅ Отчет сгенерирован:')
        self.stdout.write(f'   - Кликов на покупку: {report.total_purchase_intents}')
        self.stdout.write(f'   - Уникальных пользователей: {report.unique_users}')
        self.stdout.write(f'   - Новых подписок: {report.new_subscriptions}')
        
        # Проверяем, нужно ли отправлять
        if not options['force'] and report.sent_to_admins and report.sent_to_subscribers:
            self.stdout.write(
                self.style.WARNING('Отчет уже был отправлен. Используйте --force для повторной отправки')
            )
            return
        
        # Отправляем отчет
        self.stdout.write('📧 Отправка отчета...')
        
        if send_weekly_report(report):
            self.stdout.write(self.style.SUCCESS('✅ Отчет успешно отправлен!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Ошибка отправки отчета'))
