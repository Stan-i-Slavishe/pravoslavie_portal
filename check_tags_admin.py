"""
Скрипт для проверки и исправления отображения тегов в админке
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Tag as CoreTag
from stories.models import Story
from django.db import connection

def check_tags_display():
    """Проверяем, почему теги не отображаются в админке"""
    
    print("\n" + "=" * 70)
    print("ДИАГНОСТИКА ОТОБРАЖЕНИЯ ТЕГОВ В АДМИНКЕ")
    print("=" * 70)
    
    # 1. Проверяем все теги
    print("\n1. СТАТУС ВСЕХ ТЕГОВ:")
    print("-" * 40)
    
    all_tags = CoreTag.objects.all().order_by('name')
    
    for tag in all_tags:
        # Проверяем количество связанных рассказов
        story_count = Story.objects.filter(tags=tag).count()
        print(f"  {tag.name}: active={tag.is_active}, stories={story_count}, id={tag.id}")
    
    print(f"\nВсего тегов: {all_tags.count()}")
    print(f"Активных: {all_tags.filter(is_active=True).count()}")
    
    # 2. Проверяем дубликаты
    print("\n2. ПРОВЕРКА ДУБЛИКАТОВ:")
    print("-" * 40)
    
    # Ищем теги с похожими названиями
    duplicates = []
    tag_names = list(all_tags.values_list('name', flat=True))
    
    for name in tag_names:
        similar = CoreTag.objects.filter(name__iexact=name)
        if similar.count() > 1:
            if name.lower() not in duplicates:
                duplicates.append(name.lower())
                print(f"  ⚠️ Найден дубликат: {name}")
                for dup_tag in similar:
                    print(f"     - id={dup_tag.id}, name='{dup_tag.name}'")
    
    if not duplicates:
        print("  ✅ Дубликатов не найдено")
    
    # 3. Удаляем дубликат "папа" с маленькой буквы
    print("\n3. ИСПРАВЛЕНИЕ ДУБЛИКАТОВ:")
    print("-" * 40)
    
    # Находим теги "Папа" и "папа"
    papa_big = CoreTag.objects.filter(name='Папа').first()
    papa_small = CoreTag.objects.filter(name='папа').first()
    
    if papa_big and papa_small:
        # Переносим все связи с "папа" на "Папа"
        stories_with_small = Story.objects.filter(tags=papa_small)
        for story in stories_with_small:
            story.tags.remove(papa_small)
            story.tags.add(papa_big)
        
        # Удаляем дубликат
        papa_small.delete()
        print(f"  ✅ Удален дубликат 'папа' (id={papa_small.id})")
        print(f"  ✅ Оставлен тег 'Папа' (id={papa_big.id})")
    else:
        print("  ℹ️ Дубликаты 'Папа'/'папа' не найдены или уже исправлены")
    
    # 4. Проверяем настройки админки
    print("\n4. ПРОВЕРКА КОНФИГУРАЦИИ АДМИНКИ:")
    print("-" * 40)
    
    # Проверяем, зарегистрирован ли Tag в админке
    from django.contrib import admin
    from django.apps import apps
    
    if admin.site.is_registered(CoreTag):
        print("  ✅ Модель Tag зарегистрирована в админке")
    else:
        print("  ❌ Модель Tag НЕ зарегистрирована в админке!")
    
    # 5. Проверяем связи many-to-many
    print("\n5. СТРУКТУРА ТАБЛИЦЫ СВЯЗЕЙ:")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Проверяем структуру таблицы
        cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='stories_story_tags';
        """)
        result = cursor.fetchone()
        if result:
            print("  Структура таблицы stories_story_tags найдена")
        else:
            # Для PostgreSQL
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'stories_story_tags'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            if columns:
                print("  Колонки в stories_story_tags:")
                for col_name, col_type in columns:
                    print(f"    - {col_name}: {col_type}")

