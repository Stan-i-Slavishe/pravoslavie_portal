#!/usr/bin/env python
"""
Скрипт для исправления отображения изображений товаров в магазине
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
    
    print("🔄 Исправление изображений товаров в магазине...")
    
    # Получаем все товары типа 'book'
    book_products = Product.objects.filter(product_type='book')
    
    print(f"📚 Найдено товаров книг: {book_products.count()}")
    
    updated_count = 0
    error_count = 0
    
    for product in book_products:
        try:
            # Находим соответствующую книгу
            book = Book.objects.get(id=product.book_id)
            
            print(f"\n📖 Обрабатываем: {product.title}")
            print(f"   ID товара: {product.id}")
            print(f"   ID книги: {product.book_id}")
            print(f"   Обложка книги: {'✅ есть' if book.cover else '❌ нет'}")
            print(f"   Изображение товара: {'✅ есть' if product.image else '❌ нет'}")
            
            # Проверяем, есть ли обложка у книги
            if book.cover:
                # Если у товара нет изображения или оно отличается
                if not product.image:
                    product.image = book.cover
                    product.save()
                    print(f"   ✅ Обложка скопирована в товар")
                    updated_count += 1
                else:
                    print(f"   ℹ️ У товара уже есть изображение")
            else:
                print(f"   ⚠️ У книги нет обложки для копирования")
                    
        except Book.DoesNotExist:
            print(f"❌ Книга с ID {product.book_id} не найдена для товара: {product.title}")
            error_count += 1
        except Exception as e:
            print(f"❌ Ошибка при обработке товара {product.title}: {e}")
            error_count += 1
    
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"   ✅ Обновлено изображений: {updated_count}")
    print(f"   ❌ Ошибок: {error_count}")
    print(f"   📋 Всего товаров книг: {book_products.count()}")
    
    # Финальная статистика
    print(f"\n🖼️ ФИНАЛЬНАЯ СТАТИСТИКА:")
    with_images = book_products.exclude(image='').count()
    without_images = book_products.filter(image='').count()
    
    print(f"   ✅ Товаров с изображениями: {with_images}")
    print(f"   ❌ Товаров без изображений: {without_images}")
    
    if without_images > 0:
        print(f"\n📝 ТОВАРЫ БЕЗ ИЗОБРАЖЕНИЙ:")
        for product in book_products.filter(image=''):
            try:
                book = Book.objects.get(id=product.book_id)
                print(f"   📖 {product.title}")
                print(f"      Книга: {book.title}")
                print(f"      Обложка книги: {'есть' if book.cover else 'НЕТ'}")
            except Book.DoesNotExist:
                print(f"   📖 {product.title} (книга не найдена)")
    
    print(f"\n🎉 Исправление завершено!")
    
    # Дополнительная проверка
    print(f"\n🔍 ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА:")
    all_products = Product.objects.filter(is_active=True)
    for product in all_products[:5]:  # Проверим первые 5 товаров
        content_obj = product.content_object
        print(f"📦 {product.title}")
        print(f"   Тип: {product.product_type}")
        print(f"   Изображение товара: {'✅' if product.image else '❌'}")
        if content_obj:
            if hasattr(content_obj, 'cover'):
                print(f"   Обложка объекта: {'✅' if content_obj.cover else '❌'}")
            else:
                print(f"   Обложка объекта: ❓ (нет поля cover)")
        else:
            print(f"   Связанный объект: ❌ (не найден)")
    
except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()
