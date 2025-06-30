from django.core.management.base import BaseCommand
from django.utils import timezone
from fairy_tales.models import FairyTaleTemplate, PersonalizationOrder
from shop.models import Product, Order, OrderItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Интегрировать терапевтические сказки в магазин'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-products',
            action='store_true',
            help='Создать продукты для всех шаблонов сказок',
        )
        parser.add_argument(
            '--migrate-orders',
            action='store_true',
            help='Мигрировать существующие заказы сказок',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет сделано без изменений',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧚 Интеграция терапевтических сказок в магазин')
        )
        
        if options['create_products']:
            self.create_products(dry_run=options['dry_run'])
        
        if options['migrate_orders']:
            self.migrate_orders(dry_run=options['dry_run'])
        
        if not options['create_products'] and not options['migrate_orders']:
            self.stdout.write(
                self.style.WARNING('Укажите --create-products или --migrate-orders')
            )

    def create_products(self, dry_run=False):
        """Создать продукты для всех шаблонов сказок"""
        self.stdout.write('\n📦 Создание продуктов для шаблонов сказок...')
        
        templates = FairyTaleTemplate.objects.filter(is_published=True)
        created_count = 0
        
        for template in templates:
            # Проверить, существует ли уже продукт
            existing_product = Product.objects.filter(
                product_type='fairy_tale',
                fairy_tale_template_id=template.id
            ).first()
            
            if existing_product:
                self.stdout.write(f'  ⏭️  Продукт уже существует: {template.title}')
                continue
            
            product_data = {
                'title': f'Персонализированная сказка: {template.title}',
                'description': template.short_description,
                'price': template.base_price,
                'product_type': 'fairy_tale',
                'fairy_tale_template_id': template.id,
                'requires_personalization': True,
                'is_digital': True,
                'has_audio_option': template.has_audio_option,
                'audio_option_price': template.audio_price,
                'has_illustration_option': template.has_illustration_option,
                'illustration_option_price': template.illustration_price,
                'personalization_form_config': template.personalization_fields,
                'image': template.cover_image,
            }
            
            if dry_run:
                self.stdout.write(f'  🔍 [DRY RUN] Создал бы продукт: {product_data["title"]}')
            else:
                product = Product.objects.create(**product_data)
                self.stdout.write(f'  ✅ Создан продукт: {product.title}')
                created_count += 1
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'✨ Создано {created_count} новых продуктов')
            )

    def migrate_orders(self, dry_run=False):
        """Мигрировать существующие заказы персонализации"""
        self.stdout.write('\n📋 Миграция заказов персонализации...')
        
        old_orders = PersonalizationOrder.objects.all()
        migrated_count = 0
        
        for old_order in old_orders:
            # Проверить, не мигрирован ли уже этот заказ
            existing_order = Order.objects.filter(
                user=old_order.user,
                notes__contains=f'Migrated from PersonalizationOrder {old_order.order_id}'
            ).first()
            
            if existing_order:
                self.stdout.write(f'  ⏭️  Заказ уже мигрирован: {old_order.order_id}')
                continue
            
            # Найти или создать продукт для этого шаблона
            product = Product.objects.filter(
                product_type='fairy_tale',
                fairy_tale_template_id=old_order.template.id
            ).first()
            
            if not product:
                if dry_run:
                    self.stdout.write(f'  🔍 [DRY RUN] Создал бы продукт для: {old_order.template.title}')
                    continue
                else:
                    # Создать продукт
                    product = Product.objects.create(
                        title=f'Персонализированная сказка: {old_order.template.title}',
                        description=old_order.template.short_description,
                        price=old_order.base_price,
                        product_type='fairy_tale',
                        fairy_tale_template_id=old_order.template.id,
                        requires_personalization=True,
                        is_digital=True,
                        has_audio_option=old_order.template.has_audio_option,
                        audio_option_price=old_order.template.audio_price,
                        has_illustration_option=old_order.template.has_illustration_option,
                        illustration_option_price=old_order.template.illustration_price,
                        image=old_order.template.cover_image,
                    )
            
            # Подготовить данные заказа
            order_data = {
                'user': old_order.user,
                'status': self.map_old_status_to_new(old_order.status),
                'total_amount': old_order.total_price,
                'email': old_order.customer_email,
                'first_name': old_order.customer_name.split()[0] if old_order.customer_name else '',
                'last_name': ' '.join(old_order.customer_name.split()[1:]) if old_order.customer_name and len(old_order.customer_name.split()) > 1 else '',
                'phone': old_order.customer_phone or '',
                'notes': f'Migrated from PersonalizationOrder {old_order.order_id}',
                'created_at': old_order.created_at,
                'paid_at': old_order.completed_at if old_order.status in ['paid', 'ready', 'delivered'] else None,
            }
            
            if dry_run:
                self.stdout.write(f'  🔍 [DRY RUN] Мигрировал бы заказ: {old_order.order_id}')
                continue
            
            # Создать новый заказ
            new_order = Order.objects.create(**order_data)
            
            # Создать элемент заказа с данными персонализации
            order_item_data = {
                'order': new_order,
                'product': product,
                'product_title': product.title,
                'product_price': old_order.base_price,
                'quantity': 1,
                'personalization_data': old_order.personalization_data,
                'include_audio': old_order.include_audio,
                'include_illustrations': old_order.include_illustrations,
                'special_requests': old_order.special_requests,
                'fairy_tale_status': self.map_old_status_to_fairy_tale_status(old_order.status),
                'generated_content': old_order.generated_content,
                'audio_file': old_order.audio_file,
                'illustration_file': old_order.illustration_file,
                'estimated_completion': old_order.estimated_completion,
                'admin_notes': old_order.admin_notes,
            }
            
            OrderItem.objects.create(**order_item_data)
            
            self.stdout.write(f'  ✅ Мигрирован заказ: {old_order.order_id} -> {new_order.short_id}')
            migrated_count += 1
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'✨ Мигрировано {migrated_count} заказов')
            )
    
    def map_old_status_to_new(self, old_status):
        """Сопоставить старый статус с новым"""
        status_mapping = {
            'pending': 'pending',
            'paid': 'paid',
            'in_progress': 'paid',
            'ready': 'completed',
            'delivered': 'completed',
            'cancelled': 'cancelled',
        }
        return status_mapping.get(old_status, 'pending')
    
    def map_old_status_to_fairy_tale_status(self, old_status):
        """Сопоставить старый статус со статусом сказки"""
        status_mapping = {
            'pending': 'pending',
            'paid': 'pending',
            'in_progress': 'in_progress',
            'ready': 'ready',
            'delivered': 'delivered',
            'cancelled': '',
        }
        return status_mapping.get(old_status, 'pending')
