#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простая инициализация магазина без Redis и эмодзи
"""
import os
import sys
import django
from pathlib import Path

# Устанавливаем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Временно отключаем Redis для этого скрипта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')

try:
    django.setup()
    
    # Импортируем Django модули после настройки
    from django.core.management import execute_from_command_line
    from shop.models import Product, Discount
    from books.models import Book, Category, Tag
    from django.utils import timezone
    from datetime import timedelta
    from decimal import Decimal
    
    print("Инициализация системы магазина...")
    
    # Применяем миграции
    print("Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
    print("Миграции применены!")
    
    # Очищаем старые данные с проблемными slug'ами
    print("Очистка старых данных...")
    Book.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Product.objects.all().delete()
    
    # Создаем категории с правильными slug'ами
    print("Создание категорий...")
    categories_data = [
        {'name': 'Духовная литература', 'icon': 'cross', 'description': 'Книги о православной вере'},
        {'name': 'Жития святых', 'icon': 'person-hearts', 'description': 'Жизнеописания святых'},
        {'name': 'Богословие', 'icon': 'book', 'description': 'Богословские труды'},
        {'name': 'Молитвословы', 'icon': 'chat-heart', 'description': 'Сборники молитв'},
        {'name': 'Детская литература', 'icon': 'heart', 'description': 'Книги для детей'},
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category = Category.objects.create(
            name=cat_data['name'],
            icon=cat_data['icon'], 
            description=cat_data['description']
        )
        created_categories.append(category)
        print(f"Создана категория: {category.name} (slug: {category.slug})")
    
    # Создаем теги
    print("Создание тегов...")
    tags_data = ['Молитва', 'Пост', 'Святые', 'Евангелие', 'Традиции', 'Семья']
    
    created_tags = []
    for tag_name in tags_data:
        tag = Tag.objects.create(name=tag_name)
        created_tags.append(tag)
        print(f"Создан тег: {tag.name} (slug: {tag.slug})")
    
    # Создаем книги
    print("Создание книг...")
    books_data = [
        {
            'title': 'Житие преподобного Серафима Саровского',
            'author': 'Архимандрит Сергий',
            'description': 'Жизнеописание великого святого Русской Церкви',
            'category_idx': 1,  # Жития святых
            'price': Decimal('0.00'),
            'is_free': True,
        },
        {
            'title': 'Основы православной веры',
            'author': 'Протоиерей Александр Мень',
            'description': 'Введение в православное вероучение',
            'category_idx': 0,  # Духовная литература
            'price': Decimal('199.00'),
            'is_free': False,
        },
        {
            'title': 'Детский молитвослов',
            'author': 'Составитель: инокиня Мария',
            'description': 'Молитвы для детей с иллюстрациями',
            'category_idx': 4,  # Детская литература
            'price': Decimal('149.00'),
            'is_free': False,
        },
        {
            'title': 'Православная психология',
            'author': 'Протоиерей Андрей Лоргус',
            'description': 'Православный взгляд на психологию человека',
            'category_idx': 2,  # Богословие
            'price': Decimal('299.00'),
            'is_free': False,
        }
    ]
    
    created_books = []
    for book_data in books_data:
        book = Book.objects.create(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description'],
            content=f"Содержание книги '{book_data['title']}'...",
            category=created_categories[book_data['category_idx']],
            format='pdf',
            price=book_data['price'],
            is_free=book_data['is_free'],
            is_published=True,
            is_featured=True,
            pages=200,
            language='ru',
            publisher='Православное издательство',
            publication_year=2023
        )
        created_books.append(book)
        
        # Добавляем теги
        if created_tags:
            book.tags.add(created_tags[0])  # Молитва
            if len(created_tags) > 2:
                book.tags.add(created_tags[2])  # Святые
        
        print(f"Создана книга: {book.title} (slug: {book.slug}) - {book.price}р")
    
    # Создаем товары из книг
    print("Создание товаров...")
    for book in created_books:
        product = Product.objects.create(
            title=book.title,
            description=book.description,
            price=book.price,
            product_type='book',
            book_id=book.id,
            is_active=True,
            is_digital=True
        )
        print(f"Создан товар: {product.title} - {product.price}р")
    
    # Создаем промокоды
    print("Создание промокодов...")
    now = timezone.now()
    
    discounts_data = [
        {
            'code': 'WELCOME10',
            'description': 'Скидка 10% для новых пользователей',
            'discount_type': 'percentage',
            'discount_value': Decimal('10.00'),
            'min_amount': Decimal('100.00'),
        },
        {
            'code': 'BOOK50',
            'description': 'Скидка 50р на книги',
            'discount_type': 'fixed',
            'discount_value': Decimal('50.00'),
            'min_amount': Decimal('200.00'),
        }
    ]
    
    for discount_data in discounts_data:
        discount_data.update({
            'valid_from': now,
            'valid_until': now + timedelta(days=30),
            'is_active': True
        })
        
        discount = Discount.objects.create(**discount_data)
        print(f"Создан промокод: {discount.code}")
    
    print("\nСистема магазина настроена!")
    print("Статистика:")
    print(f"- Категорий: {Category.objects.count()}")
    print(f"- Тегов: {Tag.objects.count()}")
    print(f"- Книг: {Book.objects.count()}")
    print(f"- Товаров: {Product.objects.count()}")
    print(f"- Промокодов: {Discount.objects.count()}")
    
    print("\nДля запуска сервера:")
    print("python manage.py runserver")
    
    print("\nСсылки:")
    print("- Магазин: http://127.0.0.1:8000/shop/")
    print("- Библиотека: http://127.0.0.1:8000/books/")
    print("- Админка: http://127.0.0.1:8000/admin/")

except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
