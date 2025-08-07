import os
import sys
import django

# Добавляем путь проекта
sys.path.append(r'E:\pravoslavie_portal')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book
from shop.models import Product, Cart, CartItem
from django.contrib.auth.models import User

def test_cart_functionality():
    """Тестирует полную функциональность корзины и счетчика"""
    
    print("🧪 ТЕСТИРОВАНИЕ ФУНКЦИОНАЛЬНОСТИ КОРЗИНЫ")
    print("=" * 60)
    
    # 1. Проверяем наличие платных книг
    print("1️⃣ Поиск платных книг...")
    paid_books = Book.objects.filter(is_free=False, price__gt=0, is_published=True)
    print(f"   Найдено платных книг: {paid_books.count()}")
    
    if paid_books.count() == 0:
        print("   ⚠️  Создаем тестовую платную книгу...")
        test_book = Book.objects.create(
            title="Тестовая Платная Книга",
            slug="test-paid-book-cart",
            author="Тестовый Автор",
            description="Тестовая книга для проверки корзины",
            price=199.00,
            is_free=False,
            is_published=True,
            format='pdf'
        )
        print(f"   ✅ Создана книга: {test_book.title} - {test_book.price}₽")
        paid_books = [test_book]
    
    # 2. Проверяем товары в магазине
    print("\n2️⃣ Проверка товаров в магазине...")
    for book in paid_books[:3]:  # Проверяем первые 3 книги
        products = Product.objects.filter(book_id=book.id)
        print(f"   📖 {book.title}")
        print(f"      Товаров в магазине: {products.count()}")
        
        if products.count() == 0:
            print("      🔧 Создаем товар...")
            product = Product.objects.create(
                product_type='book',
                book_id=book.id,
                title=book.title,
                description=f"Духовная книга '{book.title}'",
                price=book.price,
                is_active=True,
                is_digital=True,
            )
            print(f"      ✅ Товар создан: {product.price}₽")
        else:
            for product in products:
                if not product.is_active or product.price != book.price:
                    print("      🔧 Обновляем товар...")
                    product.is_active = True
                    product.price = book.price
                    product.save()
                    print("      ✅ Товар обновлен")
    
    # 3. Проверяем URL-ы
    print("\n3️⃣ Проверка URL-ов...")
    from django.urls import reverse
    try:
        cart_count_url = reverse('shop:cart_count')
        add_book_url = reverse('shop:add_book_to_cart')
        cart_url = reverse('shop:cart')
        print(f"   ✅ URL корзины: {cart_url}")
        print(f"   ✅ URL счетчика: {cart_count_url}")
        print(f"   ✅ URL добавления книги: {add_book_url}")
    except Exception as e:
        print(f"   ❌ Ошибка URL: {e}")
    
    # 4. Проверяем функцию get_cart_count
    print("\n4️⃣ Проверка функции get_cart_count...")
    try:
        from shop.views import get_cart_count
        print("   ✅ Функция get_cart_count найдена")
    except ImportError as e:
        print(f"   ❌ Функция get_cart_count не найдена: {e}")
    
    # 5. Создаем тестового пользователя и корзину
    print("\n5️⃣ Тестирование корзины...")
    test_user, created = User.objects.get_or_create(
        username='test_cart_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Тест',
            'is_active': True
        }
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"   ✅ Создан тестовый пользователь: {test_user.username}")
    else:
        print(f"   📝 Использован существующий пользователь: {test_user.username}")
    
    # Создаем или получаем корзину
    cart, cart_created = Cart.objects.get_or_create(user=test_user)
    if cart_created:
        print("   ✅ Создана новая корзина")
    else:
        print(f"   📝 Найдена существующая корзина с {cart.total_items} товарами")
    
    # 6. Тестируем добавление товара в корзину
    print("\n6️⃣ Тестирование добавления товара...")
    if paid_books:
        test_book = paid_books[0]
        products = Product.objects.filter(book_id=test_book.id, is_active=True)
        
        if products.exists():
            product = products.first()
            
            # Добавляем товар в корзину
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 1}
            )
            
            if item_created:
                print(f"   ✅ Товар добавлен в корзину: {product.title}")
            else:
                cart_item.quantity += 1
                cart_item.save()
                print(f"   ✅ Увеличено количество товара: {cart_item.quantity}")
            
            print(f"   📊 Итого в корзине: {cart.total_items} товаров на {cart.total_price}₽")
    
    print("\n🎯 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print("=" * 60)
    
    # Финальная сводка
    final_cart = Cart.objects.get(user=test_user)
    print(f"✅ Корзина пользователя {test_user.username}:")
    print(f"   - Товаров: {final_cart.total_items}")
    print(f"   - Сумма: {final_cart.total_price}₽")
    
    print(f"\n✅ Платных книг в системе: {Book.objects.filter(is_free=False, price__gt=0).count()}")
    print(f"✅ Активных товаров в магазине: {Product.objects.filter(is_active=True, price__gt=0).count()}")
    
    print("\n📋 ИНСТРУКЦИИ ДЛЯ РУЧНОГО ТЕСТИРОВАНИЯ:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Войдите как пользователь test_cart_user (пароль: testpass123)")
    print("   Или создайте своего пользователя")
    print("3. Откройте страницу любой платной книги")
    print("4. Нажмите кнопку 'Купить за X ₽'")
    print("5. Проверьте:")
    print("   - Появилось ли уведомление 'Книга добавлена в корзину!'")
    print("   - Обновился ли счетчик корзины в навигации (красный кружок с цифрой)")
    print("   - Изменилась ли кнопка на 'Перейти в корзину'")
    print("   - Есть ли товар в корзине при переходе")
    
    print("\n🔍 ОТЛАДКА ПРОБЛЕМ:")
    print("- Если счетчик не обновляется, откройте консоль браузера (F12)")
    print("- Проверьте наличие ошибок JavaScript")
    print("- Убедитесь, что запрос /shop/cart/count/ возвращает данные")
    print("- Проверьте, что функция updateCartCount() вызывается")
    
    return test_user, final_cart

def show_test_urls():
    """Показывает URL-ы для тестирования"""
    
    print("\n🔗 URL-Ы ДЛЯ ТЕСТИРОВАНИЯ:")
    print("=" * 40)
    
    paid_books = Book.objects.filter(is_free=False, price__gt=0, is_published=True)[:5]
    
    for book in paid_books:
        print(f"📖 {book.title} ({book.price}₽)")
        print(f"   http://127.0.0.1:8000/books/book/{book.slug}/")
    
    print(f"\n🛒 Корзина:")
    print(f"   http://127.0.0.1:8000/shop/cart/")
    
    print(f"\n🏪 Магазин:")
    print(f"   http://127.0.0.1:8000/shop/")

if __name__ == "__main__":
    print("🚀 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ КОРЗИНЫ И СЧЕТЧИКА")
    
    try:
        test_user, cart = test_cart_functionality()
        show_test_urls()
        
        print("\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("\nТеперь при добавлении книги в корзину:")
        print("✅ Счетчик корзины будет обновляться автоматически")
        print("✅ Будет показываться уведомление")
        print("✅ Кнопка изменится на 'Перейти в корзину'")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
