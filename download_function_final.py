@login_required
def download_book(request, book_id):
    """Скачивание книги - ФИНАЛЬНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    import os
    import re
    from urllib.parse import quote
    
    # Получаем книгу
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
    
    # Получаем реальное расширение файла
    file_extension = os.path.splitext(book.file.name)[1]
    if not file_extension:
        # Если расширения нет, используем формат из модели
        file_extension = f'.{book.format}'
    
    # Очищаем название книги от специальных символов
    safe_title = re.sub(r'[<>:"/\\|?*]', '', book.title)
    safe_title = safe_title.strip()
    
    # Формируем имя файла
    filename = f"{safe_title}{file_extension}"
    
    # Кодируем имя файла для безопасности
    filename_encoded = quote(filename.encode('utf-8'))
    
    # Определяем MIME тип
    mime_type = 'application/octet-stream'
    if file_extension.lower() == '.pdf':
        mime_type = 'application/pdf'
    elif file_extension.lower() == '.epub':
        mime_type = 'application/epub+zip'
    elif file_extension.lower() == '.fb2':
        mime_type = 'application/xml'
    
    # Возвращаем файл
    try:
        with open(book.file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            
            # Используем правильный заголовок Content-Disposition с поддержкой UTF-8
            response['Content-Disposition'] = f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename_encoded}'
            response['Content-Length'] = os.path.getsize(book.file.path)
            
            # Принудительно отключаем кеширование
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
            return response
            
    except Exception as e:
        messages.error(request, f'Ошибка при скачивании файла: {str(e)}')
        return redirect('books:detail', slug=book.slug)
