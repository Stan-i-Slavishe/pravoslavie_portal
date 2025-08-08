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

def diagnose_book_pricing():
    """Диагностирует проблемы с ценообразованием книг"""
    
    print("🔍 ДИАГНОСТИКА ПРОБЛЕМ С ЦЕНООБРАЗОВАНИЕМ")
    print("=" * 60)
    
    # 1. Найдем все книги с неправильными настройками
    problem_books = Book.objects.filter(price__gt=0, is_free=True)
    print(f"📚 Книги с ценой > 0, но is_free=True: {problem_books.count()}")
    
    for book in problem_books:
        print(f"   📖 {book.title}")
        print(f"      ID: {book.id}")
        print(f"      Цена: {book.price} ₽")
        print(f"      Бесплатная: {book.is_free}")
        print(f"      Опубликована: {book.is_published}")
        print()
    
    # 2. Найдем все книги
    all_books = Book.objects.all()
    print(f"📊 СТАТИСТИКА ВСЕХ КНИГ ({all_books.count()})")
    
    free_books = all_books.filter(is_free=True)
    paid_books = all_books.filter(is_free=False)
    books_with_price = all_books.filter(price__gt=0)
    
    print(f"   ✅ Бесплатных книг (is_free=True): {free_books.count()}")
    print(f"   💰 Платных книг (is_free=False): {paid_books.count()}")
    print(f"   💵 Книг с ценой > 0: {books_with_price.count()}")
    
    # 3. Анализируем каждую книгу
    print(f"\n📋 АНАЛИЗ КАЖДОЙ КНИГИ:")
    for book in all_books:
        status = "🟢 Корректно"
        if book.price > 0 and book.is_free:
            status = "🔴 ПРОБЛЕМА: Цена > 0, но is_free=True"
        elif book.price == 0 and not book.is_free:
            status = "🟡 ВНИМАНИЕ: Цена = 0, но is_free=False"
        
        print(f"   📖 {book.title[:30]:<30} | Цена: {book.price:>6} ₽ | Бесплатная: {book.is_free} | {status}")
    
    return problem_books

def fix_book_pricing():
    """Исправляет проблемы с ценообразованием"""
    
    print("\n🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ С ЦЕНООБРАЗОВАНИЕМ")
    print("=" * 60)
    
    # Исправляем книги с ценой > 0, но is_free=True
    problem_books = Book.objects.filter(price__gt=0, is_free=True)
    
    if problem_books.count() == 0:
        print("✅ Проблемных книг не найдено!")
        return
    
    print(f"🔧 Исправляем {problem_books.count()} книг...")
    
    for book in problem_books:
        print(f"   📖 Исправляем: {book.title}")
        print(f"      До: price={book.price}, is_free={book.is_free}")
        
        # Если у книги есть цена > 0, делаем её платной
        book.is_free = False
        book.save()
        
        print(f"      После: price={book.price}, is_free={book.is_free}")
        
        # Обновляем товар в магазине
        products = Product.objects.filter(book_id=book.id)
        for product in products:
            if not product.is_active:
                product.is_active = True
                product.save()
                print(f"      ✅ Активирован товар в магазине")
    
    print(f"\n✅ Исправлено {problem_books.count()} книг!")

def create_test_books():
    """Создает тестовые книги с правильными настройками"""
    
    print(f"\n📝 СОЗДАНИЕ ТЕСТОВЫХ КНИГ")
    print("=" * 60)
    
    # Создаем бесплатную книгу
    free_book, created = Book.objects.get_or_create(
        slug='test-free-book',
        defaults={
            'title': 'Тестовая Бесплатная Книга',
            'author': 'Тестовый Автор',
            'description': 'Это тестовая бесплатная книга',
            'price': 0.00,
            'is_free': True,
            'is_published': True,
            'format': 'pdf'
        }
    )
    
    if created:
        print(f"✅ Создана бесплатная книга: {free_book.title}")
    
    # Создаем платную книгу
    paid_book, created = Book.objects.get_or_create(
        slug='test-paid-book-correct',
        defaults={
            'title': 'Тестовая Платная Книга (Исправленная)',
            'author': 'Тестовый Автор',
            'description': 'Это тестовая платная книга с правильными настройками',
            'price': 299.00,
            'is_free': False,  # ← ПРАВИЛЬНО!
            'is_published': True,
            'format': 'pdf'
        }
    )
    
    if created:
        print(f"✅ Создана платная книга: {paid_book.title}")
        
        # Создаем товар в магазине
        product, product_created = Product.objects.get_or_create(
            book_id=paid_book.id,
            product_type='book',
            defaults={
                'title': paid_book.title,
                'description': paid_book.description,
                'price': paid_book.price,
                'is_active': True,
                'is_digital': True,
            }
        )
        
        if product_created:
            print(f"✅ Создан товар в магазине: {product.title}")

if __name__ == "__main__":
    print("🚀 ДИАГНОСТИКА И ИСПРАВЛЕНИЕ ЦЕНООБРАЗОВАНИЯ")
    
    try:
        # 1. Диагностика
        problem_books = diagnose_book_pricing()
        
        # 2. Исправление
        fix_book_pricing()
        
        # 3. Создание тестовых книг
        create_test_books()
        
        print("\n🎯 ИТОГОВЫЕ РЕКОМЕНДАЦИИ:")
        print("1. Для ПЛАТНЫХ книг: is_free=False И price>0")
        print("2. Для БЕСПЛАТНЫХ книг: is_free=True И price=0")
        print("3. Проверьте товары в магазине после исправления")
        
        print("\n🧪 ТЕСТИРОВАНИЕ:")
        print("1. python manage.py runserver")
        print("2. Откройте исправленные книги")
        print("3. Проверьте кнопки 'Купить' для платных книг")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
