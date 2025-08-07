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

print("=== ДИАГНОСТИКА КНИГИ 'ВЕЛИКАЯ КНИГА' ===")

# Поиск книги по URL
try:
    book = Book.objects.get(slug='velikaya-kniga')
    print(f"✅ Найдена книга: {book.title}")
    print(f"   ID: {book.id}")
    print(f"   Цена: {book.price} ₽")
    print(f"   Бесплатная: {book.is_free}")
    print(f"   Опубликована: {book.is_published}")
    print(f"   Автор: {book.author}")
    print()
    
    # Проверяем есть ли товар в магазине
    products = Product.objects.filter(book_id=book.id)
    print(f"Товаров в магазине для этой книги: {products.count()}")
    
    for product in products:
        print(f"   Товар: {product.title} - {product.price}₽ (Активный: {product.is_active})")
    
    print()
    print("=== ТЕСТ ДОБАВЛЕНИЯ В КОРЗИНУ ===")
    
    # Проверяем условие для добавления в корзину
    can_add_to_cart = book.price and book.price > 0
    print(f"Может быть добавлена в корзину: {can_add_to_cart}")
    
    if not can_add_to_cart:
        print("❌ ПРОБЛЕМА: Книга не может быть добавлена в корзину")
        if not book.price:
            print("   Причина: price = None")
        elif book.price <= 0:
            print(f"   Причина: price = {book.price} (должна быть > 0)")
    else:
        print("✅ Книга может быть добавлена в корзину")

except Book.DoesNotExist:
    print("❌ Книга с slug 'velikaya-kniga' не найдена!")
    
    # Попробуем найти похожие
    books = Book.objects.filter(title__icontains='велик')
    print(f"\nПохожие книги ({books.count()}):")
    for book in books:
        print(f"   {book.id}: {book.title} (slug: {book.slug}) - {book.price}₽")

except Exception as e:
    print(f"❌ Ошибка: {e}")
