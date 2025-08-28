from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Удаляет бесплатные товары из магазина'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Полностью удалить бесплатные товары (по умолчанию только деактивирует)',
        )

    def handle(self, *args, **options):
        self.stdout.write("🧹 Начинаем очистку бесплатных товаров из магазина...")
        
        # Найдем все бесплатные товары
        free_products = Product.objects.filter(price=0)
        
        self.stdout.write(f"📊 Найдено бесплатных товаров: {free_products.count()}")
        
        if free_products.exists():
            for product in free_products:
                self.stdout.write(f"   - {product.title} (ID: {product.id}, цена: {product.price}₽)")
            
            if options['delete']:
                # Полностью удаляем
                deleted_count = free_products.delete()[0]
                self.stdout.write(
                    self.style.SUCCESS(f"🗑️ Удалено товаров: {deleted_count}")
                )
            else:
                # Только деактивируем
                updated_count = free_products.update(is_active=False)
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Деактивировано товаров: {updated_count}")
                )
        else:
            self.stdout.write(
                self.style.SUCCESS("✅ Бесплатных товаров не найдено")
            )
        
        # Покажем итоговую статистику
        self.stdout.write("\n📈 Итоговая статистика:")
        active_products = Product.objects.filter(is_active=True)
        paid_products = active_products.filter(price__gt=0)
        
        self.stdout.write(f"   Всего активных товаров: {active_products.count()}")
        self.stdout.write(f"   Платных товаров: {paid_products.count()}")
        self.stdout.write(f"   Бесплатных активных: {active_products.filter(price=0).count()}")
        
        if paid_products.exists():
            self.stdout.write("\n💰 Активные платные товары:")
            for product in paid_products:
                self.stdout.write(f"   - {product.title}: {product.price}₽")
        
        self.stdout.write(
            self.style.SUCCESS("\n🎉 Очистка завершена!")
        )
