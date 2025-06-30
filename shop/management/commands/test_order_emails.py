# shop/management/commands/test_order_emails.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Order, OrderItem, Product
from shop.utils import send_order_email
import uuid


class Command(BaseCommand):
    help = 'Тестирование email уведомлений для заказов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email для отправки тестовых писем (по умолчанию admin@example.com)',
            default='admin@example.com'
        )
        parser.add_argument(
            '--template',
            type=str,
            choices=['order_created', 'order_paid_download', 'order_status_changed', 'fairy_tale_ready'],
            help='Тип шаблона для тестирования',
        )

    def handle(self, *args, **options):
        email = options['email']
        template = options['template']
        
        # Создаем тестовый заказ
        test_order = self.create_test_order()
        
        if template:
            # Тестируем конкретный шаблон
            self.test_specific_template(test_order, template, email)
        else:
            # Тестируем все шаблоны
            self.test_all_templates(test_order, email)

    def create_test_order(self):
        """Создает тестовый заказ для демонстрации"""
        
        # Создаем тестового пользователя если его нет
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )
        
        # Создаем тестовый заказ
        order = Order(
            order_id=uuid.uuid4(),
            user=user,
            first_name='Анна',
            last_name='Петрова',
            email='test@example.com',
            phone='+7 (900) 123-45-67',
            total_amount=1500.00,
            status='pending'
        )
        
        return order

    def test_specific_template(self, order, template, email):
        """Тестирует конкретный шаблон"""
        self.stdout.write(f"Тестирование шаблона: {template}")
        
        context = {}
        if template == 'order_status_changed':
            context['old_status'] = 'pending'
            order.status = 'paid'
        elif template == 'fairy_tale_ready':
            # Создаем мок объект для элемента заказа
            class MockOrderItem:
                def __init__(self):
                    self.id = 1
                    self.product_title = "Персонализированная сказка 'Храбрый медвежонок'"
                    self.personalization_data = {
                        'child_name': 'Маша',
                        'child_age': '5 лет',
                        'main_problem': 'Боится темноты'
                    }
                    self.include_audio = True
                    self.include_illustrations = False
                    self.special_requests = 'Пожалуйста, добавьте кота в сказку'
                
                def get_personalization_summary(self):
                    return "Имя: Маша; Возраст: 5 лет; Проблема: Боится темноты"
            
            context['order_item'] = MockOrderItem()
        
        # Отправляем тестовое письмо
        success = send_order_email(
            order=order,
            template_type=template,
            recipient_email=email,
            context=context
        )
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Письмо "{template}" успешно отправлено на {email}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка отправки письма "{template}"')
            )

    def test_all_templates(self, order, email):
        """Тестирует все шаблоны по очереди"""
        templates = [
            'order_created',
            'order_status_changed', 
            'order_paid_download',
            'fairy_tale_ready'
        ]
        
        self.stdout.write("Тестирование всех email шаблонов...")
        
        for template in templates:
            self.test_specific_template(order, template, email)
            self.stdout.write("---")
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Тестирование завершено! Проверьте email: {email}")
        )
