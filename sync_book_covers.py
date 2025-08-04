#!/usr/bin/env python
"""
Скрипт для синхронизации обложек книг с товарами в магазине
"""

import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    
    from books.models import Book
    from shop.models import Product
    
    print("🔄 Синхронизация обложек книг с товарами в магазине...")
    
    # Получаем все товары типа 'book'
    book_products = Product.objects.filter(product_type='book')
    
    updated_count = 0
    error_count = 0
    
    for product in book_products:
        try:
            # Находим соответствующую книгу
            book = Book.objects.get(id=product.book_id)
            
            # Проверяем, есть ли обложка у книги
            if book.cover:
                # Если у товара нет изображения или оно отличается
                if not product.image or product.image != book.cover:
                    product.image = book.cover
                    product.save()
                    print(f"✅ Обновлена обложка для: {product.title}")
                    updated_count += 1
                else:
                    print(f"✓ Обложка актуальна: {product.title}")
            else:
                if product.image:
                    print(f"⚠️ У книги нет обложки, но у товара есть изображение: {product.title}")
                else:
                    print(f"⚠️ У книги и товара нет изображения: {product.title}")
                    
        except Book.DoesNotExist:
            print(f"❌ Книга с ID {product.book_id} не найдена для товара: {product.title}")
            error_count += 1
        except Exception as e:
            print(f"❌ Ошибка при обработке товара {product.title}: {e}")
            error_count += 1
    
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"   Обновлено обложек: {updated_count}")
    print(f"   Ошибок: {error_count}")
    print(f"   Всего товаров книг: {book_products.count()}")
    
    # Проверяем состояние обложек
    print(f"\n🖼️ СТАТИСТИКА ОБЛОЖЕК:")
    with_covers = book_products.filter(image__isnull=False).count()
    without_covers = book_products.filter(image__isnull=True).count()
    
    print(f"   С обложками: {with_covers}")
    print(f"   Без обложек: {without_covers}")
    
    if without_covers > 0:
        print(f"\n📝 ТОВАРЫ БЕЗ ОБЛОЖЕК:")
        for product in book_products.filter(image__isnull=True):
            try:
                book = Book.objects.get(id=product.book_id)
                print(f"   📖 {product.title} (книга обложка: {'есть' if book.cover else 'нет'})")
            except Book.DoesNotExist:
                print(f"   📖 {product.title} (книга не найдена)")
    
    print(f"\n🎉 Синхронизация завершена!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
