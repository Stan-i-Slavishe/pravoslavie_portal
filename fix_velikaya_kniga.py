#!/usr/bin/env python
"""
Диагностика и исправление проблемы с книгой "Великая книга"
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def main():
    print("🔍 ДИАГНОСТИКА КНИГИ 'ВЕЛИКАЯ КНИГА'")
    print("=" * 50)
    
    try:
        # Ищем книгу по slug
        book = Book.objects.get(slug='velikaya-kniga')
        
        print(f"📖 НАЙДЕНА КНИГА:")
        print(f"   ID: {book.id}")
        print(f"   Название: {book.title}")
        print(f"   Slug: {book.slug}")
        print(f"   Цена: {book.price} ₽")
        print(f"   Бесплатная: {book.is_free}")
        print(f"   Опубликована: {book.is_published}")
        
        print(f"\n🎭 АНАЛИЗ ЛОГИКИ ШАБЛОНА:")
        print(f"   Условие: user.is_authenticated = True")
        print(f"   book.is_free = {book.is_free}")
        print(f"   user_can_read = False (пользователь не купил книгу)")
        
        if book.is_free:
            print(f"   ❌ ПРОБЛЕМА: book.is_free=True")
            print(f"   → Шаблон показывает кнопку 'Читать книгу'")
            print(f"   🔧 РЕШЕНИЕ: Нужно установить is_free=False")
            
            # Исправляем
            book.is_free = False
            book.save()
            print(f"   ✅ ИСПРАВЛЕНО: is_free установлено в False")
        else:
            print(f"   ✅ Книга правильно настроена как платная")
            print(f"   → Шаблон должен показывать кнопку 'Купить за {book.price} ₽'")
        
        print(f"\n📊 ИТОГОВЫЕ НАСТРОЙКИ:")
        book.refresh_from_db()
        print(f"   Название: {book.title}")
        print(f"   Цена: {book.price} ₽")
        print(f"   Бесплатная: {book.is_free}")
        print(f"   Опубликована: {book.is_published}")
        
        print(f"\n🎯 РЕЗУЛЬТАТ:")
        if book.is_free:
            print(f"   → Будет показана кнопка: 'Читать книгу'")
        else:
            print(f"   → Будет показана кнопка: 'Купить за {book.price} ₽'")
        
    except Book.DoesNotExist:
        print("❌ Книга 'velikaya-kniga' не найдена!")
        
        # Показываем все книги
        print("\n📚 ВСЕ КНИГИ В БАЗЕ:")
        books = Book.objects.all()
        for book in books:
            print(f"   - ID:{book.id} | '{book.title}' | slug:'{book.slug}' | price:{book.price} ₽ | free:{book.is_free}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
