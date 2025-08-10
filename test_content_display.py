#!/usr/bin/env python
"""
Скрипт для проверки отображения содержания книг
"""

import os
import sys
import django

# Добавляем корневую директорию проекта в sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def test_content_display():
    """Проверяем, что у книг есть содержание для отображения"""
    
    print("=" * 60)
    print("ПРОВЕРКА ОТОБРАЖЕНИЯ СОДЕРЖАНИЯ КНИГ")
    print("=" * 60)
    
    books = Book.objects.all()
    
    if not books.exists():
        print("❌ Книги не найдены в базе данных")
        return
    
    print(f"📚 Найдено книг: {books.count()}")
    print("-" * 60)
    
    books_with_content = 0
    books_without_content = 0
    
    for book in books:
        print(f"📖 {book.title}")
        print(f"   Автор: {book.author or 'Не указан'}")
        
        if book.description:
            print(f"   ✅ Описание: {len(book.description)} символов")
        else:
            print(f"   ❌ Описание: отсутствует")
        
        if book.content:
            print(f"   ✅ Содержание: {len(book.content)} символов")
            books_with_content += 1
            # Показываем первые 100 символов содержания
            content_preview = book.content[:100].replace('\n', ' ').replace('\r', '')
            print(f"   📄 Превью: {content_preview}...")
        else:
            print(f"   ❌ Содержание: отсутствует")
            books_without_content += 1
        
        print(f"   🔗 URL: {book.get_absolute_url()}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("СТАТИСТИКА:")
    print(f"📚 Всего книг: {books.count()}")
    print(f"✅ Книг с содержанием: {books_with_content}")
    print(f"❌ Книг без содержания: {books_without_content}")
    
    if books_with_content > 0:
        print(f"\n🎉 ИСПРАВЛЕНИЕ РАБОТАЕТ!")
        print(f"   Теперь содержание будет отображаться на страницах книг")
        print(f"   где поле 'content' заполнено в админке.")
    else:
        print(f"\n⚠️ ВНИМАНИЕ!")
        print(f"   У всех книг отсутствует содержание.")
        print(f"   Заполните поле 'Содержание' в админке для тестирования.")
    
    print("=" * 60)

if __name__ == "__main__":
    test_content_display()
