#!/usr/bin/env python
"""
Исправление обложек в магазине
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
    
    print("🔄 Исправление обложек товаров в магазине...")
    
    # Получаем все товары типа 'book'
    book_products = Product.objects.filter(product_type='book')
    
    updated_count = 0
    created_count = 0
    error_count = 0
    
    for product in book_products:
        try:
            # Находим соответствующую книгу
            book = Book.objects.get(id=product.book_id)
            
            print(f"\n📖 Обрабатываем: {product.title}")
            print(f"   Book ID: {product.book_id}")
            print(f"   Book cover: {book.cover}")
            print(f"   Product image: {product.image}")
            
            # Синхронизируем обложку
            if book.cover and (not product.image or str(product.image) != str(book.cover)):
                product.image = book.cover
                product.save()
                print(f"   ✅ Обложка обновлена")
                updated_count += 1
            elif not book.cover and product.image:
                print(f"   ⚠️ У книги нет обложки, но у товара есть изображение")
            elif not book.cover and not product.image:
                print(f"   ⚠️ И у книги, и у товара нет изображения")
            else:
                print(f"   ✓ Обложка актуальна")
                    
        except Book.DoesNotExist:
            print(f"❌ Книга с ID {product.book_id} не найдена для товара: {product.title}")
            error_count += 1
        except Exception as e:
            print(f"❌ Ошибка при обработке товара {product.title}: {e}")
            error_count += 1
    
    # Создаем товары для книг, у которых их еще нет
    print(f"\n🔍 Проверяем книги без товаров...")
    books_without_products = []
    
    for book in Book.objects.filter(price__gt=0):
        if not Product.objects.filter(product_type='book', book_id=book.id).exists():
            books_without_products.append(book)
    
    print(f"   Найдено книг без товаров: {len(books_without_products)}")
    
    for book in books_without_products:
        try:
            product = Product.objects.create(
                title=book.title,
                description=book.description,
                price=book.price,
                product_type='book',
                book_id=book.id,
                image=book.cover,
                is_active=True,
                is_digital=True,
            )
            print(f"✅ Создан товар для книги: {book.title}")
            created_count += 1
        except Exception as e:
            print(f"❌ Ошибка создания товара для книги {book.title}: {e}")
            error_count += 1
    
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"   Обновлено обложек: {updated_count}")
    print(f"   Создано товаров: {created_count}")
    print(f"   Ошибок: {error_count}")
    print(f"   Всего товаров книг: {Product.objects.filter(product_type='book').count()}")
    
    # Финальная проверка
    print(f"\n🖼️ ФИНАЛЬНАЯ СТАТИСТИКА ОБЛОЖЕК:")
    with_covers = Product.objects.filter(product_type='book', image__isnull=False).count()
    without_covers = Product.objects.filter(product_type='book', image__isnull=True).count()
    
    print(f"   Товары с обложками: {with_covers}")
    print(f"   Товары без обложек: {without_covers}")
    
    if without_covers > 0:
        print(f"\n📝 ТОВАРЫ БЕЗ ОБЛОЖЕК:")
        for product in Product.objects.filter(product_type='book', image__isnull=True):
            try:
                book = Book.objects.get(id=product.book_id)
                print(f"   📖 {product.title} (у книги обложка: {'есть' if book.cover else 'НЕТ'})")
            except Book.DoesNotExist:
                print(f"   📖 {product.title} (книга не найдена)")
    
    print(f"\n🎉 Исправление завершено!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
