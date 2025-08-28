# shop/management/commands/sync_products.py

from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import Book
from shop.models import Product

class Command(BaseCommand):
    help = 'Синхронизирует все платные товары с магазином'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать изменения без применения',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 РЕЖИМ ПРЕДВАРИТЕЛЬНОГО ПРОСМОТРА (без изменений)')
            )
        
        self.stdout.write("🏪 Синхронизация платных товаров с магазином...")
        
        created_count = 0
        updated_count = 0
        
        with transaction.atomic():
            # Синхронизация книг
            paid_books = Book.objects.filter(price__gt=0)
            self.stdout.write(f"📚 Найдено платных книг: {paid_books.count()}")
            
            for book in paid_books:
                if dry_run:
                    existing = Product.objects.filter(
                        product_type='book',
                        book_id=book.id
                    ).exists()
                    
                    if not existing:
                        self.stdout.write(f"  ➕ Будет создана: {book.title} - {book.price}₽")
                        created_count += 1
                    else:
                        self.stdout.write(f"  ✓ Существует: {book.title}")
                else:
                    product, created = Product.objects.get_or_create(
                        product_type='book',
                        book_id=book.id,
                        defaults={
                            'title': book.title,
                            'description': book.description or f"Духовная книга '{book.title}'",
                            'price': book.price,
                            'is_active': True,
                            'is_digital': True,
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✅ Создана: {product.title} - {product.price}₽")
                        )
                        created_count += 1
                    else:
                        # Обновляем существующий товар
                        updated = False
                        if product.title != book.title:
                            product.title = book.title
                            updated = True
                        if product.price != book.price:
                            product.price = book.price
                            updated = True
                        if not product.is_active:
                            product.is_active = True
                            updated = True
                            
                        if updated:
                            product.save()
                            self.stdout.write(f"  🔄 Обновлена: {product.title}")
                            updated_count += 1
                        else:
                            self.stdout.write(f"  ✓ Актуальна: {product.title}")
            
            if dry_run:
                # Откатываем транзакцию в режиме предварительного просмотра
                transaction.set_rollback(True)
        
        # Показываем статистику
        total_products = Product.objects.filter(is_active=True).count()
        
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.WARNING("📋 ПРЕДВАРИТЕЛЬНЫЙ РЕЗУЛЬТАТ:"))
            self.stdout.write(f"  Будет создано: {created_count}")
            self.stdout.write(f"  Будет обновлено: {updated_count}")
        else:
            self.stdout.write(self.style.SUCCESS("🎉 СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА:"))
            self.stdout.write(f"  ✅ Создано: {created_count}")
            self.stdout.write(f"  🔄 Обновлено: {updated_count}")
            self.stdout.write(f"  🛒 Всего товаров в магазине: {total_products}")
            
        self.stdout.write("="*50)
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING("Для применения изменений запустите без --dry-run")
            )
