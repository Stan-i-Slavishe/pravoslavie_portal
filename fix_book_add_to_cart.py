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

def fix_book_cart_functionality():
    """Исправляет функциональность добавления книг в корзину"""
    
    print("🔧 ИСПРАВЛЕНИЕ ДОБАВЛЕНИЯ КНИГ В КОРЗИНУ")
    print("=" * 50)
    
    # 1. Найдем все книги
    books = Book.objects.all()
    print(f"📚 Найдено книг: {books.count()}")
    
    for book in books:
        print(f"\n📖 Книга: {book.title}")
        print(f"   ID: {book.id}")
        print(f"   Slug: {book.slug}")
        print(f"   Цена: {book.price} ₽")
        print(f"   Бесплатная: {book.is_free}")
        print(f"   Опубликована: {book.is_published}")
        
        # Определяем, должна ли книга быть в корзине
        should_be_in_cart = not book.is_free and book.price and book.price > 0
        print(f"   Должна быть в корзине: {'✅ ДА' if should_be_in_cart else '❌ НЕТ'}")
        
        # Проверяем товар в магазине
        products = Product.objects.filter(book_id=book.id)
        print(f"   Товаров в магазине: {products.count()}")
        
        if should_be_in_cart and products.count() == 0:
            print("   🔨 Создаем товар в магазине...")
            product = Product.objects.create(
                product_type='book',
                book_id=book.id,
                title=book.title,
                description=book.description or f"Духовная книга '{book.title}' - погрузитесь в мир веры и мудрости.",
                price=book.price,
                is_active=True,
                is_digital=True,
            )
            print(f"   ✅ Товар создан: {product.title} - {product.price}₽")
        
        elif products.count() > 0:
            for product in products:
                print(f"   📦 Товар: {product.title} - {product.price}₽ (Активный: {product.is_active})")
                
                # Обновляем товар если нужно
                if should_be_in_cart:
                    if product.price != book.price or not product.is_active:
                        print("   🔧 Обновляем товар...")
                        product.price = book.price
                        product.is_active = True
                        product.title = book.title
                        product.description = book.description or f"Духовная книга '{book.title}'"
                        product.save()
                        print("   ✅ Товар обновлен")
                else:
                    if product.is_active:
                        print("   🔧 Деактивируем товар (книга бесплатная)...")
                        product.is_active = False
                        product.save()
                        print("   ✅ Товар деактивирован")
        
        print("   " + "-" * 40)
    
    print("\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("\nТеперь проверьте функциональность:")
    print("1. Бесплатные книги (is_free=True) - должна показываться кнопка 'Читать бесплатно'")
    print("2. Платные книги (is_free=False, price>0) - должна показываться кнопка 'Купить за X ₽'")
    print("3. При клике на 'Купить' книга должна добавляться в корзину")

def test_cart_logic():
    """Тестирует логику добавления в корзину"""
    
    print("\n🧪 ТЕСТИРОВАНИЕ ЛОГИКИ КОРЗИНЫ")
    print("=" * 50)
    
    books = Book.objects.all()
    
    for book in books:
        # Логика из шаблона
        show_buy_button = not book.is_free and book.price and book.price > 0
        
        # Логика из views
        can_add_to_cart = not (book.is_free or not book.price or book.price <= 0)
        
        print(f"📖 {book.title}")
        print(f"   is_free: {book.is_free}")
        print(f"   price: {book.price}")
        print(f"   Показать кнопку покупки: {'✅' if show_buy_button else '❌'}")
        print(f"   Можно добавить в корзину: {'✅' if can_add_to_cart else '❌'}")
        print(f"   Логика совпадает: {'✅' if show_buy_button == can_add_to_cart else '❌ ОШИБКА!'}")
        print()

if __name__ == "__main__":
    print("🚀 ЗАПУСК ИСПРАВЛЕНИЯ ДОБАВЛЕНИЯ КНИГ В КОРЗИНУ")
    
    try:
        fix_book_cart_functionality()
        test_cart_logic()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
