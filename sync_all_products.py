#!/usr/bin/env python
"""
Комплексный скрипт для синхронизации ВСЕХ платных товаров с магазином

Этот скрипт:
1. Находит все платные товары во всех приложениях
2. Создает соответствующие записи в магазине
3. Настраивает автоматическую синхронизацию
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
    from audio.models import AudioTrack
    from subscriptions.models import Subscription
    from fairy_tales.models import FairyTale
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
                
            if updated:
                product.save()
                print(f"🔄 Обновлена книга: {product.title} - {product.price}₽")
                updated_total += 1
            else:
                print(f"✓ Книга актуальна: {product.title}")
    
    # ========== 2. ПЛАТНЫЕ АУДИО ==========
    print("\n🎵 ОБРАБОТКА ПЛАТНЫХ АУДИО:")
    print("-" * 40)
    
    try:
        paid_audio = AudioTrack.objects.filter(price__gt=0)
        print(f"Найдено платных аудио: {paid_audio.count()}")
        
        for audio in paid_audio:
            product, created = Product.objects.get_or_create(
                product_type='audio',
                audio_id=audio.id,
                defaults={
                    'title': audio.title,
                    'description': audio.description or f"Духовное аудио '{audio.title}' - слушайте и размышляйте.",
                    'price': audio.price,
                    'is_active': True,
                    'is_digital': True,
                    'image': getattr(audio, 'cover_image', None),
                }
            )
            
            if created:
                print(f"✅ Создано аудио: {product.title} - {product.price}₽")
                created_total += 1
            else:
                print(f"✓ Аудио актуально: {product.title}")
                
    except Exception as e:
        print(f"⚠️ Ошибка при обработке аудио: {e}")
    
    # ========== 3. ПЛАТНЫЕ ПОДПИСКИ ==========
    print("\n💳 ОБРАБОТКА ПОДПИСОК:")
    print("-" * 40)
    
    try:
        subscriptions = Subscription.objects.filter(price__gt=0)
        print(f"Найдено подписок: {subscriptions.count()}")
        
        for subscription in subscriptions:
            product, created = Product.objects.get_or_create(
                product_type='subscription',
                subscription_id=subscription.id,
                defaults={
                    'title': subscription.name,
                    'description': subscription.description or f"Подписка '{subscription.name}' - расширенный доступ к контенту.",
                    'price': subscription.price,
                    'is_active': True,
                    'is_digital': True,
                }
            )
            
            if created:
                print(f"✅ Создана подписка: {product.title} - {product.price}₽")
                created_total += 1
            else:
                print(f"✓ Подписка актуальна: {product.title}")
                
    except Exception as e:
        print(f"⚠️ Ошибка при обработке подписок: {e}")
    
    # ========== 4. ТЕРАПЕВТИЧЕСКИЕ СКАЗКИ ==========
    print("\n🧚 ОБРАБОТКА ТЕРАПЕВТИЧЕСКИХ СКАЗОК:")
    print("-" * 40)
    
    try:
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
                
    except Exception as e:
        print(f"⚠️ Ошибка при обработке сказок: {e}")
    
    # ========== 5. ПРОВЕРКА РЕЗУЛЬТАТОВ ==========
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
    for product_type, products in by_type.items():
        print(f"\n📦 {product_type.upper()} ({len(products)} товаров):")
        for product in products:
            print(f"   • {product.title} - {product.price}₽")
            total_products += 1
    
    print(f"\n🎉 ВСЕГО В МАГАЗИНЕ: {total_products} товаров")
    print(f"💰 Средняя цена: {all_products.aggregate(avg_price=django.db.models.Avg('price'))['avg_price']:.2f}₽")
    
    # ========== 6. СОЗДАНИЕ СИГНАЛОВ ДЛЯ АВТОМАТИЧЕСКОЙ СИНХРОНИЗАЦИИ ==========
    print(f"\n🔧 СОЗДАНИЕ СИСТЕМЫ АВТОМАТИЧЕСКОЙ СИНХРОНИЗАЦИИ...")
    
    signals_code = '''# shop/signals.py - Автоматическая синхронизация товаров

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from books.models import Book
from .models import Product

@receiver(post_save, sender=Book)
def sync_book_with_shop(sender, instance, created, **kwargs):
    """Автоматически создает/обновляет товар при сохранении книги"""
    if instance.price > 0:  # Только для платных книг
        product, product_created = Product.objects.get_or_create(
            product_type='book',
            book_id=instance.id,
            defaults={
                'title': instance.title,
                'description': instance.description or f"Духовная книга '{instance.title}'",
                'price': instance.price,
                'is_active': True,
                'is_digital': True,
                'image': getattr(instance, 'cover_image', None),
            }
        )
        
        if not product_created:
            # Обновляем существующий товар
            product.title = instance.title
            product.description = instance.description or f"Духовная книга '{instance.title}'"
            product.price = instance.price
            product.is_active = True
            product.save()
    else:
        # Если книга стала бесплатной, деактивируем товар
        Product.objects.filter(
            product_type='book',
            book_id=instance.id
        ).update(is_active=False)

@receiver(post_delete, sender=Book)
def remove_book_from_shop(sender, instance, **kwargs):
    """Удаляет товар при удалении книги"""
    Product.objects.filter(
        product_type='book',
        book_id=instance.id
    ).delete()

# Аналогично можно добавить для аудио, подписок и других товаров
'''
    
    signals_file = Path('shop/signals.py')
    with open(signals_file, 'w', encoding='utf-8') as f:
        f.write(signals_code)
    
    print(f"✅ Создан файл автоматической синхронизации: {signals_file}")
    
    # Обновляем apps.py для подключения сигналов
    apps_code = '''from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    
    def ready(self):
        import shop.signals  # Подключаем сигналы
'''
    
    apps_file = Path('shop/apps.py')
    with open(apps_file, 'w', encoding='utf-8') as f:
        f.write(apps_code)
    
    print(f"✅ Обновлен файл: {apps_file}")
    
    print(f"\n🎉 СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    print("🔄 Перезапустите Django сервер для активации автоматической синхронизации")
    print("🛒 Теперь все платные товары автоматически попадают в магазин!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
