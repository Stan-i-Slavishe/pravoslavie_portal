#!/usr/bin/env python
"""
Диагностика файлов книг для скачивания
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
    from shop.models import Product, Purchase
    from django.contrib.auth.models import User
    
    print("🔍 ДИАГНОСТИКА ФАЙЛОВ КНИГ ДЛЯ СКАЧИВАНИЯ")
    print("=" * 60)
    
    # Ищем книгу "Книга весна"
    book_vesna = Book.objects.filter(title__icontains='весна').first()
    if book_vesna:
        print(f"\n📖 КНИГА: {book_vesna.title}")
        print(f"   ID: {book_vesna.id}")
        print(f"   Файл: {book_vesna.file}")
        print(f"   Файл существует: {'Да' if book_vesna.file else 'Нет'}")
        if book_vesna.file:
            print(f"   Путь к файлу: {book_vesna.file.url}")
            print(f"   Физический файл: {book_vesna.file.path}")
            
            # Проверяем физическое существование файла
            try:
                file_exists = os.path.exists(book_vesna.file.path)
                print(f"   Физический файл существует: {'Да' if file_exists else 'Нет'}")
                if file_exists:
                    file_size = os.path.getsize(book_vesna.file.path)
                    print(f"   Размер файла: {file_size} байт")
            except Exception as e:
                print(f"   Ошибка проверки файла: {e}")
        
        # Проверяем товар в магазине
        product = Product.objects.filter(product_type='book', book_id=book_vesna.id).first()
        if product:
            print(f"\n🛍️ ТОВАР В МАГАЗИНЕ:")
            print(f"   ID: {product.id}")
            print(f"   Название: {product.title}")
            print(f"   content_object: {product.content_object}")
            
            content_obj = product.content_object
            if content_obj:
                print(f"   content_object.file: {content_obj.file if hasattr(content_obj, 'file') else 'НЕТ АТРИБУТА'}")
                if hasattr(content_obj, 'file') and content_obj.file:
                    print(f"   content_object.file.url: {content_obj.file.url}")
        
        # Проверяем покупки этой книги
        purchases = Purchase.objects.filter(product__book_id=book_vesna.id)
        print(f"\n💰 ПОКУПКИ ЭТОЙ КНИГИ:")
        print(f"   Количество покупок: {purchases.count()}")
        
        for purchase in purchases:
            print(f"\n   📦 Покупка #{purchase.id}:")
            print(f"      Пользователь: {purchase.user.username}")
            print(f"      Дата: {purchase.purchased_at}")
            print(f"      Заказ статус: {purchase.order.status}")
            print(f"      Товар: {purchase.product.title}")
            
            # Проверяем доступность для скачивания
            content_obj = purchase.product.content_object
            if content_obj and hasattr(content_obj, 'file') and content_obj.file:
                print(f"      ✅ Файл доступен для скачивания: {content_obj.file.url}")
            else:
                print(f"      ❌ Файл НЕ доступен для скачивания")
                print(f"         content_obj: {content_obj}")
                if content_obj:
                    print(f"         hasattr file: {hasattr(content_obj, 'file')}")
                    if hasattr(content_obj, 'file'):
                        print(f"         file value: {content_obj.file}")
    
    else:
        print("❌ Книга 'весна' не найдена!")
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    total_books = Book.objects.count()
    books_with_files = Book.objects.filter(file__isnull=False).count()
    print(f"   Всего книг: {total_books}")
    print(f"   Книг с файлами: {books_with_files}")
    
    total_purchases = Purchase.objects.count()
    paid_purchases = Purchase.objects.filter(order__status__in=['paid', 'completed']).count()
    print(f"   Всего покупок: {total_purchases}")
    print(f"   Оплаченных покупок: {paid_purchases}")
    
    print(f"\n📋 ВСЕ КНИГИ С ФАЙЛАМИ:")
    for book in Book.objects.filter(file__isnull=False)[:5]:
        print(f"   📖 {book.title} - файл: {book.file}")
    
    print(f"\n🛒 ВСЕ ПОКУПКИ:")
    for purchase in Purchase.objects.all()[:5]:
        print(f"   💰 {purchase.user.username} - {purchase.product.title} - статус: {purchase.order.status}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
