#!/usr/bin/env python
"""
Проверка конкретной книги "Яндекс директ" (ID: 2)
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from books.models import Book

def check_specific_book():
    print("🔍 ПРОВЕРКА КНИГИ 'Яндекс директ' (ID: 2)")
    print("=" * 50)
    
    try:
        # Получаем книгу по ID
        book = Book.objects.get(id=2)
        
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
                
                # Формируем итоговое имя как в функции
                import re
                safe_title = re.sub(r'[<>:"/\\|?*]', '', book.title)
                safe_title = safe_title.strip()
                
                final_extension = file_extension if file_extension else f'.{book.format}'
                filename = f"{safe_title}{final_extension}"
                
                print(f"   Очищенное название: '{safe_title}'")
                print(f"   Итоговое расширение: '{final_extension}'")
                print(f"   🎯 ОЖИДАЕМОЕ ИМЯ ФАЙЛА: '{filename}'")
                
            else:
                print(f"   ❌ Файл НЕ существует на диске!")
                print(f"   Ожидаемый путь: {book.file.path}")
        else:
            print(f"   ❌ Поле file пустое!")
            
        # Проверяем URL для скачивания
        from django.urls import reverse
        download_url = reverse('books:download', kwargs={'book_id': book.id})
        print(f"   📥 URL для скачивания: {download_url}")
        print(f"   🌐 Полный URL: http://127.0.0.1:8000{download_url}")
        
        print("\n" + "=" * 50)
        print("🎯 ПЛАН ДЕЙСТВИЙ:")
        print("1. Перезапустите сервер: python manage.py runserver")
        print("2. Откройте: http://127.0.0.1:8000/books/book/yandeks-direkt/")
        print("3. Нажмите 'Скачать бесплатно'")
        print("4. Файл должен скачаться как: '" + filename + "'")
        
    except Book.DoesNotExist:
        print("❌ Книга с ID=2 не найдена!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_specific_book()
