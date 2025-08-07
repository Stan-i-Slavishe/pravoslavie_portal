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

print("=== ПОИСК ВСЕХ КНИГ ===")

# Найдем все книги
books = Book.objects.all()
print(f"Всего книг: {books.count()}")

for book in books:
    print(f"ID: {book.id} | Название: {book.title}")
    print(f"   Slug: {book.slug}")
    print(f"   Цена: {book.price} ₽")
    print(f"   Бесплатная: {book.is_free}")
    print(f"   Опубликована: {book.is_published}")
    print(f"   Может быть в корзине: {book.price > 0 and not book.is_free}")
    print("-" * 50)
