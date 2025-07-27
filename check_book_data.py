#!/usr/bin/env python
"""
Скрипт для проверки данных книги в базе данных
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from books.models import Book

def check_book_data():
    print("🔍 ПРОВЕРКА ДАННЫХ КНИГИ В БД")
    print("=" * 50)
    
    try:
        # Ищем книгу "Яндекс директ"
        books = Book.objects.filter(title__icontains="яндекс")
        
        if not books.exists():
            print("❌ Книга 'Яндекс директ' не найдена!")
            print("\nВсе книги в БД:")
            for book in Book.objects.all():
                print(f"  - ID: {book.id}, Название: {book.title}")
            return
        
        book = books.first()
        print(f"✅ Книга найдена!")
        print(f"   ID: {book.id}")
        print(f"   Название: '{book.title}'")
        print(f"   Автор: '{book.author}'")
        print(f"   Slug: '{book.slug}'")
        print(f"   Формат: '{book.format}'")
        print(f"   Бесплатная: {book.is_free}")
        print(f"   Опубликована: {book.is_published}")
        
        if book.file:
            print(f"   Файл: '{book.file.name}'")
            print(f"   Путь к файлу: '{book.file.path}'")
            
            # Проверяем существование файла
            import os
            if os.path.exists(book.file.path):
                print(f"   ✅ Файл существует на диске")
                print(f"   Размер: {os.path.getsize(book.file.path)} байт")
                
                # Анализируем расширение
                file_extension = os.path.splitext(book.file.name)[1]
                print(f"   Расширение из имени файла: '{file_extension}'")
                
                # Формируем итоговое имя
                import re
                safe_title = re.sub(r'[<>:"/\\|?*]', '', book.title)
                safe_title = safe_title.strip()
                
                final_extension = file_extension if file_extension else f'.{book.format}'
                filename = f"{safe_title}{final_extension}"
                
                print(f"   Очищенное название: '{safe_title}'")
                print(f"   Итоговое расширение: '{final_extension}'")
                print(f"   🎯 ИТОГОВОЕ ИМЯ ФАЙЛА: '{filename}'")
                
            else:
                print(f"   ❌ Файл не существует на диске!")
        else:
            print(f"   ❌ Поле file пустое!")
            
        # Проверяем URL для скачивания
        from django.urls import reverse
        download_url = reverse('books:download', kwargs={'book_id': book.id})
        print(f"   URL для скачивания: {download_url}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_book_data()
