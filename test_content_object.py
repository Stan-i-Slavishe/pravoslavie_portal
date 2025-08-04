#!/usr/bin/env python
"""
Альтернативное решение: обновляем шаблон для получения обложки через content_object
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
    
    print("🔍 ДИАГНОСТИКА СВЯЗЕЙ МЕЖДУ КНИГАМИ И ТОВАРАМИ")
    print("=" * 60)
    
    # Проверяем конкретную книгу "Книга весна"
    book_vesna = Book.objects.filter(title__icontains='весна').first()
    if book_vesna:
        print(f"\n📖 КНИГА: {book_vesna.title}")
        print(f"   ID: {book_vesna.id}")
        print(f"   Обложка: {book_vesna.cover}")
        print(f"   Путь обложки: {book_vesna.cover.url if book_vesna.cover else 'НЕТ'}")
        
        # Ищем товар
        product = Product.objects.filter(product_type='book', book_id=book_vesna.id).first()
        if product:
            print(f"\n🛍️ ТОВАР В МАГАЗИНЕ:")
            print(f"   ID: {product.id}")
            print(f"   Название: {product.title}")
            print(f"   Product.image: {product.image}")
            print(f"   Product.image.url: {product.image.url if product.image else 'НЕТ'}")
            
            # Проверяем content_object
            content_obj = product.content_object
            print(f"\n🔗 CONTENT_OBJECT:")
            print(f"   Content object: {content_obj}")
            if content_obj:
                print(f"   Content object type: {type(content_obj)}")
                print(f"   Content object cover: {content_obj.cover if hasattr(content_obj, 'cover') else 'НЕТ АТРИБУТА'}")
                if hasattr(content_obj, 'cover') and content_obj.cover:
                    print(f"   Content object cover URL: {content_obj.cover.url}")
            
        else:
            print(f"\n❌ Товар не найден! Создаем...")
            product = Product.objects.create(
                title=book_vesna.title,
                description=book_vesna.description,
                price=book_vesna.price,
                product_type='book',
                book_id=book_vesna.id,
                image=book_vesna.cover,  # Копируем обложку
                is_active=True,
                is_digital=True,
            )
            print(f"   ✅ Товар создан: {product.title}")
    
    else:
        print("❌ Книга 'весна' не найдена!")
        # Покажем первые несколько книг
        print(f"\n📚 ПЕРВЫЕ 5 КНИГ:")
        for book in Book.objects.all()[:5]:
            print(f"   📖 {book.title} - обложка: {'есть' if book.cover else 'НЕТ'}")
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"   Всего книг: {Book.objects.count()}")
    print(f"   Книг с обложками: {Book.objects.filter(cover__isnull=False).count()}")
    print(f"   Всего товаров-книг: {Product.objects.filter(product_type='book').count()}")
    print(f"   Товаров с изображениями: {Product.objects.filter(product_type='book', image__isnull=False).count()}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
