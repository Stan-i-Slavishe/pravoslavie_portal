#!/usr/bin/env python
"""
Скрипт для очистки и пересоздания системы книг
"""
import os
import sys
import django
from pathlib import Path

# Устанавливаем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    
    # Импортируем Django модули после настройки
    from django.core.management import execute_from_command_line
    from books.models import Category, Tag, Book
    
    print("🔄 Очистка и пересоздание системы книг...")
    
    # Удаляем все данные из таблиц книг
    print("🗑️ Очистка существующих данных...")
    Book.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    print("✅ Данные очищены!")
    
    # Создаем тестовые данные
    print("🔄 Создание новых тестовых данных...")
    
    # Категории
    categories_data = [
        {'name': 'Духовная литература', 'icon': 'cross', 'description': 'Книги о православной вере и духовности'},
        {'name': 'Жития святых', 'icon': 'person-hearts', 'description': 'Жизнеописания православных святых'},
        {'name': 'Богословие', 'icon': 'book', 'description': 'Богословские труды и исследования'},
        {'name': 'Молитвословы', 'icon': 'chat-heart', 'description': 'Сборники молитв и богослужебные тексты'},
        {'name': 'Детская литература', 'icon': 'heart', 'description': 'Православные книги для детей'},
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category = Category.objects.create(
            name=cat_data['name'],
            icon=cat_data['icon'], 
            description=cat_data['description']
        )
        created_categories.append(category)
        print(f"✅ Создана категория: {category.name} (slug: {category.slug})")
    
    # Теги
    tags_data = ['Молитва', 'Пост', 'Святые', 'Евангелие', 'Традиции', 'Семья', 'Воспитание', 'Духовность', 'История', 'Проповеди']
    
    created_tags = []
    for tag_name in tags_data:
        tag = Tag.objects.create(name=tag_name)
        created_tags.append(tag)
        print(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")
    
    # Примеры книг
    books_data = [
        {
            'title': 'Житие преподобного Серафима Саровского',
            'author': 'Архимандрит Сергий',
            'description': 'Подробное жизнеописание одного из самых почитаемых святых Русской Православной Церкви. Книга рассказывает о подвигах и чудесах преподобного Серафима.',
            'category_idx': 1,  # Жития святых
            'tags': [2, 8],  # Святые, Духовность
        },
        {
            'title': 'Основы православной веры',
            'author': 'Протоиерей Александр Мень',
            'description': 'Введение в основы православного вероучения для начинающих христиан.',
            'category_idx': 0,  # Духовная литература
            'tags': [3, 8],  # Евангелие, Духовность
        },
        {
            'title': 'Детский молитвослов',
            'author': 'Составитель: инокиня Мария',
            'description': 'Сборник молитв для детей с красочными иллюстрациями.',
            'category_idx': 4,  # Детская литература
            'tags': [0, 5],  # Молитва, Семья
        }
    ]
    
    for book_data in books_data:
        book = Book.objects.create(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description'],
            content=f"Полное содержание книги '{book_data['title']}'...",
            category=created_categories[book_data['category_idx']],
            format='pdf',
            is_free=True,
            is_published=True,
            is_featured=True,
            pages=200,
            language='ru',
            publisher='Православное издательство',
            publication_year=2023
        )
        
        # Добавляем теги
        for tag_idx in book_data['tags']:
            if tag_idx < len(created_tags):
                book.tags.add(created_tags[tag_idx])
        
        print(f"✅ Создана книга: {book.title} (slug: {book.slug})")
    
    print("\n🎉 Система книг успешно пересоздана!")
    print("📝 Статистика:")
    print(f"   📂 Категорий: {Category.objects.count()}")
    print(f"   🏷️ Тегов: {Tag.objects.count()}")
    print(f"   📖 Книг: {Book.objects.count()}")
    print("\n🚀 Что дальше:")
    print("1. Зайдите в админ-панель: http://127.0.0.1:8000/admin/")
    print("2. В разделе 'BOOKS' добавьте больше книг")
    print("3. Посетите библиотеку: http://127.0.0.1:8000/books/")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
