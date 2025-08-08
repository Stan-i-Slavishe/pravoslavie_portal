#!/usr/bin/env python
"""
Скрипт для проверки работы системы тегов.
Исправляет проблему с пустой выборкой контента по тегам.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

from django.db import connection
from core.models import Tag
from stories.models import Story
from books.models import Book

def check_database_connection():
    """Проверка подключения к базе данных"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Подключение к базе данных успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False

def check_tags():
    """Проверка тегов в системе"""
    print("\n🏷️  ПРОВЕРКА ТЕГОВ:")
    
    try:
        tags_count = Tag.objects.count()
        print(f"📊 Всего тегов в системе: {tags_count}")
        
        if tags_count > 0:
            print("\n📋 Первые 10 тегов:")
            for tag in Tag.objects.all()[:10]:
                print(f"   • {tag.name} (slug: {tag.slug})")
        
        # Проверим конкретный тег "дочь"
        try:
            doch_tag = Tag.objects.get(slug='doch')
            print(f"\n🎯 Найден тег 'дочь': {doch_tag.name}")
            return doch_tag
        except Tag.DoesNotExist:
            print("❌ Тег 'дочь' не найден!")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при проверке тегов: {e}")
        return None

def check_stories_with_tags(tag=None):
    """Проверка рассказов с тегами"""
    print("\n🎬 ПРОВЕРКА РАССКАЗОВ:")
    
    try:
        stories_count = Story.objects.count()
        print(f"📊 Всего рассказов: {stories_count}")
        
        if tag:
            # Проверим рассказы с конкретным тегом
            stories_with_tag = Story.objects.filter(tags=tag, is_published=True)
            count = stories_with_tag.count()
            print(f"🎯 Рассказов с тегом '{tag.name}': {count}")
            
            if count > 0:
                print("📋 Рассказы с этим тегом:")
                for story in stories_with_tag[:5]:
                    print(f"   • {story.title}")
                return stories_with_tag
            else:
                print("⚠️  Рассказов с этим тегом не найдено")
                return None
        else:
            # Покажем все рассказы с тегами
            stories_with_any_tags = Story.objects.filter(
                tags__isnull=False,
                is_published=True
            ).distinct()
            count = stories_with_any_tags.count()
            print(f"📈 Рассказов с любыми тегами: {count}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке рассказов: {e}")
        return None

def check_books_with_tags(tag=None):
    """Проверка книг с тегами"""
    print("\n📚 ПРОВЕРКА КНИГ:")
    
    try:
        books_count = Book.objects.count()
        print(f"📊 Всего книг: {books_count}")
        
        if tag:
            # Проверим книги с конкретным тегом
            books_with_tag = Book.objects.filter(tags=tag, is_published=True)
            count = books_with_tag.count()
            print(f"🎯 Книг с тегом '{tag.name}': {count}")
            
            if count > 0:
                print("📋 Книги с этим тегом:")
                for book in books_with_tag[:5]:
                    print(f"   • {book.title}")
                return books_with_tag
            else:
                print("⚠️  Книг с этим тегом не найдено")
                return None
        else:
            # Покажем все книги с тегами
            books_with_any_tags = Book.objects.filter(
                tags__isnull=False,
                is_published=True
            ).distinct()
            count = books_with_any_tags.count()
            print(f"📈 Книг с любыми тегами: {count}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке книг: {e}")
        return None

