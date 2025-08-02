#!/usr/bin/env python
"""
Скрипт для создания товаров для всех платных книг
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
    
    print("🔄 Создание товаров для всех платных книг...")
    
    # Получаем все платные книги
    paid_books = Book.objects.filter(price__gt=0)
    
    created_count = 0
    updated_count = 0
    
    for book in paid_books:
        # Проверяем, есть ли уже товар
        product, created = Product.objects.get_or_create(
            product_type='book',
            book_id=book.id,
            defaults={
                'title': book.title,
                'description': book.description,
                'price': book.price,
                'is_active': True,
                'is_digital': True,
                'image': book.cover_image if hasattr(book, 'cover_image') else None,
            }
        )
        
        if created:
            print(f"✅ Создан товар: {product.title} - {product.price}₽")
            created_count += 1
        else:
            # Обновляем существующий товар
            updated = False
            if product.title != book.title:
                product.title = book.title
                updated = True
            if product.description != book.description:
                product.description = book.description  
                updated = True
            if product.price != book.price:
                product.price = book.price
                updated = True
            if not product.is_active:
                product.is_active = True
                updated = True
                
            if updated:
                product.save()
                print(f"🔄 Обновлен товар: {product.title} - {product.price}₽")
                updated_count += 1
            else:
                print(f"✓ Товар актуален: {product.title} - {product.price}₽")
    
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"   Создано новых товаров: {created_count}")
    print(f"   Обновлено товаров: {updated_count}")
    print(f"   Всего товаров книг: {Product.objects.filter(product_type='book').count()}")
    
    # Проверяем магазин
    print(f"\n🛒 АКТИВНЫЕ ТОВАРЫ В МАГАЗИНЕ:")
    active_products = Product.objects.filter(is_active=True)
    
    for product in active_products:
        print(f"   📦 {product.title} ({product.get_product_type_display()}) - {product.price}₽")
    
    print(f"\n🎉 Готово! В магазине {active_products.count()} активных товаров")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
