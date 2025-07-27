#!/usr/bin/env python
"""
Диагностика проблемы с именем файла при скачивании
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from books.models import Book
import re
from urllib.parse import quote

def debug_filename_generation():
    print("🔍 ДИАГНОСТИКА ГЕНЕРАЦИИ ИМЕНИ ФАЙЛА")
    print("=" * 50)
    
    try:
        # Получаем книгу с ID=2
        book = Book.objects.get(id=2)
        
        print(f"📚 Книга: {book.title}")
        print(f"📁 Файл: {book.file.name if book.file else 'НЕТ'}")
        
        if book.file:
            # Повторяем логику из функции download_book
            file_extension = os.path.splitext(book.file.name)[1]
            print(f"🔧 Расширение из файла: '{file_extension}'")
            
            if not file_extension:
                file_extension = f'.{book.format}'
                print(f"🔧 Использован формат модели: '{file_extension}'")
            
            # Очищаем название
            safe_title = re.sub(r'[<>:"/\\|?*]', '', book.title)
            safe_title = safe_title.strip()
            print(f"🧹 Очищенное название: '{safe_title}'")
            
            # Формируем имя файла
            filename = f"{safe_title}{file_extension}"
            print(f"📄 Итоговое имя: '{filename}'")
            
            # Кодируем для URL
            filename_encoded = quote(filename.encode('utf-8'))
            print(f"🔗 Закодированное имя: '{filename_encoded}'")
            
            # Формируем заголовок Content-Disposition
            content_disp = f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename_encoded}'
            print(f"📋 Content-Disposition: {content_disp}")
            
            print("\n" + "=" * 50)
            print("🎯 ТЕСТИРОВАНИЕ РАЗЛИЧНЫХ ВАРИАНТОВ:")
            
            # Вариант 1: Простое имя без специальных символов
            simple_name = "Yandeks_direkt.pdf"
            print(f"1️⃣  Простое имя: attachment; filename=\"{simple_name}\"")
            
            # Вариант 2: Только ASCII
            ascii_name = "YandeksDirekt.pdf"
            print(f"2️⃣  ASCII имя: attachment; filename=\"{ascii_name}\"")
            
            # Вариант 3: С экранированием
            escaped_name = filename.replace('"', '\\"')
            print(f"3️⃣  Экранированное: attachment; filename=\"{escaped_name}\"")
            
            print("\n" + "=" * 50)
            print("💡 РЕКОМЕНДАЦИИ:")
            print("1. Попробовать простое ASCII имя")
            print("2. Убрать пробелы из названия")
            print("3. Проверить кодировку заголовков")
            
    except Book.DoesNotExist:
        print("❌ Книга с ID=2 не найдена!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_filename_generation()