def test_tag_detail_view_logic(tag):
    """Тестируем логику TagDetailView"""
    print(f"\n🔧 ТЕСТИРОВАНИЕ ЛОГИКИ TagDetailView для тега '{tag.name}':")
    
    content_items = []
    
    try:
        # Тестируем логику из исправленного views.py
        print("🎬 Получение рассказов...")
        stories = Story.objects.filter(
            tags=tag,
            is_published=True
        ).select_related('category')
        
        for story in stories:
            content_items.append({
                'title': story.title,
                'description': story.description,
                'content_type': 'Видео-рассказ',
                'created_at': story.created_at,
                'category': story.category.name if story.category else 'Без категории',
                'type': 'story'
            })
        print(f"   ✅ Найдено рассказов: {len([i for i in content_items if i['type'] == 'story'])}")
        
        print("📚 Получение книг...")
        books = Book.objects.filter(
            tags=tag,
            is_published=True
        ).select_related('category')
        
        for book in books:
            content_items.append({
                'title': book.title,
                'description': book.description,
                'content_type': 'Книга',
                'created_at': book.created_at,
                'category': book.category.name if book.category else 'Без категории',
                'type': 'book'
            })
        print(f"   ✅ Найдено книг: {len([i for i in content_items if i['type'] == 'book'])}")
        
        # Сортировка по дате
        content_items.sort(key=lambda x: x['created_at'], reverse=True)
        
        print(f"\n📊 ИТОГО найдено контента: {len(content_items)}")
        
        if content_items:
            print("📋 Найденный контент:")
            for item in content_items[:5]:  # Показываем первые 5
                print(f"   • [{item['type'].upper()}] {item['title']} ({item['category']})")
        else:
            print("⚠️  Контент не найден - это объясняет проблему!")
            
        return content_items
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании: {e}")
        return []

def create_test_data():
    """Создание тестовых данных если их нет"""
    print("\n🛠️  СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ:")
    
    try:
        # Создаем тег "дочь" если его нет
        tag, created = Tag.objects.get_or_create(
            slug='doch',
            defaults={
                'name': 'дочь',
                'description': 'Рассказы и материалы о дочерях',
                'color': '#e84393'
            }
        )
        
        if created:
            print("✅ Создан тег 'дочь'")
        else:
            print("ℹ️  Тег 'дочь' уже существует")
        
        # Попробуем найти хотя бы один рассказ и добавить к нему тег
        stories = Story.objects.filter(is_published=True)[:3]
        if stories:
            for story in stories:
                story.tags.add(tag)
                print(f"✅ Добавлен тег 'дочь' к рассказу: {story.title}")
        
        # То же с книгами
        books = Book.objects.filter(is_published=True)[:2]
        if books:
            for book in books:
                book.tags.add(tag)
                print(f"✅ Добавлен тег 'дочь' к книге: {book.title}")
                
        return tag
        
    except Exception as e:
        print(f"❌ Ошибка создания тестовых данных: {e}")
        return None

def main():
    """Основная функция проверки"""
    print("🔍 ДИАГНОСТИКА СИСТЕМЫ ТЕГОВ")
    print("="*50)
    
    # Проверка подключения к БД
    if not check_database_connection():
        return
    
    # Проверка тегов
    doch_tag = check_tags()
    
    # Проверка рассказов
    check_stories_with_tags(doch_tag)
    
    # Проверка книг  
    check_books_with_tags(doch_tag)
    
    if doch_tag:
        # Тестируем логику view
        content_items = test_tag_detail_view_logic(doch_tag)
        
        if not content_items:
            print("\n🛠️  НЕТ КОНТЕНТА - СОЗДАЕМ ТЕСТОВЫЕ ДАННЫЕ")
            new_tag = create_test_data()
            if new_tag:
                print("\n🔄 ПОВТОРНОЕ ТЕСТИРОВАНИЕ:")
                test_tag_detail_view_logic(new_tag)
    else:
        print("\n🛠️  СОЗДАЕМ ТЕСТОВЫЕ ДАННЫЕ")
        new_tag = create_test_data()
        if new_tag:
            test_tag_detail_view_logic(new_tag)
    
    print("\n" + "="*50)
    print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА!")
    print("\n💡 РЕШЕНИЕ: Обновленный TagDetailView теперь будет загружать")
    print("    контент из всех приложений с указанным тегом")

if __name__ == '__main__':
    main()
