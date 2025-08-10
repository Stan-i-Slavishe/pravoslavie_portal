"""
Исправленная функция add_review с обработкой блокировки SQLite
"""

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.db import transaction, IntegrityError
import time
import logging

logger = logging.getLogger(__name__)

@login_required
@require_POST
def add_review(request, book_id):
    """Добавление отзыва о книге с защитой от блокировки БД"""
    book = get_object_or_404(Book, id=book_id)
    
    rating = request.POST.get('rating')
    review_text = request.POST.get('comment', '').strip()
    
    if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
        messages.error(request, 'Необходимо указать корректную оценку от 1 до 5.')
        return redirect('books:detail', slug=book.slug)
    
    rating = int(rating)
    
    # Попытки с повторными попытками при блокировке БД
    max_retries = 3
    retry_delay = 0.1  # 100ms
    
    for attempt in range(max_retries):
        try:
            with transaction.atomic():
                # Используем более безопасный подход без update_or_create
                try:
                    # Пытаемся найти существующий отзыв
                    review = BookReview.objects.select_for_update().get(
                        book=book,
                        user=request.user
                    )
                    # Обновляем существующий отзыв
                    review.rating = rating
                    review.comment = review_text
                    review.save()
                    created = False
                    
                except BookReview.DoesNotExist:
                    # Создаем новый отзыв
                    try:
                        review = BookReview.objects.create(
                            book=book,
                            user=request.user,
                            rating=rating,
                            comment=review_text
                        )
                        created = True
                    except IntegrityError:
                        # Если отзыв был создан другим процессом между проверкой и созданием
                        # Повторяем попытку обновления
                        review = BookReview.objects.select_for_update().get(
                            book=book,
                            user=request.user
                        )
                        review.rating = rating
                        review.comment = review_text
                        review.save()
                        created = False
                
                # Пересчитываем средний рейтинг книги в отдельной транзакции
                avg_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
                book.rating = round(avg_rating, 2) if avg_rating else 0
                book.save(update_fields=['rating'])
                
                # Если дошли сюда - операция успешна
                break
                
        except Exception as e:
            if 'database is locked' in str(e).lower() and attempt < max_retries - 1:
                # Это блокировка БД и у нас есть еще попытки
                logger.warning(f"Database locked on attempt {attempt + 1}, retrying in {retry_delay}s")
                time.sleep(retry_delay)
                retry_delay *= 2  # Экспоненциальная задержка
                continue
            else:
                # Это другая ошибка или последняя попытка
                logger.error(f"Error adding review: {str(e)}")
                messages.error(request, 'Произошла ошибка при добавлении отзыва. Попробуйте еще раз.')
                return redirect('books:detail', slug=book.slug)
    else:
        # Если все попытки исчерпаны
        messages.error(request, 'Сервер временно недоступен. Попробуйте позже.')
        return redirect('books:detail', slug=book.slug)
    
    message = 'Отзыв обновлен' if not created else 'Отзыв добавлен'
    messages.success(request, f'{message}. Спасибо за вашу оценку!')
    
    return redirect('books:detail', slug=book.slug)
