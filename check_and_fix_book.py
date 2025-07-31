#!/usr/bin/env python
"""
Скрипт для проверки и исправления настроек книги "Великая книга"
"""
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
    print("🔍 ПРОВЕРКА И ИСПРАВЛЕНИЕ НАСТРОЕК КНИГИ")
    print("=" * 50)
    
    try:
        # Ищем книгу по ID из URL (velikaya-kniga)
        books = Book.objects.filter(slug='velikaya-kniga')
        
        if not books.exists():
            print("❌ Книга с slug 'velikaya-kniga' не найдена!")
            
            # Попробуем найти по названию
            books = Book.objects.filter(title__icontains='Великая')
            if books.exists():
                print("✅ Найдены книги с похожим названием:")
                for book in books:
                    print(f"   - ID: {book.id}, Slug: '{book.slug}', Название: '{book.title}'")
            else:
                # Покажем все книги
                print("\n📚 Все книги в базе:")
                all_books = Book.objects.all()
                for book in all_books:
                    print(f"   - ID: {book.id}, Slug: '{book.slug}', Название: '{book.title}', Цена: {book.price} ₽, Бесплатная: {book.is_free}")
            return
        
        book = books.first()
        print(f"✅ Найдена книга: {book.title}")
        print(f"   ID: {book.id}")
        print(f"   Slug: {book.slug}")
        print(f"   Цена: {book.price} ₽")
        print(f"   Бесплатная: {book.is_free}")
        print(f"   Опубликована: {book.is_published}")
        
        # Диагностика проблемы
        print(f"\n🔍 ДИАГНОСТИКА ПРОБЛЕМЫ:")
        
        if book.is_free:
            print("   ❌ ПРОБЛЕМА: Книга помечена как бесплатная (is_free=True)")
            print("   📝 Для отображения кнопки покупки нужно is_free=False")
        else:
            print("   ✅ Книга правильно помечена как платная (is_free=False)")
        
        if book.price <= 0:
            print("   ❌ ПРОБЛЕМА: Цена книги равна 0 или отрицательная")
            print("   📝 Для отображения цены нужно установить price > 0")
        else:
            print(f"   ✅ Цена установлена корректно: {book.price} ₽")
        
        # Предлагаем исправления
        needs_fix = False
        
        if book.is_free and book.price > 0:
            print(f"\n🔧 ИСПРАВЛЕНИЕ: Устанавливаем is_free=False для платной книги")
            book.is_free = False
            needs_fix = True
        
        if book.price <= 0 and not book.is_free:
            print(f"\n🔧 ИСПРАВЛЕНИЕ: Устанавливаем цену 500 ₽ для платной книги")
            book.price = 500.00
            needs_fix = True
        
        if needs_fix:
            book.save()
            print("✅ Настройки книги исправлены и сохранены!")
            
            print(f"\n📊 ИТОГОВЫЕ НАСТРОЙКИ:")
            print(f"   Название: {book.title}")
            print(f"   Цена: {book.price} ₽")
            print(f"   Бесплатная: {book.is_free}")
            print(f"   Опубликована: {book.is_published}")
        else:
            print("\n✅ Настройки книги корректны, исправления не требуются")
        
        # Проверяем логику шаблона
        print(f"\n🎭 ЛОГИКА ОТОБРАЖЕНИЯ В ШАБЛОНЕ:")
        print(f"   user.is_authenticated = True (для авторизованного пользователя)")
        print(f"   book.is_free = {book.is_free}")
        print(f"   user_can_read = False (пользователь не купил книгу)")
        
        if book.is_free:
            print("   → Результат: Отобразится кнопка 'Читать книгу'")
        else:
            print("   → Результат: Отобразится кнопка 'Купить за X ₽'")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
