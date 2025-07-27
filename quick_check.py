import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

from books.models import Book

# Ищем книгу Яндекс директ
books = Book.objects.filter(title__icontains="яндекс")

if books.exists():
    book = books.first()
    print(f"Книга найдена: {book.title}")
    print(f"ID: {book.id}")
    print(f"Файл: {book.file.name if book.file else 'НЕТ'}")
    
    if book.file:
        import os
        file_extension = os.path.splitext(book.file.name)[1]
        print(f"Расширение: '{file_extension}'")
        
        import re
        safe_title = re.sub(r'[<>:"/\\|?*]', '', book.title).strip()
        final_ext = file_extension if file_extension else f'.{book.format}'
        filename = f"{safe_title}{final_ext}"
        
        print(f"Должно быть имя файла: '{filename}'")
    
    # URL для скачивания
    from django.urls import reverse
    url = reverse('books:download', kwargs={'book_id': book.id})
    print(f"URL: {url}")
else:
    print("Книга не найдена!")
    print("Все книги:")
    for b in Book.objects.all()[:5]:
        print(f"  - {b.title}")
