# shop/signals.py - Автоматическая синхронизация товаров

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from books.models import Book
from .models import Product

@receiver(post_save, sender=Book)
def sync_book_with_shop(sender, instance, created, **kwargs):
    """Автоматически создает/обновляет товар при сохранении книги"""
    if instance.price > 0:  # Только для платных книг
        product, product_created = Product.objects.get_or_create(
            product_type='book',
            book_id=instance.id,
            defaults={
                'title': instance.title,
                'description': instance.description or f"Духовная книга '{instance.title}' - погрузитесь в мир веры и мудрости.",
                'price': instance.price,
                'is_active': True,
                'is_digital': True,
                'image': getattr(instance, 'cover_image', None),
            }
        )
        
        if not product_created:
            # Обновляем существующий товар
            product.title = instance.title
            product.description = instance.description or f"Духовная книга '{instance.title}'"
            product.price = instance.price
            product.is_active = True
            product.save()
            
        print(f"📚 Синхронизирована книга с магазином: {instance.title}")
    else:
        # Если книга стала бесплатной, деактивируем товар
        Product.objects.filter(
            product_type='book',
            book_id=instance.id
        ).update(is_active=False)
        print(f"📚 Книга '{instance.title}' деактивирована в магазине (стала бесплатной)")

@receiver(post_delete, sender=Book)
def remove_book_from_shop(sender, instance, **kwargs):
    """Удаляет товар при удалении книги"""
    deleted_count = Product.objects.filter(
        product_type='book',
        book_id=instance.id
    ).delete()[0]
    
    if deleted_count > 0:
        print(f"Товар для книги '{instance.title}' удален из магазина")

# В будущем можно добавить сигналы для других типов товаров,
# когда соответствующие модели будут созданы
print("Сигналы синхронизации товаров подключены (только для книг)")
