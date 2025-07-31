#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

print("🔍 ПРОВЕРКА ФАЙЛОВ КНИГ В БАЗЕ ДАННЫХ")
print("=" * 50)

books = Book.objects.all()

if not books:
    print("❌ Книги не найдены в базе данных")
else:
    for book in books:
        print(f"\n📖 Книга: {book.title}")
        print(f"   ID: {book.id}")
        print(f"   Slug: {book.slug}")
        print(f"   Формат: {book.format}")
        
        if book.file:
            print(f"   ✅ Файл: {book.file.name}")
            print(f"   📁 Путь: {book.file.path if book.file else 'НЕТ'}")
            
            # Проверяем существует ли файл физически
            if book.file and os.path.exists(book.file.path):
                print(f"   💾 Файл существует: ДА")
            else:
                print(f"   ❌ Файл существует: НЕТ")
        else:
            print(f"   ❌ Файл: НЕТ ФАЙЛА")
            print("   🚨 ПРОБЛЕМА: У книги нет файла!")
            print("   💡 РЕШЕНИЕ: Добавьте файл через админку Django")

print(f"\n📊 Всего книг: {books.count()}")
books_with_files = books.exclude(file='')
print(f"📁 Книг с файлами: {books_with_files.count()}")
print(f"❌ Книг без файлов: {books.count() - books_with_files.count()}")

print("\n🎯 ВЫВОД:")
if books_with_files.count() == 0:
    print("❌ НИ У ОДНОЙ КНИГИ НЕТ ФАЙЛА!")
    print("💡 Добавьте файлы к книгам через админку: /admin/books/book/")
else:
    print(f"✅ У {books_with_files.count()} книг есть файлы")
    if books.count() - books_with_files.count() > 0:
        print(f"⚠️  У {books.count() - books_with_files.count()} книг нет файлов")
