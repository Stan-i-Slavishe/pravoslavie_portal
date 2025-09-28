"""
Скрипт для анализа и синхронизации тегов между core.Tag и stories
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

def analyze_tags():
    """Анализируем текущее состояние тегов"""
    
    print("=" * 70)
    print("АНАЛИЗ ТЕГОВ В СИСТЕМЕ")
    print("=" * 70)
    
    # 1. Теги в core.Tag
    print("\n1. ТЕГИ В МОДЕЛИ core.Tag:")
    print("-" * 40)
    core_tags = CoreTag.objects.all().order_by('name')
    
    if core_tags.exists():
        for tag in core_tags:
            print(f"  - {tag.name} (slug: {tag.slug}, активен: {tag.is_active})")
        print(f"\nВсего тегов в core.Tag: {core_tags.count()}")
    else:
        print("  НЕТ ТЕГОВ В core.Tag!")
    
    # 2. Проверяем связи stories с тегами
    print("\n2. АНАЛИЗ СВЯЗЕЙ С ТЕГАМИ В STORIES:")
    print("-" * 40)
    
    # Смотрим структуру таблицы many-to-many
    with connection.cursor() as cursor:
        # Проверяем, какие таблицы есть для связи тегов
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE '%tag%'
            ORDER BY name;
        """)
        tables = cursor.fetchall()
        
        print("Таблицы с тегами в БД:")
        for table in tables:
            print(f"  - {table[0]}")
            
        # Проверяем содержимое таблицы stories_story_tags
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM stories_story_tags;
            """)
            count = cursor.fetchone()[0]
            print(f"\nСвязей в stories_story_tags: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT DISTINCT tag_id FROM stories_story_tags;
                """)
                tag_ids = [row[0] for row in cursor.fetchall()]
                print(f"Уникальные ID тегов в stories: {tag_ids}")
                
                # Проверяем, существуют ли эти теги в core_tag
                existing_tags = CoreTag.objects.filter(id__in=tag_ids)
                print(f"Из них существует в core.Tag: {existing_tags.count()}")
                
                if existing_tags.exists():
                    print("Существующие теги:")
                    for tag in existing_tags:
                        # Считаем количество историй с этим тегом
                        cursor.execute("""
                            SELECT COUNT(*) FROM stories_story_tags WHERE tag_id = %s;
                        """, [tag.id])
                        story_count = cursor.fetchone()[0]
                        print(f"  - {tag.name}: используется в {story_count} рассказах")
                
                # Проверяем "потерянные" связи
                missing_ids = set(tag_ids) - set(existing_tags.values_list('id', flat=True))
                if missing_ids:
                    print(f"\nВНИМАНИЕ! Найдены связи с несуществующими тегами: {missing_ids}")
                    
        except Exception as e:
            print(f"Ошибка при анализе stories_story_tags: {e}")
    
    # 3. Проверяем stories с тегами через ORM
    print("\n3. РАССКАЗЫ С ТЕГАМИ (через ORM):")
    print("-" * 40)
    
    stories_with_tags = Story.objects.filter(tags__isnull=False).distinct()
    print(f"Рассказов с тегами: {stories_with_tags.count()}")
    
    if stories_with_tags.exists():
        for story in stories_with_tags[:5]:  # Показываем первые 5
            tags = story.tags.all()
            tag_names = [tag.name for tag in tags]
            print(f"  - {story.title}: {', '.join(tag_names) if tag_names else 'нет тегов'}")
        
        if stories_with_tags.count() > 5:
            print(f"  ... и еще {stories_with_tags.count() - 5} рассказов")

