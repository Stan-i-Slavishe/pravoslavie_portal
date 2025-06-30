# analytics/management/commands/send_payment_launch.py

from django.core.management.base import BaseCommand
from analytics.email_services.notifications import send_payment_launch_notification

class Command(BaseCommand):
    help = 'Отправляет уведомление о запуске платежей всем подписчикам'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать количество подписчиков без отправки писем'
        )

    def handle(self, *args, **options):
        from analytics.models import EmailSubscription
        
        # Подсчитываем подписчиков
        subscribers_count = EmailSubscription.objects.filter(
            is_active=True,
            notify_payment_launch=True
        ).count()
        
        self.stdout.write(f'📊 Найдено подписчиков: {subscribers_count}')
        
        if options['dry_run']:
            self.stdout.write(
                self.style.SUCCESS(f'Сухой запуск: уведомления будут отправлены {subscribers_count} подписчикам')
            )
            return
        
        if subscribers_count == 0:
            self.stdout.write(self.style.WARNING('Нет подписчиков для уведомления'))
            return
        
        # Подтверждение
        confirm = input(f'Отправить уведомления {subscribers_count} подписчикам? (yes/no): ')
        
        if confirm.lower() != 'yes':
            self.stdout.write('Отправка отменена')
            return
        
        self.stdout.write('🚀 Отправка уведомлений о запуске платежей...')
        
        if send_payment_launch_notification():
            self.stdout.write(
                self.style.SUCCESS(f'✅ Уведомления успешно отправлены {subscribers_count} подписчикам!')
            )
        else:
            self.stdout.write(self.style.ERROR('❌ Ошибка отправки уведомлений'))
