#!/usr/bin/env python
"""
Скрипт для инициализации системы магазина
"""
import os
import sys
import django
from pathlib import Path

# Устанавливаем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    
    # Импортируем Django модули после настройки
    from django.core.management import execute_from_command_line
    from shop.models import Product, Discount
    from books.models import Book
    from django.utils import timezone
    from datetime import timedelta
    from decimal import Decimal
    
    print("🛒 Инициализация системы магазина...")
    
    # Применяем миграции
    print("🔄 Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
    print("✅ Миграции применены!")
    
    # Создаем товары из существующих книг
    print("🔄 Создание товаров из книг...")
    books = Book.objects.filter(is_published=True)
    
    created_products = 0
    for book in books:
        # Проверяем, нет ли уже товара для этой книги
        existing_product = Product.objects.filter(
            product_type='book',
            book_id=book.id
        ).first()
        
        if not existing_product:
            # Определяем цену (бесплатные книги остаются бесплатными)
            price = book.price if not book.is_free else Decimal('0.00')
            
            product = Product.objects.create(
                title=book.title,
                description=book.description or f"Книга '{book.title}' от автора {book.author}",
                price=price,
                product_type='book',
                book_id=book.id,
                is_active=True,
                is_digital=True,
                image=book.cover
            )
            created_products += 1
            print(f"✅ Создан товар: {product.title} ({price}₽)")
    
    print(f"📦 Создано товаров: {created_products}")
    
    # Создаем несколько тестовых промокодов
    print("🔄 Создание тестовых промокодов...")
    
    now = timezone.now()
    
    # Промокоды для тестирования
    discounts_data = [
        {
            'code': 'WELCOME10',
            'description': 'Скидка 10% для новых пользователей',
            'discount_type': 'percentage',
            'discount_value': Decimal('10.00'),
            'min_amount': Decimal('100.00'),
            'valid_from': now,
            'valid_until': now + timedelta(days=30),
        },
        {
            'code': 'BOOK50',
            'description': 'Скидка 50₽ на книги',
            'discount_type': 'fixed',
            'discount_value': Decimal('50.00'),
            'min_amount': Decimal('200.00'),
            'valid_from': now,
            'valid_until': now + timedelta(days=60),
        },
        {
            'code': 'PRAVOSLAVIE',
            'description': 'Специальная скидка 15%',
            'discount_type': 'percentage',
            'discount_value': Decimal('15.00'),
            'min_amount': Decimal('300.00'),
            'max_uses': 100,
            'valid_from': now,
            'valid_until': now + timedelta(days=90),
        }
    ]
    
    created_discounts = 0
    for discount_data in discounts_data:
        discount, created = Discount.objects.get_or_create(
            code=discount_data['code'],
            defaults=discount_data
        )
        if created:
            created_discounts += 1
            print(f"✅ Создан промокод: {discount.code} ({discount.discount_value}{'%' if discount.discount_type == 'percentage' else '₽'})")
    
    print(f"🎫 Создано промокодов: {created_discounts}")
    
    # Добавляем несколько дополнительных книг с ценами для демонстрации магазина
    print("🔄 Создание дополнительных платных книг...")
    
    additional_books_data = [
        {
            'title': 'Православная психология',
            'author': 'Протоиерей Андрей Лоргус',
            'description': 'Глубокое исследование православного подхода к психологии человека.',
            'price': Decimal('299.00'),
            'pages': 320,
        },
        {
            'title': 'Молитвенный опыт святых отцов',
            'author': 'Игумен Петр (Мещеринов)',
            'description': 'Сборник наставлений о молитве от великих святых православной церкви.',
            'price': Decimal('199.00'),
            'pages': 280,
        },
        {
            'title': 'Детская исповедь',
            'author': 'Протоиерей Алексий Уминский',
            'description': 'Практическое руководство для родителей о подготовке детей к исповеди.',
            'price': Decimal('149.00'),
            'pages': 150,
        }
    ]
    
    created_books = 0
    for book_data in additional_books_data:
        # Проверяем, нет ли уже такой книги
        existing_book = Book.objects.filter(title=book_data['title']).first()
        
        if not existing_book:
            # Получаем категории для новых книг
            from books.models import Category
            spiritual_category = Category.objects.filter(name__icontains='духовн').first()
            
            book = Book.objects.create(
                title=book_data['title'],
                author=book_data['author'],
                description=book_data['description'],
                content=f"Полное содержание книги '{book_data['title']}'...",
                category=spiritual_category,
                format='pdf',
                price=book_data['price'],
                is_free=False,
                is_published=True,
                is_featured=True,
                pages=book_data['pages'],
                language='ru',
                publisher='Православное издательство',
                publication_year=2023
            )
            created_books += 1
            
            # Создаем товар для этой книги
            product = Product.objects.create(
                title=book.title,
                description=book.description,
                price=book.price,
                product_type='book',
                book_id=book.id,
                is_active=True,
                is_digital=True
            )
            
            print(f"✅ Создана книга и товар: {book.title} ({book.price}₽)")
    
    print(f"📚 Создано дополнительных книг: {created_books}")
    
    print("\n🎉 Система магазина успешно настроена!")
    print("📊 Статистика:")
    print(f"   📦 Всего товаров: {Product.objects.count()}")
    print(f"   📚 Книг-товаров: {Product.objects.filter(product_type='book').count()}")
    print(f"   🎫 Промокодов: {Discount.objects.count()}")
    print(f"   💰 Платных книг: {Book.objects.filter(is_free=False).count()}")
    print(f"   🆓 Бесплатных книг: {Book.objects.filter(is_free=True).count()}")
    
    print("\n🛒 Теперь в магазине доступно:")
    products = Product.objects.filter(is_active=True)
    for product in products:
        price_str = f"{product.price}₽" if product.price > 0 else "Бесплатно"
        print(f"   • {product.title} - {price_str}")
    
    print(f"\n🎯 Тестовые промокоды:")
    for discount in Discount.objects.filter(is_active=True):
        print(f"   • {discount.code} - {discount.description}")
    
    print("\n🚀 Что дальше:")
    print("1. Зайдите в админ-панель: http://127.0.0.1:8000/admin/")
    print("2. В разделе 'SHOP' управляйте магазином:")
    print("   - Товары (Products)")
    print("   - Корзины (Carts)")
    print("   - Заказы (Orders)")
    print("   - Покупки (Purchases)")
    print("   - Промокоды (Discounts)")
    print("3. Посетите магазин: http://127.0.0.1:8000/shop/")
    print("4. Протестируйте процесс покупки с тестовой оплатой")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
