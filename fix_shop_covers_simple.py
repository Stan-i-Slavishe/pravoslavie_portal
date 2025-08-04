#!/usr/bin/env python
"""
Простое исправление обложек товаров в магазине
Запускать через: python manage.py shell < fix_shop_covers_simple.py
"""

from books.models import Book
from shop.models import Product

print("🔄 Исправление обложек товаров в магазине...")

# Получаем все товары типа 'book'
book_products = Product.objects.filter(product_type='book')
updated_count = 0

for product in book_products:
    try:
        # Находим соответствующую книгу
        book = Book.objects.get(id=product.book_id)
        
        # Синхронизируем обложку, если она есть у книги, но нет у товара
        if book.cover and not product.image:
            product.image = book.cover
            product.save()
            print(f"✅ Обновлена обложка для: {product.title}")
            updated_count += 1
            
    except Book.DoesNotExist:
        print(f"❌ Книга не найдена для товара: {product.title}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

print(f"\n📊 Обновлено обложек: {updated_count}")

# Проверяем результат
with_covers = Product.objects.filter(product_type='book', image__isnull=False).count()
without_covers = Product.objects.filter(product_type='book', image__isnull=True).count()

print(f"Товары с обложками: {with_covers}")
print(f"Товары без обложек: {without_covers}")

print("🎉 Готово!")
