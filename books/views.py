from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q, Avg, F
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import models
from .models import Book, Category, Tag, BookDownload, UserFavoriteBook, BookReview, ReadingSession, ReadingBookmark, BookChapter
from core.utils.views import track_view_session


def book_list(request):
    """Список всех книг с фильтрацией и поиском"""
    books = Book.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
    categories = Category.objects.all()
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Фильтр по категории
    category_slug = request.GET.get('category')
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    # Фильтр по формату
    format_filter = request.GET.get('format')
    if format_filter:
        books = books.filter(format=format_filter)
    
    # Фильтр по тегу
    tag_slug = request.GET.get('tag')
    if tag_slug:
        books = books.filter(tags__slug=tag_slug)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        books = books.order_by('-downloads_count')
    elif sort_by == 'rating':
        books = books.order_by('-rating')
    elif sort_by == 'title':
        books = books.order_by('title')
    else:  # newest
        books = books.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(books, 12)  # 12 книг на страницу
    page = request.GET.get('page')
    books = paginator.get_page(page)
    
    context = {
        'books': books,
        'categories': categories,
        'title': 'Библиотека',
    }
    
    return render(request, 'books/book_list.html', context)


def book_detail(request, slug):
    """Детальная страница книги"""
    book = get_object_or_404(
        Book.objects.select_related('category').prefetch_related('tags', 'reviews__user'),
        slug=slug,
        is_published=True
    )
    
    # Отслеживаем просмотр (один раз за сессию)
    track_view_session(request, book)
    
    # Похожие книги
    related_books = Book.objects.filter(
        is_published=True,
        category=book.category
    ).exclude(id=book.id)[:4]
    
    # Проверяем, добавлена ли книга в избранное текущим пользователем
    is_favorite = False
    user_can_read = book.is_free
    reading_session = None
    
    if request.user.is_authenticated:
        is_favorite = UserFavoriteBook.objects.filter(
            user=request.user,
            book=book
        ).exists()
        
        # Проверяем права на чтение
        if not book.is_free:
            from shop.models import Purchase
            user_can_read = Purchase.objects.filter(
                user=request.user,
                product__name__icontains=book.title
            ).exists()
        
        # Получаем сессию чтения если есть
        if user_can_read:
            try:
                reading_session = ReadingSession.objects.get(
                    user=request.user,
                    book=book
                )
            except ReadingSession.DoesNotExist:
                pass
    
    # Получаем отзывы
    reviews = book.reviews.select_related('user').order_by('-created_at')
    
    context = {
        'book': book,
        'related_books': related_books,
        'is_favorite': is_favorite,
        'reviews': reviews,
        'user_can_read': user_can_read,
        'reading_session': reading_session,
        'title': book.title,
    }
    
    return render(request, 'books/book_detail.html', context)


@login_required
def download_book(request, book_id):
    """Скачивание книги - ПРОСТОЕ РЕШЕНИЕ ДЛЯ ИСПРАВЛЕНИЯ ИМЕНИ"""
    import os
    
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
    
    # ПРОСТОЕ И НАДЕЖНОЕ ИМЯ ФАЙЛА (только ASCII)
    # Для книги "Яндекс директ" используем простое имя
    if book.id == 2:  # Яндекс директ
        filename = f"Yandeks_direkt{file_extension}"
    else:
        # Для других книг создаем простое ASCII имя
        filename = f"book_{book.id}{file_extension}"
    
    # ПРИНУДИТЕЛЬНО ИСПОЛЬЗУЕМ application/octet-stream
    mime_type = 'application/octet-stream'
    
    # Возвращаем файл
    try:
        with open(book.file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            
            # ПРОСТОЙ заголовок Content-Disposition (только ASCII)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = os.path.getsize(book.file.path)
            
            # Отключаем кеширование
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['X-Content-Type-Options'] = 'nosniff'
            
            return response
            
    except Exception as e:
        messages.error(request, f'Ошибка при скачивании файла: {str(e)}')
        return redirect('books:detail', slug=book.slug)


@login_required
@require_POST
def toggle_favorite(request, book_id):
    """Добавление/удаление книги из избранного"""
    try:
        book = get_object_or_404(Book, id=book_id)
        
        favorite, created = UserFavoriteBook.objects.get_or_create(
            user=request.user,
            book=book
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
            message = 'Книга удалена из избранного'
        else:
            is_favorite = True
            message = 'Книга добавлена в избранное'
        
        # Всегда возвращаем JSON для AJAX запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'is_favorite': is_favorite,
                'message': message
            })
        
        messages.success(request, message)
        return redirect('books:detail', slug=book.slug)
        
    except Exception as e:
        # Обработка ошибок для AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        
        messages.error(request, f'Ошибка: {str(e)}')
        return redirect('books:list')


