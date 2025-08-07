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

def check_specific_book():
    """Проверяет конкретную книгу 'Великая Книга'"""
    
    print("🔍 ПРОВЕРКА КНИГИ 'ВЕЛИКАЯ КНИГА'")
    print("=" * 50)
    
    try:
        # Ищем книгу по разным критериям
        possible_books = []
        
        # 1. По slug
        try:
            book = Book.objects.get(slug='velikaya-kniga')
            possible_books.append(book)
        except Book.DoesNotExist:
            print("❌ Книга с slug 'velikaya-kniga' не найдена")
        
        # 2. По названию (точное совпадение)
        try:
            book = Book.objects.get(title__iexact='Великая Книга')
            if book not in possible_books:
                possible_books.append(book)
        except Book.DoesNotExist:
            print("❌ Книга с названием 'Великая Книга' не найдена")
        
        # 3. По названию (частичное совпадение)
        books = Book.objects.filter(title__icontains='велик')
        for book in books:
            if book not in possible_books:
                possible_books.append(book)
        
        # 4. По слагу (частичное совпадение)
        books = Book.objects.filter(slug__icontains='velika')
        for book in books:
            if book not in possible_books:
                possible_books.append(book)
        
        if not possible_books:
            print("❌ Никаких подходящих книг не найдено!")
            return
        
        print(f"📚 Найдено подходящих книг: {len(possible_books)}")
        
        for i, book in enumerate(possible_books, 1):
            print(f"\n📖 Книга #{i}: {book.title}")
            print(f"   ID: {book.id}")
            print(f"   Slug: {book.slug}")
            print(f"   Автор: {book.author}")
            print(f"   Цена: {book.price} ₽")
            print(f"   Бесплатная: {book.is_free}")
            print(f"   Опубликована: {book.is_published}")
            
            # Проверяем логику корзины
            should_show_buy_button = not book.is_free and book.price and book.price > 0
            can_add_to_cart = not (book.is_free or not book.price or book.price <= 0)
            
            print(f"   Должна показываться кнопка покупки: {'✅ ДА' if should_show_buy_button else '❌ НЕТ'}")
            print(f"   Может быть добавлена в корзину: {'✅ ДА' if can_add_to_cart else '❌ НЕТ'}")
            
            # Проверяем товары в магазине
            products = Product.objects.filter(book_id=book.id)
            print(f"   Товаров в магазине: {products.count()}")
            
            for product in products:
                print(f"      📦 Товар: {product.title} - {product.price}₽")
                print(f"         Активный: {product.is_active}")
                print(f"         Тип: {product.product_type}")
            
            # Создаем товар если нужно
            if should_show_buy_button and products.count() == 0:
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
            
            print("   " + "-" * 40)
        
        # Показываем инструкции
        print("\n📋 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:")
        for i, book in enumerate(possible_books, 1):
            if not book.is_free and book.price and book.price > 0:
                print(f"   {i}. Откройте: http://127.0.0.1:8000/books/book/{book.slug}/")
                print(f"      Должна быть кнопка: 'Купить за {book.price|floatformat:0} ₽'")
    
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")
        import traceback
        traceback.print_exc()

def create_test_book():
    """Создает тестовую платную книгу"""
    
    print("\n🧪 СОЗДАНИЕ ТЕСТОВОЙ ПЛАТНОЙ КНИГИ")
    print("=" * 50)
    
    try:
        # Проверяем, есть ли уже тестовая книга
        test_book, created = Book.objects.get_or_create(
            slug='test-platnaya-kniga',
            defaults={
                'title': 'Тестовая Платная Книга',
                'author': 'Тестовый Автор',
                'description': 'Это тестовая платная книга для проверки функциональности корзины.',
                'price': 299.00,
                'is_free': False,
                'is_published': True,
                'format': 'pdf',
                'pages': 100,
            }
        )
        
        if created:
            print("✅ Создана тестовая книга:")
        else:
            print("📚 Найдена существующая тестовая книга:")
        
        print(f"   Название: {test_book.title}")
        print(f"   ID: {test_book.id}")
        print(f"   Slug: {test_book.slug}")
        print(f"   Цена: {test_book.price} ₽")
        print(f"   Бесплатная: {test_book.is_free}")
        
        # Создаем товар в магазине
        product, product_created = Product.objects.get_or_create(
            book_id=test_book.id,
            product_type='book',
            defaults={
                'title': test_book.title,
                'description': test_book.description,
                'price': test_book.price,
                'is_active': True,
                'is_digital': True,
            }
        )
        
        if product_created:
            print("✅ Создан товар в магазине:")
        else:
            print("📦 Найден существующий товар:")
        
        print(f"   Товар: {product.title} - {product.price}₽")
        print(f"   Активный: {product.is_active}")
        
        print(f"\n🔗 Ссылка для тестирования:")
        print(f"   http://127.0.0.1:8000/books/book/{test_book.slug}/")
        
    except Exception as e:
        print(f"❌ Ошибка при создании тестовой книги: {e}")

if __name__ == "__main__":
    print("🚀 ДЕТАЛЬНАЯ ДИАГНОСТИКА КНИГ И КОРЗИНЫ")
    
    check_specific_book()
    create_test_book()
    
    print("\n🎯 ГОТОВО! Теперь вы можете протестировать функциональность.")
