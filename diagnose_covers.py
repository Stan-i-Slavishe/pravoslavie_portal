#!/usr/bin/env python
"""
Диагностика проблемы с обложками книг
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
    
    print("🔍 ДИАГНОСТИКА ОБЛОЖЕК КНИГ")
    print("=" * 50)
    
    # Проверяем книгу "Книга весна"
    book_vesna = Book.objects.filter(title__icontains='весна').first()
    if book_vesna:
        print(f"\n📖 КНИГА: {book_vesna.title}")
        print(f"   ID: {book_vesna.id}")
        print(f"   Обложка: {book_vesna.cover}")
        print(f"   Обложка существует: {'Да' if book_vesna.cover else 'Нет'}")
        if book_vesna.cover:
            print(f"   Путь к обложке: {book_vesna.cover.url if book_vesna.cover else 'Нет'}")
        
        # Проверяем товар в магазине
        product = Product.objects.filter(product_type='book', book_id=book_vesna.id).first()
        if product:
            print(f"\n🛍️ ТОВАР В МАГАЗИНЕ:")
            print(f"   Название: {product.title}")
            print(f"   ID: {product.id}")
            print(f"   Изображение: {product.image}")
            print(f"   Изображение существует: {'Да' if product.image else 'Нет'}")
            if product.image:
                print(f"   Путь к изображению: {product.image.url}")
        else:
            print(f"\n❌ Товар для этой книги в магазине не найден!")
    else:
        print("❌ Книга 'весна' не найдена!")
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    total_books = Book.objects.count()
    books_with_covers = Book.objects.filter(cover__isnull=False).count()
    print(f"   Всего книг: {total_books}")
    print(f"   Книг с обложками: {books_with_covers}")
    
    total_products = Product.objects.filter(product_type='book').count()
    products_with_images = Product.objects.filter(product_type='book', image__isnull=False).count()
    print(f"   Всего товаров-книг: {total_products}")
    print(f"   Товаров с изображениями: {products_with_images}")
    
    print(f"\n📋 ВСЕ КНИГИ С ОБЛОЖКАМИ:")
    for book in Book.objects.filter(cover__isnull=False)[:5]:
        print(f"   📖 {book.title} - {book.cover}")
    
    print(f"\n🛒 ВСЕ ТОВАРЫ-КНИГИ:")
    for product in Product.objects.filter(product_type='book')[:5]:
        print(f"   🛍️ {product.title} - изображение: {product.image or 'НЕТ'}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
