import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

from core.models import Tag
from stories.models import Story
from books.models import Book

# Находим тег "дочь"
try:
    tag = Tag.objects.get(slug='doch')
    print(f"Найден тег: {tag.name} (slug: {tag.slug})")
    
    # Проверяем истории с этим тегом
    stories = Story.objects.filter(tags=tag, is_published=True)
    print(f"Историй с тегом 'дочь': {stories.count()}")
    
    for story in stories:
        print(f"  - {story.title}")
    
    # Проверяем книги с этим тегом
    books = Book.objects.filter(tags=tag, is_published=True)
    print(f"Книг с тегом 'дочь': {books.count()}")
    
    for book in books:
        print(f"  - {book.title}")
    
    # Проверим все истории и их теги
    print("\nВсе истории и их теги:")
    all_stories = Story.objects.filter(is_published=True).prefetch_related('tags')
    for story in all_stories:
        tag_names = [t.name for t in story.tags.all()]
        print(f"  {story.title}: {tag_names}")
        
    # Проверим все книги и их теги
    print("\nВсе книги и их теги:")
    all_books = Book.objects.filter(is_published=True).prefetch_related('tags')
    for book in all_books:
        tag_names = [t.name for t in book.tags.all()]
        print(f"  {book.title}: {tag_names}")
        
except Tag.DoesNotExist:
    print("Тег 'дочь' не найден")
except Exception as e:
    print(f"Ошибка: {e}")
