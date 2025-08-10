#!/usr/bin/env python
"""
Проверка поля content у книги "Великая книга"
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def check_book_content():
    """Проверяет содержание поля content у книги"""
    
    print("🔍 Проверка поля 'content' у книг")
    print("=" * 50)
    
    try:
        # Ищем книгу "Великая книга"
        book = Book.objects.filter(title__icontains="Великая").first()
        
        if book:
            print(f"📚 Найдена книга: {book.title}")
            print(f"   ID: {book.id}")
            print(f"   Slug: {book.slug}")
            print(f"   Описание (description): {book.description[:100] if book.description else 'ПУСТОЕ'}...")
            print(f"   Содержание (content): {book.content[:100] if book.content else 'ПУСТОЕ'}...")
            
            if not book.content:
                print(f"\n❌ Поле 'content' ПУСТОЕ!")
                print(f"🎯 Это объясняет, почему содержание не отображается")
                print(f"📝 Решение: заполните поле 'Содержание' в админке")
                print(f"   http://127.0.0.1:8000/admin/books/book/{book.id}/change/")
            else:
                print(f"\n✅ Поле 'content' заполнено ({len(book.content)} символов)")
                print(f"🎯 Содержание должно отображаться на странице книги")
        else:
            print("❌ Книга 'Великая книга' не найдена")
            
        # Показываем все книги с заполненным content
        books_with_content = Book.objects.exclude(content="").exclude(content__isnull=True)
        
        print(f"\n📊 Книги с заполненным полем 'content': {books_with_content.count()}")
        for book in books_with_content:
            print(f"   - {book.title} (ID: {book.id})")
            
        # Показываем все книги для справки
        all_books = Book.objects.all()
        print(f"\n📖 Все книги в базе ({all_books.count()}):")
        for book in all_books:
            content_status = "✅" if book.content else "❌"
            print(f"   {content_status} {book.title} (ID: {book.id})")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_template_context():
    """Тестирует контекст шаблона"""
    print(f"\n🧪 Тестирование шаблона...")
    print("=" * 30)
    
    from django.test import RequestFactory
    from books.views import book_detail
    from django.contrib.auth.models import AnonymousUser
    
    try:
        book = Book.objects.filter(title__icontains="Великая").first()
        if book:
            # Создаем фейковый запрос
            factory = RequestFactory()
            request = factory.get(f'/books/book/{book.slug}/')
            request.user = AnonymousUser()
            request.session = {}
            
            # Вызываем view
            response = book_detail(request, book.slug)
            
            print(f"✅ View отработал без ошибок")
            print(f"   Status code: {response.status_code}")
            print(f"   Template: books/book_detail.html")
            
        else:
            print("❌ Книга не найдена для тестирования")
            
    except Exception as e:
        print(f"❌ Ошибка в тестировании view: {e}")

if __name__ == "__main__":
    try:
        check_book_content()
        test_template_context()
        
        print(f"\n" + "=" * 50)
        print(f"📋 ИНСТРУКЦИЯ ПО ИСПРАВЛЕНИЮ:")
        print(f"1. Откройте админку: http://127.0.0.1:8000/admin/books/book/")
        print(f"2. Найдите книгу 'Великая книга' и откройте её")
        print(f"3. Заполните поле 'Содержание' в разделе 'Основная информация'")
        print(f"4. Сохраните изменения")
        print(f"5. Перезагрузите страницу книги")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
