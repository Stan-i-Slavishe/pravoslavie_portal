@login_required
def download_book(request, book_id):
    """Скачивание книги - УПРОЩЕННАЯ ВЕРСИЯ ДЛЯ ИСПРАВЛЕНИЯ ИМЕНИ"""
    import os
    import re
    import unicodedata
    
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
        file_extension = f'.{book.format}'
    
    # УПРОЩЕННЫЙ ПОДХОД К ГЕНЕРАЦИИ ИМЕНИ ФАЙЛА
    # Транслитерируем русские символы в латиницу
    def transliterate(text):
        """Транслитерация кириллицы в латиницу"""
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
            'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }
        
        result = ''
        for char in text:
            if char in translit_dict:
                result += translit_dict[char]
            elif char.isalnum():
                result += char
            else:
                result += '_'
        return result
    
    # Создаем безопасное ASCII имя файла
    transliterated_title = transliterate(book.title)
    # Убираем множественные подчеркивания и очищаем
    safe_title = re.sub(r'_+', '_', transliterated_title).strip('_')
    
    # Ограничиваем длину
    if len(safe_title) > 50:
        safe_title = safe_title[:50]
    
    # Формируем простое ASCII имя файла
    filename = f"{safe_title}{file_extension}"
    
    # ПРИНУДИТЕЛЬНО ИСПОЛЬЗУЕМ application/octet-stream
    mime_type = 'application/octet-stream'
    
    # Возвращаем файл с упрощенными заголовками
    try:
        with open(book.file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            
            # УПРОЩЕННЫЙ заголовок Content-Disposition (только ASCII)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = os.path.getsize(book.file.path)
            
            # Заголовки для принудительного скачивания
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['X-Content-Type-Options'] = 'nosniff'
            response['Content-Transfer-Encoding'] = 'binary'
            response['X-Download-Options'] = 'noopen'
            
            return response
            
    except Exception as e:
        messages.error(request, f'Ошибка при скачивании файла: {str(e)}')
        return redirect('books:detail', slug=book.slug)
