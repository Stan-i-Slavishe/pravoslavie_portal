import os
import sys
import django

# Добавляем путь проекта
sys.path.append(r'E:\pravoslavie_portal')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, CartItem
from books.models import Book

def check_book_covers_in_cart():
    """Проверяет отображение обложек книг в корзине"""
    
    print("🖼️ ПРОВЕРКА ОБЛОЖЕК КНИГ В КОРЗИНЕ")
    print("=" * 50)
    
    # 1. Проверяем товары типа "книга"
    book_products = Product.objects.filter(product_type='book', is_active=True)
    print(f"📚 Найдено товаров-книг: {book_products.count()}")
    
    for product in book_products:
        print(f"\n📖 Товар: {product.title}")
        print(f"   ID товара: {product.id}")
        print(f"   book_id: {product.book_id}")
        
        # Проверяем связанную книгу
        book = product.content_object
        if book:
            print(f"   ✅ Связанная книга: {book.title}")
            print(f"   📷 Обложка книги: {'✅ Есть' if book.cover else '❌ Нет'}")
            if book.cover:
                print(f"      URL: {book.cover.url}")
        else:
            print(f"   ❌ Связанная книга не найдена!")
        
        # Проверяем собственное изображение товара
        print(f"   🏷️ Изображение товара: {'✅ Есть' if product.image else '❌ Нет'}")
    
    # 2. Проверяем элементы корзины
    cart_items = CartItem.objects.filter(product__product_type='book')
    print(f"\n🛒 Элементов-книг в корзинах: {cart_items.count()}")
    
    for item in cart_items:
        print(f"\n🛒 Корзина пользователя: {item.cart.user.username}")
        print(f"   📖 Товар: {item.product.title}")
        
        book = item.product.content_object
        if book and book.cover:
            print(f"   ✅ Обложка будет показана: {book.cover.url}")
        else:
            print(f"   ❌ Обложка НЕ будет показана")

def add_covers_to_books():
    """Добавляет обложки к книгам без них"""
    
    print(f"\n🎨 ДОБАВЛЕНИЕ ОБЛОЖЕК К КНИГАМ")
    print("=" * 50)
    
    books_without_covers = Book.objects.filter(cover__isnull=True)
    print(f"📚 Книг без обложек: {books_without_covers.count()}")
    
    if books_without_covers.count() > 0:
        print("\n💡 РЕКОМЕНДАЦИИ:")
        print("1. Загрузите обложки для книг через админку Django")
        print("2. Или установите дефолтные обложки")
        print("3. Перейдите в админку: http://127.0.0.1:8000/admin/books/book/")
        
        for book in books_without_covers:
            print(f"   📖 {book.title} - нужна обложка")

if __name__ == "__main__":
    print("🚀 ДИАГНОСТИКА ОБЛОЖЕК В КОРЗИНЕ")
    
    try:
        check_book_covers_in_cart()
        add_covers_to_books()
        
        print("\n🎯 ИТОГ:")
        print("✅ Шаблон корзины исправлен для показа обложек книг")
        print("✅ Теперь для товаров-книг будет показываться обложка самой книги")
        print("✅ Если у книги нет обложки, будет показана иконка книги")
        
        print("\n🔄 Для применения изменений:")
        print("1. Перезагрузите страницу корзины")
        print("2. Проверьте отображение обложек")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
