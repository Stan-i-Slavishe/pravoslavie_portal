from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Book, Category, Tag, BookDownload, UserFavoriteBook, BookReview
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
    if request.user.is_authenticated:
        is_favorite = UserFavoriteBook.objects.filter(
            user=request.user,
            book=book
        ).exists()
    
    # Получаем отзывы
    reviews = book.reviews.select_related('user').order_by('-created_at')
    
    context = {
        'book': book,
        'related_books': related_books,
        'is_favorite': is_favorite,
        'reviews': reviews,
        'title': book.title,
    }
    
    return render(request, 'books/book_detail.html', context)


@login_required
def download_book(request, book_id):
    """Скачивание книги - ИСПРАВЛЕНО ДЛЯ МОБИЛЬНЫХ УСТРОЙСТВ"""
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
    
    # ПРИНУДИТЕЛЬНО ИСПОЛЬЗУЕМ application/octet-stream для скачивания
    # Вместо application/pdf, чтобы браузер НЕ открывал файл для просмотра
    mime_type = 'application/octet-stream'
    
    # Возвращаем файл с принудительным скачиванием
    try:
        with open(book.file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            
            # ПРИНУДИТЕЛЬНЫЕ заголовки для скачивания (не просмотра)
            response['Content-Disposition'] = f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename_encoded}'
            response['Content-Length'] = os.path.getsize(book.file.path)
            
            # Отключаем кеширование и принудительное скачивание
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['X-Content-Type-Options'] = 'nosniff'
            response['Content-Transfer-Encoding'] = 'binary'
            
            # Дополнительные заголовки для мобильных браузеров
            response['X-Download-Options'] = 'noopen'
            response['X-Frame-Options'] = 'DENY'
            
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