def create_missing_tags():
    """Создаем недостающие теги из списка"""
    
    print("\n" + "=" * 70)
    print("СОЗДАНИЕ НЕДОСТАЮЩИХ ТЕГОВ")
    print("=" * 70)
    
    # Список тегов из вашего скриншота (те, которые должны быть)
    required_tags = [
        'алкоголь', 'бабушка', 'бандиты', 'внутренняя сила', 'ВОВ',
        'вразумление', 'врачебные истории', 'гонения', 'дедушка', 'дети',
        'доброе слово', 'дочь', 'жертвенность', 'животные', 'за пределами логики',
        'испытания', 'истории из жизни', 'исцеление', 'кротость', 'мама',
        'молитва', 'моя половинка', 'папа', 'покаяние (изменение)',
        'простая радость', 'семья', 'сильная личность', 'смирение',
        'сострадание', 'сын', 'христианская любовь', 'чудеса', 'школа'
    ]
    
    created_count = 0
    updated_count = 0
    
    for tag_name in required_tags:
        tag, created = CoreTag.objects.get_or_create(
            name=tag_name,
            defaults={
                'is_active': True,
                'description': f'Тег для видео-рассказов: {tag_name}',
                'color': '#74b9ff'  # Синий цвет по умолчанию
            }
        )
        
        if created:
            print(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")
            created_count += 1
        else:
            # Убеждаемся, что тег активен
            if not tag.is_active:
                tag.is_active = True
                tag.save()
                updated_count += 1
                print(f"🔄 Активирован тег: {tag.name}")
            else:
                print(f"✔️ Тег уже существует: {tag.name}")
    
    print(f"\nИТОГО:")
    print(f"  - Создано новых тегов: {created_count}")
    print(f"  - Активировано тегов: {updated_count}")
    print(f"  - Всего тегов в системе: {CoreTag.objects.count()}")

def sync_story_tags():
    """Синхронизируем теги у рассказов"""
    
    print("\n" + "=" * 70)
    print("СИНХРОНИЗАЦИЯ ТЕГОВ В РАССКАЗАХ")
    print("=" * 70)
    
    # Мапинг тегов к рассказам (примерный, можно дополнить)
    tag_mappings = {
        'молитва': ['молит', 'помолил', 'молебен'],
        'чудеса': ['чудо', 'чудес', 'необъяснимо'],
        'исцеление': ['исцел', 'выздоров', 'излечил'],
        'семья': ['семь', 'родител', 'родственник'],
        'дети': ['ребенок', 'ребёнок', 'дет', 'сын', 'дочь', 'дочк'],
        'мама': ['мам', 'матер', 'матушк'],
        'папа': ['отец', 'отц', 'папа', 'батюшк'],
        'вразумление': ['вразум', 'понял', 'осознал'],
        'покаяние (изменение)': ['покая', 'раская', 'изменил', 'простил'],
        'христианская любовь': ['любов', 'милосерд', 'сострадан'],
    }
    
    stories = Story.objects.all()
    
    for story in stories:
        added_tags = []
        
        # Анализируем заголовок и описание
        text_to_analyze = f"{story.title} {story.description}".lower()
        
        for tag_name, keywords in tag_mappings.items():
            for keyword in keywords:
                if keyword in text_to_analyze:
                    try:
                        tag = CoreTag.objects.get(name=tag_name)
                        if not story.tags.filter(id=tag.id).exists():
                            story.tags.add(tag)
                            added_tags.append(tag_name)
                    except CoreTag.DoesNotExist:
                        print(f"⚠️ Тег '{tag_name}' не найден!")
                    break
        
        if added_tags:
            print(f"📌 {story.title}: добавлены теги: {', '.join(added_tags)}")
    
    print("\n✅ Синхронизация завершена!")

def clean_broken_references():
    """Очищаем битые ссылки на теги"""
    
    print("\n" + "=" * 70)
    print("ОЧИСТКА БИТЫХ ССЫЛОК")
    print("=" * 70)
    
    with connection.cursor() as cursor:
        # Находим и удаляем битые ссылки
        cursor.execute("""
            DELETE FROM stories_story_tags 
            WHERE tag_id NOT IN (SELECT id FROM core_tag);
        """)
        
        deleted_count = cursor.rowcount
        
        if deleted_count > 0:
            print(f"🗑️ Удалено битых ссылок: {deleted_count}")
        else:
            print("✅ Битых ссылок не найдено")

if __name__ == '__main__':
    print("\n🚀 ЗАПУСК АНАЛИЗА И СИНХРОНИЗАЦИИ ТЕГОВ\n")
    
    # 1. Анализируем текущее состояние
    analyze_tags()
    
    # 2. Создаем недостающие теги
    create_missing_tags()
    
    # 3. Очищаем битые ссылки
    clean_broken_references()
    
    # 4. Синхронизируем теги (опционально)
    sync_choice = input("\nХотите автоматически присвоить теги рассказам? (y/n): ")
    if sync_choice.lower() == 'y':
        sync_story_tags()
    
    # 5. Финальный анализ
    print("\n" + "=" * 70)
    print("ФИНАЛЬНЫЙ АНАЛИЗ")
    print("=" * 70)
    analyze_tags()
    
    print("\n✨ ГОТОВО!")
