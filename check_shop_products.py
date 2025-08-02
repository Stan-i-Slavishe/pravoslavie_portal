#!/usr/bin/env python
"""
Скрипт для проверки и синхронизации товаров с книгами
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
    print("✅ Django настроен успешно")
    
    from books.models import Book
    from shop.models import Product
    
    print("\n📚 ПРОВЕРКА КНИГ И ТОВАРОВ:")
    print("=" * 50)
    
    # Получаем все платные книги
    paid_books = Book.objects.filter(price__gt=0)
    print(f"Платных книг в системе: {paid_books.count()}")
    
    for book in paid_books:
        print(f"\n📖 Книга: {book.title}")
        print(f"   Цена: {book.price}₽")
        print(f"   Слаг: {book.slug}")
        
        # Проверяем, есть ли товар для этой книги
        product = Product.objects.filter(
            product_type='book',
            book_id=book.id
        ).first()
        
        if product:
            print(f"   ✅ Товар в магазине: {product.title} (ID: {product.id})")
            print(f"   📦 Активен: {product.is_active}")
        else:
            print(f"   ❌ Товара в магазине НЕТ")
            
            # Создаем товар для книги
            product = Product.objects.create(
                title=book.title,
                description=book.description,
                price=book.price,
                product_type='book',
                book_id=book.id,
                is_active=True,
                is_digital=True,
                image=book.cover_image
            )
            print(f"   ✅ СОЗДАН товар: {product.title} (ID: {product.id})")
    
    # Проверяем все товары в магазине
    print(f"\n🛒 ВСЕ ТОВАРЫ В МАГАЗИНЕ:")
    print("=" * 50)
    
    all_products = Product.objects.filter(is_active=True)
    print(f"Активных товаров: {all_products.count()}")
    
    for product in all_products:
        print(f"\n🛍️ {product.title}")
        print(f"   Тип: {product.get_product_type_display()}")
        print(f"   Цена: {product.price}₽")
        print(f"   Активен: {product.is_active}")
        
        if product.product_type == 'book' and product.book_id:
            try:
                book = Book.objects.get(id=product.book_id)
                print(f"   📚 Связанная книга: {book.title}")
            except Book.DoesNotExist:
                print(f"   ⚠️ Книга с ID {product.book_id} не найдена!")
    
    print(f"\n🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