@login_required
@require_POST
def add_review(request, book_id):
    """Добавление отзыва о книге"""
    book = get_object_or_404(Book, id=book_id)
    
    rating = request.POST.get('rating')
    review_text = request.POST.get('comment', '').strip()
    
    if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
        messages.error(request, 'Необходимо указать корректную оценку от 1 до 5.')
        return redirect('books:detail', slug=book.slug)
    
    # Создаем или обновляем отзыв
    review, created = BookReview.objects.update_or_create(
        book=book,
        user=request.user,
        defaults={
            'rating': int(rating),
            'comment': review_text
        }
    )
    
    # Пересчитываем средний рейтинг книги
    avg_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    book.rating = round(avg_rating, 2) if avg_rating else 0
    book.save(update_fields=['rating'])
    
    message = 'Отзыв обновлен' if not created else 'Отзыв добавлен'
    messages.success(request, f'{message}. Спасибо за вашу оценку!')
    
    return redirect('books:detail', slug=book.slug)


def category_list(request):
    """Список категорий"""
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'title': 'Категории книг',
    }
    
    return render(request, 'books/category_list.html', context)


def category_detail(request, slug):
    """Книги в определенной категории"""
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    
    context = {
        'category': category,
        'books': books,
        'title': f'Категория: {category.name}',
    }
    
    return render(request, 'books/category_detail.html', context)


@login_required
def user_favorites(request):
    """Избранные книги пользователя"""
    favorites = UserFavoriteBook.objects.filter(
        user=request.user
    ).select_related('book__category').order_by('-added_at')
    
    # Пагинация
    paginator = Paginator(favorites, 12)
    page = request.GET.get('page')
    favorites = paginator.get_page(page)
    
    context = {
        'favorites': favorites,
        'title': 'Мои избранные книги',
    }
    
    return render(request, 'books/user_favorites.html', context)


def search_books(request):
    """Поиск книг (AJAX)"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'books': []})
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query),
        is_published=True
    )[:10]
    
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'cover_url': book.cover.url if book.cover else '',
            'url': book.get_absolute_url(),
            'price': str(book.price) if not book.is_free else 'Бесплатно'
        })
    
    return JsonResponse({'books': books_data})


@require_POST
def track_book_view(request, book_id):
    """Отслеживание просмотров книги (AJAX)"""
    try:
        book = get_object_or_404(Book, id=book_id)
        
        # Отслеживаем просмотр (один раз за сессию)
        track_view_session(request, book)
        
        return JsonResponse({
            'status': 'success',
            'views_count': book.views_count
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


def get_favorites_count(request):
    """Получение количества избранных книг (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    count = UserFavoriteBook.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})


@login_required
def read_book(request, slug):
    """Чтение книги онлайн"""
    book = get_object_or_404(
        Book.objects.select_related('category').prefetch_related('chapters'),
        slug=slug,
        is_published=True
    )
    
    # Проверяем права на чтение
    user_can_read = book.is_free
    if not book.is_free:
        # Проверяем, купил ли пользователь книгу (интеграция с магазином)
        from shop.models import Purchase
        user_can_read = Purchase.objects.filter(
            user=request.user,
            product__name__icontains=book.title  # Простая проверка по названию
        ).exists()
    
    if not user_can_read:
        messages.error(request, 'У вас нет доступа к чтению этой книги. Необходимо приобрести её.')
        return redirect('books:detail', slug=book.slug)
    
    # Получаем или создаем сессию чтения
    reading_session, created = ReadingSession.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={
            'total_pages': book.pages or 100,  # Если не указано, ставим 100
        }
    )
    
    # Получаем главы если есть
    chapters = book.chapters.all().order_by('order')
    
    # Определяем шаблон в зависимости от формата книги
    if book.format == 'pdf' and book.file:
        template = 'books/reader_pdf.html'
    else:
        template = 'books/reader_html.html'
    
    context = {
        'book': book,
        'reading_session': reading_session,
        'chapters': chapters,
        'title': f'Чтение: {book.title}',
        'user_can_read': user_can_read,
    }
    
    return render(request, template, context)