def assign_sample_tags():
    """Присваиваем теги нескольким рассказам для теста"""
    
    print("\n" + "=" * 70)
    print("ПРИСВОЕНИЕ ТЕГОВ РАССКАЗАМ (ТЕСТ)")
    print("=" * 70)
    
    # Берем первые 5 рассказов
    stories = Story.objects.all()[:5]
    
    if not stories:
        print("  ⚠️ Нет рассказов в базе данных")
        return
    
    # Присваиваем разные теги
    tag_names = ['молитва', 'чудеса', 'семья', 'исцеление', 'вразумление']
    
    for story, tag_name in zip(stories, tag_names):
        try:
            tag = CoreTag.objects.get(name=tag_name)
            if not story.tags.filter(id=tag.id).exists():
                story.tags.add(tag)
                print(f"  ✅ Рассказу '{story.title[:30]}...' добавлен тег '{tag_name}'")
            else:
                print(f"  ℹ️ У рассказа '{story.title[:30]}...' уже есть тег '{tag_name}'")
        except CoreTag.DoesNotExist:
            print(f"  ❌ Тег '{tag_name}' не найден")

def check_admin_config():
    """Проверяем конфигурацию админки для Story"""
    
    print("\n" + "=" * 70)
    print("КОНФИГУРАЦИЯ АДМИНКИ ДЛЯ STORY")
    print("=" * 70)
    
    from django.contrib import admin
    from stories.admin import StoryAdmin
    
    # Проверяем настройки StoryAdmin
    if hasattr(StoryAdmin, 'filter_horizontal'):
        print(f"  filter_horizontal: {StoryAdmin.filter_horizontal}")
    
    if hasattr(StoryAdmin, 'filter_vertical'):
        print(f"  filter_vertical: {StoryAdmin.filter_vertical}")
    
    if hasattr(StoryAdmin, 'fields'):
        print(f"  fields настроены: {bool(StoryAdmin.fields)}")
    
    if hasattr(StoryAdmin, 'fieldsets'):
        print(f"  fieldsets настроены: {bool(StoryAdmin.fieldsets)}")
    
    # Проверяем, есть ли tags в конфигурации
    print("\n  Проверка наличия 'tags' в конфигурации админки:")
    
    # Получаем форму админки
    from stories.models import Story
    model_admin = admin.site._registry.get(Story)
    if model_admin:
        print(f"  ✅ Story зарегистрирована в админке")
        
        # Проверяем форму
        if hasattr(model_admin, 'get_form'):
            print("  ✅ Метод get_form доступен")
        
        # Проверяем поля
        if hasattr(model_admin, 'get_fields'):
            try:
                # Создаем фиктивный request для проверки
                class FakeRequest:
                    user = None
                fields = model_admin.get_fields(FakeRequest())
                if 'tags' in fields:
                    print(f"  ✅ Поле 'tags' присутствует в полях админки")
                else:
                    print(f"  ❌ Поле 'tags' НЕ найдено в полях админки")
                    print(f"     Доступные поля: {fields}")
            except Exception as e:
                print(f"  ⚠️ Не удалось получить поля: {e}")

def main():
    print("\n" + "🔍" * 35)
    print("ДИАГНОСТИКА СИСТЕМЫ ТЕГОВ")
    print("🔍" * 35)
    
    # 1. Проверяем отображение
    check_tags_display()
    
    # 2. Проверяем конфигурацию админки
    check_admin_config()
    
    # 3. Присваиваем тестовые теги
    choice = input("\nПрисвоить тестовые теги нескольким рассказам? (y/n): ")
    if choice.lower() == 'y':
        assign_sample_tags()
    
    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ:")
    print("=" * 70)
    print("1. Проверьте в админке: http://127.0.0.1:8000/admin/stories/story/")
    print("2. Откройте любой рассказ для редактирования")
    print("3. Найдите поле 'Теги' - там должен быть список всех тегов")
    print("4. Если поле отсутствует, нужно проверить stories/admin.py")
    
    print("\n✅ Диагностика завершена!")

if __name__ == '__main__':
    main()
