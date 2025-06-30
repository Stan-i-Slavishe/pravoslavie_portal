#!/usr/bin/env python
"""
Скрипт для создания миграций и применения их для модели книг
"""
import os
import sys
import django

# Добавляем корневую директорию проекта в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_books_migrations():
    """Создание и применение миграций для книг"""
    
    print("🔄 Создание миграций для приложения books...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'books'])
        print("✅ Миграции созданы успешно!")
    except Exception as e:
        print(f"❌ Ошибка при создании миграций: {e}")
        return False
    
    print("\n🔄 Применение миграций...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Миграции применены успешно!")
    except Exception as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        return False
    
    return True

def create_sample_data():
    """Создание примеров данных"""
    from books.models import Category, Tag, Book
    
    print("\n🔄 Создание примеров данных...")
    
    # Создаем категории
    categories_data = [
        {'name': 'Духовная литература', 'icon': 'cross', 'description': 'Книги о православной вере и духовности'},
        {'name': 'Жития святых', 'icon': 'person-hearts', 'description': 'Жизнеописания православных святых'},
        {'name': 'Богословие', 'icon': 'book', 'description': 'Богословские труды и исследования'},
        {'name': 'Молитвословы', 'icon': 'chat-heart', 'description': 'Сборники молитв и богослужебные тексты'},
        {'name': 'Детская литература', 'icon': 'heart', 'description': 'Православные книги для детей'},
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'icon': cat_data['icon'],
                'description': cat_data['description']
            }
        )
        created_categories.append(category)
        if created:
            print(f"✅ Создана категория: {category.name}")
    
    # Создаем теги
    tags_data = [
        'Молитва', 'Пост', 'Святые', 'Евангелие', 'Традиции',
        'Семья', 'Воспитание', 'Духовность', 'История', 'Проповеди'
    ]
    
    created_tags = []
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        created_tags.append(tag)
        if created:
            print(f"✅ Создан тег: {tag.name}")
    
    # Создаем пример книги
    if not Book.objects.exists():
        sample_book = Book.objects.create(
            title='Житие преподобного Серафима Саровского',
            author='Архимандрит Сергий',
            description='Подробное жизнеописание одного из самых почитаемых святых Русской Православной Церкви.',
            content='Подробное содержание книги о житии преподобного Серафима...',
            category=created_categories[1] if created_categories else None,
            format='pdf',
            is_free=True,
            is_published=True,
            is_featured=True,
            pages=250,
            language='ru'
        )
        
        # Добавляем теги
        if created_tags:
            sample_book.tags.add(created_tags[0], created_tags[2])
        
        print(f"✅ Создана книга: {sample_book.title}")
    
    print("✅ Примеры данных созданы!")

if __name__ == '__main__':
    print("🚀 Инициализация системы книг...")
    
    if create_books_migrations():
        create_sample_data()
        print("\n🎉 Система книг успешно настроена!")
        print("\n📖 Теперь вы можете:")
        print("1. Зайти в админ-панель Django по адресу /admin/")
        print("2. Добавить книги в разделе 'BOOKS'")
        print("3. Настроить категории и теги")
        print("4. Просмотреть библиотеку по адресу /books/")
    else:
        print("\n❌ Не удалось настроить систему книг")
        sys.exit(1)