@login_required
@require_POST
def update_reading_progress(request, book_id):
    """Обновление прогресса чтения (AJAX)"""
    try:
        import json
        
        book = get_object_or_404(Book, id=book_id)
        data = json.loads(request.body)
        
        current_page = data.get('current_page', 1)
        reading_time = data.get('reading_time', 0)
        
        # Получаем сессию чтения
        reading_session = get_object_or_404(
            ReadingSession,
            user=request.user,
            book=book
        )
        
        # Обновляем прогресс
        reading_session.current_page = current_page
        reading_session.reading_time += reading_time
        reading_session.save()
        
        return JsonResponse({
            'status': 'success',
            'progress_percentage': reading_session.progress_percentage,
            'reading_time': reading_session.reading_time
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def add_bookmark(request, book_id):
    """Добавление закладки (AJAX)"""
    try:
        import json
        
        book = get_object_or_404(Book, id=book_id)
        data = json.loads(request.body)
        
        page = data.get('page', 1)
        note = data.get('note', '')
        
        # Получаем сессию чтения
        reading_session = get_object_or_404(
            ReadingSession,
            user=request.user,
            book=book
        )
        
        # Проверяем, нет ли уже закладки на этой странице
        bookmark, created = ReadingBookmark.objects.get_or_create(
            session=reading_session,
            page=page,
            defaults={'note': note}
        )
        
        if not created:
            bookmark.note = note
            bookmark.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Закладка добавлена' if created else 'Закладка обновлена'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def remove_bookmark(request, book_id, bookmark_id):
    """Удаление закладки (AJAX)"""
    try:
        book = get_object_or_404(Book, id=book_id)
        
        # Получаем сессию чтения
        reading_session = get_object_or_404(
            ReadingSession,
            user=request.user,
            book=book
        )
        
        # Получаем закладку по индексу
        bookmarks = reading_session.bookmarks.all()
        if 0 <= bookmark_id < len(bookmarks):
            bookmarks[bookmark_id].delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Закладка удалена'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Закладка не найдена'
            }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
def reading_history(request):
    """История чтения пользователя"""
    reading_sessions = ReadingSession.objects.filter(
        user=request.user
    ).select_related('book').order_by('-last_read')
    
    # Пагинация
    paginator = Paginator(reading_sessions, 12)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)
    
    context = {
        'sessions': sessions,
        'title': 'История чтения',
    }
    
    return render(request, 'books/reading_history.html', context)


@login_required
def reading_stats(request):
    """Статистика чтения пользователя"""
    sessions = ReadingSession.objects.filter(user=request.user)
    
    total_books = sessions.count()
    completed_books = sessions.filter(current_page__gte=F('total_pages')).count()
    total_reading_time = sum(session.reading_time for session in sessions)
    
    # Последние прочитанные книги
    recent_books = sessions.select_related('book').order_by('-last_read')[:5]
    
    # Статистика по месяцам (последние 6 месяцев)
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_stats = sessions.filter(
        last_read__gte=six_months_ago
    ).extra(
        select={'month': 'EXTRACT(month FROM last_read)'},
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    context = {
        'total_books': total_books,
        'completed_books': completed_books,
        'total_reading_time': total_reading_time,
        'recent_books': recent_books,
        'monthly_stats': list(monthly_stats),
        'title': 'Статистика чтения',
    }
    
    return render(request, 'books/reading_stats.html', context)
