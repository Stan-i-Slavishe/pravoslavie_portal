import os
import sys
import django

sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

print("📊 ПРОВЕРКА ИСПРАВЛЕНИЙ")
print("=" * 40)

books = Book.objects.all()
for book in books:
    should_be_paid = book.price > 0
    is_correctly_set = (should_be_paid and not book.is_free) or (not should_be_paid and book.is_free)
    
    status = "✅ Правильно" if is_correctly_set else "❌ Неправильно"
    
    print(f"{book.title[:25]:<25} | {book.price:>6}₽ | is_free: {book.is_free} | {status}")

print("\n🎯 ПРАВИЛО:")
print("- Если price > 0, то is_free должно быть False")
print("- Если price = 0, то is_free должно быть True")
