@echo off
echo Исправление блокировки БД для отзывов...

echo.
echo 1. Создание резервной копии...
copy "books\views.py" "books\views.py.backup_database_fix_%date:~-4,4%%date:~-10,2%%date:~-7,2%"

echo.
echo 2. Применение исправления...

python -c "
import re

# Читаем файл
with open('books/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем недостающие импорты
if 'from django.db import transaction' not in content:
    # Находим строку с импортами из django.db
    if 'from django.db import models' in content:
        content = content.replace('from django.db import models', 'from django.db import models, transaction, IntegrityError')
    else:
        # Добавляем новый импорт после других импортов Django
        import_pos = content.find('from .models import')
        if import_pos > 0:
            insert_pos = content.rfind('\n', 0, import_pos)
            content = content[:insert_pos] + '\nfrom django.db import transaction, IntegrityError' + content[insert_pos:]

# Новая функция add_review
new_function = '''@login_required
@require_POST
def add_review(request, book_id):
    \\\"\\\"\\\"Добавление отзыва о книге с защитой от блокировки БД\\\"\\\"\\\"
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
                
                # Пересчитываем средний рейтинг книги
                avg_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
                book.rating = round(avg_rating, 2) if avg_rating else 0
                book.save(update_fields=['rating'])
                
                # Если дошли сюда - операция успешна
                break
                
        except Exception as e:
            import time
            if 'database is locked' in str(e).lower() and attempt < max_retries - 1:
                # Это блокировка БД и у нас есть еще попытки
                time.sleep(retry_delay)
                retry_delay *= 2  # Экспоненциальная задержка
                continue
            else:
                # Это другая ошибка или последняя попытка
                messages.error(request, 'Произошла ошибка при добавлении отзыва. Попробуйте еще раз.')
                return redirect('books:detail', slug=book.slug)
    else:
        # Если все попытки исчерпаны
        messages.error(request, 'Сервер временно недоступен. Попробуйте позже.')
        return redirect('books:detail', slug=book.slug)
    
    message = 'Отзыв обновлен' if not created else 'Отзыв добавлен'
    messages.success(request, f'{message}. Спасибо за вашу оценку!')
    
    return redirect('books:detail', slug=book.slug)'''

# Заменяем старую функцию
old_pattern = r'@login_required\\s*@require_POST\\s*def add_review\\(request, book_id\\):.*?return redirect\\(\\'books:detail\\', slug=book\\.slug\\)'

try:
    content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
    
    # Сохраняем обновленный файл
    with open('books/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ Функция add_review успешно обновлена!')
    
except Exception as e:
    print(f'❌ Ошибка при обновлении: {e}')
"

echo.
echo 3. Проверка синтаксиса...
python manage.py check

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ИСПРАВЛЕНИЕ УСПЕШНО ПРИМЕНЕНО!
    echo.
    echo Изменения:
    echo - Добавлена защита от блокировки БД
    echo - Добавлены повторные попытки при блокировке
    echo - Улучшена обработка ошибок
    echo - Исправлен race condition в update_or_create
    echo.
    echo Теперь отзывы должны работать стабильно!
) else (
    echo.
    echo ❌ Обнаружены ошибки. Восстанавливаем резервную копию...
    copy "books\views.py.backup_database_fix_%date:~-4,4%%date:~-10,2%%date:~-7,2%" "books\views.py"
    echo Резервная копия восстановлена.
)

pause
