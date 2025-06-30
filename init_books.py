#!/usr/bin/env python
"""
Простой скрипт для инициализации системы книг
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
    
    print("🚀 Инициализация системы книг...")
    
    # Применяем миграции
    print("🔄 Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
    print("✅ Миграции применены!")
    
    # Создаем тестовые данные
    print("🔄 Создание тестовых данных...")
    
    # Категории
    categories_data = [
        {'name': 'Духовная литература', 'icon': 'cross', 'description': 'Книги о православной вере и духовности'},
        {'name': 'Жития святых', 'icon': 'person-hearts', 'description': 'Жизнеописания православных святых'},
        {'name': 'Богословие', 'icon': 'book', 'description': 'Богословские труды и исследования'},
        {'name': 'Молитвословы', 'icon': 'chat-heart', 'description': 'Сборники молитв и богослужебные тексты'},
        {'name': 'Детская литература', 'icon': 'heart', 'description': 'Православные книги для детей'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'icon': cat_data['icon'], 
                'description': cat_data['description']
            }
        )
        if created:
            print(f"✅ Создана категория: {category.name}")
    
    # Теги
    tags_data = ['Молитва', 'Пост', 'Святые', 'Евангелие', 'Традиции', 'Семья', 'Воспитание', 'Духовность', 'История', 'Проповеди']
    
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"✅ Создан тег: {tag.name}")
    
    # Пример книги
    if not Book.objects.exists():
        spiritual_category = Category.objects.filter(name='Жития святых').first()
        
        sample_book = Book.objects.create(
            title='Житие преподобного Серафима Саровского',
            author='Архимандрит Сергий',
            description='Подробное жизнеописание одного из самых почитаемых святых Русской Православной Церкви. Книга рассказывает о подвигах и чудесах преподобного Серафима.',
            content='В этой книге вы найдете полное жизнеописание преподобного Серафима Саровского...',
            category=spiritual_category,
            format='pdf',
            is_free=True,
            is_published=True,
            is_featured=True,
            pages=250,
            language='ru',
            publisher='Православное издательство',
            publication_year=2023
        )
        
        # Добавляем теги
        prayer_tag = Tag.objects.filter(name='Молитва').first()
        saints_tag = Tag.objects.filter(name='Святые').first()
        if prayer_tag:
            sample_book.tags.add(prayer_tag)
        if saints_tag:
            sample_book.tags.add(saints_tag)
        
        print(f"✅ Создана книга: {sample_book.title}")
    
    print("\n🎉 Система книг успешно настроена!")
    print("📝 Что дальше:")
    print("1. Зайдите в админ-панель: http://127.0.0.1:8000/admin/")
    print("2. В разделе 'BOOKS' вы найдете управление:")
    print("   - Книги (Books)")
    print("   - Категории (Categories)")  
    print("   - Теги (Tags)")
    print("   - Отзывы (Book reviews)")
    print("   - Скачивания (Book downloads)")
    print("3. Посетите библиотеку: http://127.0.0.1:8000/books/")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
