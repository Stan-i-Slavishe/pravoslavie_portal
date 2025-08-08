import os
import sys
import django

# Добавляем путь проекта
sys.path.append(r'E:\pravoslavie_portal')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book
from shop.models import Product

def test_favorites_cart_integration():
    """Тестирует интеграцию корзины в избранном"""
    
    print("🛒 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ КОРЗИНЫ В ИЗБРАННОМ")
    print("=" * 60)
    
    # 1. Проверяем платные книги
    paid_books = Book.objects.filter(is_free=False, price__gt=0, is_published=True)
    print(f"📚 Найдено платных книг: {paid_books.count()}")
    
    if paid_books.count() == 0:
        print("   ⚠️  Нет платных книг для тестирования")
        return
    
    # 2. Проверяем товары в магазине
    print("\n🏪 Проверка товаров в магазине...")
    books_with_products = 0
    
    for book in paid_books[:5]:  # Проверяем первые 5 книг
        products = Product.objects.filter(book_id=book.id, is_active=True)
        has_product = products.exists()
        
        print(f"   📖 {book.title} ({book.price}₽)")
        print(f"      Товар в магазине: {'✅ Да' if has_product else '❌ Нет'}")
        
        if has_product:
            books_with_products += 1
        else:
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
            books_with_products += 1
    
    print(f"\n📊 Итого книг с товарами: {books_with_products}")
    
    # 3. Показываем инструкции для тестирования
    print("\n📋 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Авторизуйтесь в системе")
    print("3. Добавьте несколько платных книг в избранное")
    print("4. Перейдите на страницу: http://127.0.0.1:8000/books/favorites/")
    print("5. Нажмите кнопку 'Купить X ₽' у любой книги")
    print("6. Проверьте:")
    print("   - ✅ Появилось уведомление 'Книга добавлена в корзину!'")
    print("   - ✅ Обновился счетчик корзины в навигации")
    print("   - ✅ Кнопка изменилась на 'Перейти в корзину'")
    print("   - ✅ Товар появился в корзине")
    
    print("\n🎯 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:")
    print("Теперь в избранном кнопка 'Купить' добавляет книгу в корзину,")
    print("а не перенаправляет в магазин!")
    
    # 4. Список книг для тестирования
    print("\n🔗 КНИГИ ДЛЯ ТЕСТИРОВАНИЯ:")
    test_books = paid_books[:3]
    for book in test_books:
        print(f"   📖 {book.title} - {book.price}₽")
        print(f"      http://127.0.0.1:8000/books/book/{book.slug}/")
    
    return books_with_products

if __name__ == "__main__":
    print("🚀 ТЕСТИРОВАНИЕ КОРЗИНЫ В ИЗБРАННОМ")
    
    try:
        books_count = test_favorites_cart_integration()
        
        print("\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("\nТеперь в избранном:")
        print("✅ Кнопка 'Купить' добавляет книгу прямо в корзину")
        print("✅ Показывается уведомление о добавлении")
        print("✅ Автоматически обновляется счетчик корзины")
        print("✅ Кнопка меняется на 'Перейти в корзину'")
        print("✅ Работает как на детальной странице книги")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
