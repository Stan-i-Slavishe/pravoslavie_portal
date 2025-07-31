#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def main():
    print("=== ПРОВЕРКА КНИГИ 'ВЕЛИКАЯ КНИГА' ===")
    
    try:
        # Ищем книгу по названию (частичное совпадение)
        books = Book.objects.filter(title__icontains='Великая')
        
        if not books.exists():
            print("❌ Книга 'Великая книга' не найдена!")
            
            # Покажем все книги
            print("\n📚 Все книги в базе:")
            all_books = Book.objects.all()
            for book in all_books:
                print(f"ID: {book.id}, Название: '{book.title}', Цена: {book.price}, Бесплатная: {book.is_free}")
            return
        
        for book in books:
            print(f"\n📖 Найдена книга:")
            print(f"   ID: {book.id}")
            print(f"   Название: {book.title}")
            print(f"   Slug: {book.slug}")
            print(f"   Автор: {book.author}")
            print(f"   Цена: {book.price} ₽")
            print(f"   Бесплатная: {book.is_free}")
            print(f"   Опубликована: {book.is_published}")
            print(f"   Формат: {book.format}")
            print(f"   Файл: {book.file}")
            print(f"   Обложка: {book.cover}")
            print(f"   Категория: {book.category}")
            
            print(f"\n🔍 Анализ проблемы:")
            if book.is_free:
                print("   ✅ Книга бесплатная - кнопка 'Читать' должна отображаться")
            else:
                print("   💰 Книга платная - должна быть кнопка 'Купить'")
                
            if book.price > 0:
                print(f"   💵 Цена установлена: {book.price} ₽")
            else:
                print("   ⚠️  Цена равна 0!")
                
            # Проверим логику шаблона
            print(f"\n🎭 Логика шаблона:")
            print(f"   book.is_free = {book.is_free}")
            print(f"   book.price = {book.price}")
            
            if book.is_free:
                print("   → Должна отображаться кнопка 'Читать книгу'")
            else:
                print("   → Должна отображаться кнопка 'Купить за X ₽'")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    main()
