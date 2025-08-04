# test_orders_system.py
# Скрипт для тестирования системы заказов и покупок

import os
import django
import sys
from decimal import Decimal
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Product, Cart, CartItem, Order, OrderItem, Purchase
from books.models import Book
from shop.views import complete_order

def create_test_data():
    """Создать тестовые данные для проверки системы"""
    
    print("🔧 Создание тестовых данных...")
    
    # Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Тест',
            'last_name': 'Пользователь'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Создан пользователь: {user.username}")
    else:
        print(f"📋 Пользователь уже существует: {user.username}")
    
    # Находим книги для создания товаров
    books = Book.objects.all()[:3]
    
    if not books:
        print("⚠️  Книги не найдены. Создаем тестовую книгу...")
        from books.models import Category as BookCategory
        
        category, _ = BookCategory.objects.get_or_create(
            name='Тестовая категория',
            defaults={'slug': 'test-category'}
        )
        
        book = Book.objects.create(
            title='Тестовая книга',
            slug='test-book',
            description='Описание тестовой книги',
            category=category,
            price=Decimal('299.00'),
            author='Тестовый автор'
        )
        books = [book]
        print(f"✅ Создана тестовая книга: {book.title}")
    
    # Создаем товары в магазине для каждой книги
    products = []
    for book in books:
        product, created = Product.objects.get_or_create(
            book_id=book.id,
            product_type='book',
            defaults={
                'title': book.title,
                'description': book.description,
                'price': book.price,
                'is_active': True,
                'is_digital': True,
            }
        )
        products.append(product)
        
        if created:
            print(f"✅ Создан товар: {product.title} - {product.price}₽")
        else:
            print(f"📋 Товар уже существует: {product.title}")
    
    return user, products

def create_test_order(user, products):
    """Создать тестовый заказ"""
    
    print("\n🛒 Создание тестового заказа...")
    
    # Создаем заказ
    order = Order.objects.create(
        user=user,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone='+7 123 456 78 90',
        total_amount=Decimal('0.00'),
        status='pending'
    )
    
    print(f"✅ Создан заказ #{order.short_id}")
    
    # Добавляем товары в заказ
    total_amount = Decimal('0.00')
    
    for i, product in enumerate(products[:2]):  # Берем первые 2 товара
        quantity = 1
        
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_title=product.title,
            product_price=product.price,
            quantity=quantity
        )
        
        total_amount += product.price * quantity
        print(f"✅ Добавлен товар: {product.title} x{quantity} = {product.price}₽")
    
    # Обновляем общую сумму заказа
    order.total_amount = total_amount
    order.save()
    
    print(f"💰 Общая сумма заказа: {total_amount}₽")
    
    return order

def simulate_payment(order):
    """Имитировать успешную оплату"""
    
    print(f"\n💳 Имитация оплаты заказа #{order.short_id}...")
    
    # Меняем статус на "оплачено"
    order.status = 'paid'
    order.paid_at = timezone.now()
    order.payment_method = 'test_card'
    order.payment_id = f'test_payment_{order.order_id.hex[:8]}'
    order.save()
    
    print(f"✅ Заказ #{order.short_id} успешно оплачен!")
    
    # Завершаем заказ и создаем покупки
    complete_order(order)
    
    return order

def check_purchases(user):
    """Проверить созданные покупки"""
    
    print(f"\n📦 Проверка покупок пользователя {user.username}...")
    
    purchases = Purchase.objects.filter(user=user).order_by('-purchased_at')
    
    if purchases.exists():
        print(f"✅ Найдено покупок: {purchases.count()}")
        
        for purchase in purchases:
            print(f"  📚 {purchase.product.title}")
            print(f"      Заказ: #{purchase.order.short_id}")
            print(f"      Дата: {purchase.purchased_at.strftime('%d.%m.%Y %H:%M')}")
            print(f"      Скачиваний: {purchase.download_count}")
            print("")
    else:
        print("❌ Покупки не найдены!")
    
    return purchases

def check_orders(user):
    """Проверить заказы пользователя"""
    
    print(f"\n📋 Проверка заказов пользователя {user.username}...")
    
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    if orders.exists():
        print(f"✅ Найдено заказов: {orders.count()}")
        
        for order in orders:
            print(f"  🧾 Заказ #{order.short_id}")
            print(f"      Статус: {order.get_status_display()}")
            print(f"      Сумма: {order.total_amount}₽")
            print(f"      Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}")
            
            if order.paid_at:
                print(f"      Оплачен: {order.paid_at.strftime('%d.%m.%Y %H:%M')}")
            
            # Показываем товары в заказе
            items = order.items.all()
            print(f"      Товары ({items.count()}):")
            for item in items:
                print(f"        - {item.product_title} x{item.quantity} = {item.total_price}₽")
            print("")
    else:
        print("❌ Заказы не найдены!")
    
    return orders

def run_full_test():
    """Запустить полный тест системы"""
    
    print("🚀 ТЕСТИРОВАНИЕ СИСТЕМЫ ЗАКАЗОВ И ПОКУПОК")
    print("=" * 50)
    
    try:
        # 1. Создаем тестовые данные
        user, products = create_test_data()
        
        # 2. Создаем тестовый заказ
        order = create_test_order(user, products)
        
        # 3. Проверяем заказы ДО оплаты
        print("\n📋 СОСТОЯНИЕ ДО ОПЛАТЫ:")
        check_orders(user)
        check_purchases(user)
        
        # 4. Имитируем оплату
        paid_order = simulate_payment(order)
        
        # 5. Проверяем заказы и покупки ПОСЛЕ оплаты
        print("\n📋 СОСТОЯНИЕ ПОСЛЕ ОПЛАТЫ:")
        check_orders(user)
        check_purchases(user)
        
        print("\n🎉 ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
        print("=" * 50)
        
        # Полезная информация для тестирования
        print("\n📌 ИНФОРМАЦИЯ ДЛЯ ТЕСТИРОВАНИЯ:")
        print(f"Пользователь: {user.username} (пароль: testpass123)")
        print(f"URL заказов: http://127.0.0.1:8000/shop/my-orders/")
        print(f"URL покупок: http://127.0.0.1:8000/shop/my-purchases/")
        print(f"URL тестовой оплаты: http://127.0.0.1:8000/shop/test-payment-success/{order.order_id}/")
        
        return user, order
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПРИ ТЕСТИРОВАНИИ: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def clean_test_data():
    """Очистить тестовые данные"""
    
    print("\n🧹 Очистка тестовых данных...")
    
    try:
        # Удаляем тестового пользователя и все связанные данные
        test_user = User.objects.filter(username='testuser').first()
        if test_user:
            # Django автоматически удалит связанные заказы и покупки
            test_user.delete()
            print("✅ Тестовые данные удалены")
        else:
            print("📋 Тестовые данные не найдены")
            
    except Exception as e:
        print(f"❌ Ошибка при очистке: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean_test_data()
    else:
        run_full_test()
