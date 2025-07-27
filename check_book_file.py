#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

# Проверяем книгу "Яндекс директ"
try:
    book = Book.objects.get(id=2)
    print(f"Книга найдена: {book.title}")
    print(f"Slug: {book.slug}")
    print(f"Формат: {book.format}")
    print(f"Файл: {book.file}")
    print(f"Путь к файлу: {book.file.path if book.file else 'НЕТ ФАЙЛА'}")
    print(f"URL файла: {book.file.url if book.file else 'НЕТ URL'}")
    
    if book.file:
        import os
        if os.path.exists(book.file.path):
            print(f"✅ Файл существует: {book.file.path}")
            print(f"Размер файла: {os.path.getsize(book.file.path)} байт")
        else:
            print(f"❌ Файл НЕ существует: {book.file.path}")
    else:
        print("❌ У книги нет прикрепленного файла")
        
except Book.DoesNotExist:
    print("❌ Книга с ID 2 не найдена")
except Exception as e:
    print(f"❌ Ошибка: {e}")
