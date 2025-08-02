#!/usr/bin/env python
"""
Исправленный скрипт для синхронизации ВСЕХ платных товаров с магазином
Работает только с существующими моделями
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
    
    print("🏪 СИНХРОНИЗАЦИЯ ВСЕХ ПЛАТНЫХ ТОВАРОВ С МАГАЗИНОМ")
    print("=" * 60)
    
    created_total = 0
    updated_total = 0
    
    # ========== 1. ПЛАТНЫЕ КНИГИ ==========
    print("\n📚 ОБРАБОТКА ПЛАТНЫХ КНИГ:")
    print("-" * 40)
    
    paid_books = Book.objects.filter(price__gt=0)
    print(f"Найдено платных книг: {paid_books.count()}")
    
    for book in paid_books:
        # Создаем или получаем товар
        product, created = Product.objects.get_or_create(
            product_type='book',
            book_id=book.id,
            defaults={
                'title': book.title,
                'description': book.description or f"Духовная книга '{book.title}' - погрузитесь в мир веры и мудрости.",
                'price': book.price,
                'is_active': True,
                'is_digital': True,
                'image': getattr(book, 'cover_image', None),
            }
        )
        
        if created:
            print(f"✅ Создана книга: {product.title} - {product.price}₽")
            created_total += 1
        else:
            # Обновляем существующий товар
            updated = False
            if product.title != book.title:
                product.title = book.title
                updated = True
            if product.price != book.price:
                product.price = book.price
                updated = True
            if not product.is_active:
                product.is_active = True
                updated = True
            if product.description != (book.description or f"Духовная книга '{book.title}' - погрузитесь в мир веры и мудрости."):
                product.description = book.description or f"Духовная книга '{book.title}' - погрузитесь в мир веры и мудрости."
                updated = True
                
            if updated:
                product.save()
                print(f"🔄 Обновлена книга: {product.title} - {product.price}₽")
                updated_total += 1
            else:
                print(f"✓ Книга актуальна: {product.title}")
    
    # ========== 2. ТЕРАПЕВТИЧЕСКИЕ СКАЗКИ ==========
    print("\n🧚 СОЗДАНИЕ ПРОДУКТОВ ДЛЯ ТЕРАПЕВТИЧЕСКИХ СКАЗОК:")
    print("-" * 40)
    
    # Создаем базовые продукты для персонализированных сказок
    fairy_tale_products = [
        {
            'title': 'Персонализированная сказка "Преодоление страхов"',
            'description': 'Индивидуальная терапевтическая сказка для помощи ребенку в преодолении страхов. Учитывает возраст, имя и особенности вашего ребенка.',
            'price': 500,
            'fairy_tale_template_id': 1,
        },
        {
            'title': 'Персонализированная сказка "Повышение самооценки"',
            'description': 'Специальная сказка для укрепления уверенности в себе. Создается индивидуально с именем и особенностями вашего ребенка.',
            'price': 500,
            'fairy_tale_template_id': 2,
        },
        {
            'title': 'Персонализированная сказка "Дружба и отношения"',
            'description': 'Терапевтическая сказка о дружбе и взаимоотношениях, персонализированная под вашего ребенка.',
            'price': 450,
            'fairy_tale_template_id': 3,
        },
        {
            'title': 'Персонализированная сказка "Учебная мотивация"',
            'description': 'Сказка для повышения интереса к учебе и развития ответственности. Адаптируется под возраст и интересы ребенка.',
            'price': 450,
            'fairy_tale_template_id': 4,
        },
        {
            'title': 'Персонализированная сказка "Семейные ценности"',
            'description': 'Православная сказка о важности семьи, любви и взаимопомощи. Включает имя ребенка и семейные традиции.',
            'price': 550,
            'fairy_tale_template_id': 5,
        },
    ]
    
    for fairy_data in fairy_tale_products:
        product, created = Product.objects.get_or_create(
            product_type='fairy_tale',
            fairy_tale_template_id=fairy_data['fairy_tale_template_id'],
            defaults={
                'title': fairy_data['title'],
                'description': fairy_data['description'],
                'price': fairy_data['price'],
                'is_active': True,
                'is_digital': True,
                'requires_personalization': True,
                'has_audio_option': True,
                'audio_option_price': 200,
                'has_illustration_option': True,
                'illustration_option_price': 300,
            }
        )
        
        if created:
            print(f"✅ Создана сказка: {product.title} - {product.price}₽")
            created_total += 1
        else:
            print(f"✓ Сказка актуальна: {product.title}")
    
    # ========== 3. СОЗДАНИЕ ПОДПИСОК ==========
    print("\n💳 СОЗДАНИЕ ПРОДУКТОВ ДЛЯ ПОДПИСОК:")
    print("-" * 40)
    
    subscription_products = [
        {
            'title': 'Месячная подписка "Добрые истории"',
            'description': 'Полный доступ к библиотеке книг, аудио и персонализированным сказкам на 1 месяц.',
            'price': 299,
            'subscription_id': 1,
        },
        {
            'title': 'Годовая подписка "Добрые истории"',
            'description': 'Полный доступ ко всему контенту на 12 месяцев. Экономия 50% по сравнению с месячной подпиской!',
            'price': 1799,
            'subscription_id': 2,
        },
        {
            'title': 'Семейная подписка',
            'description': 'Подписка для всей семьи с доступом до 5 детских профилей и неограниченными персонализированными сказками.',
            'price': 499,
            'subscription_id': 3,
        },
    ]
    
    for sub_data in subscription_products:
        product, created = Product.objects.get_or_create(
            product_type='subscription',
            subscription_id=sub_data['subscription_id'],
            defaults={
                'title': sub_data['title'],
                'description': sub_data['description'],
                'price': sub_data['price'],
                'is_active': True,
                'is_digital': True,
            }
        )
        
        if created:
            print(f"✅ Создана подписка: {product.title} - {product.price}₽")
            created_total += 1
        else:
            print(f"✓ Подписка актуальна: {product.title}")
    
    # ========== 4. ПРОВЕРКА РЕЗУЛЬТАТОВ ==========
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print("=" * 60)
    print(f"✅ Создано новых товаров: {created_total}")
    print(f"🔄 Обновлено товаров: {updated_total}")
    
    # Показываем все товары в магазине
    print(f"\n🛒 ВСЕ ТОВАРЫ В МАГАЗИНЕ:")
    print("-" * 40)
    
    all_products = Product.objects.filter(is_active=True).order_by('product_type', 'title')
    
    by_type = {}
    for product in all_products:
        product_type = product.get_product_type_display()
        if product_type not in by_type:
            by_type[product_type] = []
        by_type[product_type].append(product)
    
    total_products = 0
    total_value = 0
    for product_type, products in by_type.items():
        print(f"\n📦 {product_type.upper()} ({len(products)} товаров):")
        for product in products:
            print(f"   • {product.title} - {product.price}₽")
            total_products += 1
            total_value += float(product.price)
    
    print(f"\n🎉 ВСЕГО В МАГАЗИНЕ: {total_products} товаров")
    print(f"💰 Общая стоимость всех товаров: {total_value:.2f}₽")
    print(f"📊 Средняя цена товара: {total_value/total_products:.2f}₽")
    
    print(f"\n🎉 СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    print("🛒 Теперь все товары доступны в магазине!")
    print("🔄 Для автоматической синхронизации в будущем используются Django сигналы")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
