# Исправленная функция download_book

import os
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Book, BookDownload

@login_required
def download_book(request, book_id):
    """Скачивание книги"""
    book = get_object_or_404(Book, id=book_id, is_published=True)
    
    # Проверяем права на скачивание
    if not book.is_free and not hasattr(request.user, 'has_subscription'):
        messages.error(request, 'Для скачивания платных книг требуется подписка.')
        return redirect('books:detail', slug=book.slug)
    
    if not book.file:
        messages.error(request, 'Файл книги недоступен.')
        return redirect('books:detail', slug=book.slug)
    
    # Записываем статистику скачивания
    BookDownload.objects.create(
        book=book,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Увеличиваем счетчик скачиваний
    book.downloads_count += 1
    book.save(update_fields=['downloads_count'])
    
    # Получаем правильное расширение файла
    if book.file and book.file.name:
        # Получаем расширение из имени файла
        file_extension = os.path.splitext(book.file.name)[1]
        if not file_extension:
            file_extension = f'.{book.format}'
    else:
        file_extension = f'.{book.format}'
    
    # Создаем безопасное имя файла
    safe_title = book.title.replace('/', '_').replace('\\', '_').replace('"', '_')
    download_filename = f'{safe_title}{file_extension}'
    
    # Возвращаем файл с правильным именем и расширением
    response = HttpResponse(book.file.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{download_filename}"'
    
    return response
