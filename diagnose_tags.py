#!/usr/bin/env python3
"""
Скрипт для проверки тегов в базе данных и исправления ошибки
"""
import os
import sys
import django

# Настройка Django
sys.path.append('E:\\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    
    from core.models import Tag
    from stories.models import Story
    
    print("🔍 ДИАГНОСТИКА СИСТЕМЫ ТЕГОВ")
    print("=" * 50)
    
    # 1. Проверяем все теги
    all_tags = Tag.objects.all()
    print(f"📊 Всего тегов в базе: {all_tags.count()}")
    
    if all_tags.count() > 0:
        print("\n📋 Список всех тегов:")
        for tag in all_tags[:10]:  # Показываем первые 10
            print(f"   • {tag.name} (slug: {tag.slug})")
            
        # 2. Проверяем конкретный тег "doch"
        print(f"\n🔍 Поиск тега со slug 'doch':")
        try:
            doch_tag = Tag.objects.get(slug='doch')
            print(f"   ✅ Найден: {doch_tag.name}")
        except Tag.DoesNotExist:
            print("   ❌ Тег со slug 'doch' не найден!")
            
            # Ищем похожие теги
            similar_tags = Tag.objects.filter(name__icontains='дочь')
            if similar_tags.exists():
                print("   🔍 Найдены похожие теги:")
                for tag in similar_tags:
                    print(f"      • {tag.name} (slug: {tag.slug})")
            
            # Создаем тег "дочь" если его нет
            print("\n🛠️ Создаем тег 'дочь'...")
            new_tag = Tag.objects.create(
                name='дочь',
                slug='doch',
                description='Материалы о воспитании дочерей и отношениях с ними',
                color='#FF6B9D',
                is_active=True
            )
            print(f"   ✅ Создан тег: {new_tag.name} (slug: {new_tag.slug})")
    else:
        print("\n⚠️ В базе нет тегов! Создаем базовые теги...")
        
        # Создаем базовые теги
        basic_tags = [
            {'name': 'дочь', 'slug': 'doch', 'description': 'Материалы о воспитании дочерей', 'color': '#FF6B9D'},
            {'name': 'сын', 'slug': 'syn', 'description': 'Материалы о воспитании сыновей', 'color': '#2196F3'},
            {'name': 'семья', 'slug': 'semya', 'description': 'Материалы о семейных ценностях', 'color': '#4CAF50'},
            {'name': 'вера', 'slug': 'vera', 'description': 'Материалы о вере и духовности', 'color': '#9C27B0'},
            {'name': 'любовь', 'slug': 'lyubov', 'description': 'Материалы о любви', 'color': '#E91E63'},
        ]
        
        for tag_data in basic_tags:
            tag = Tag.objects.create(**tag_data, is_active=True)
            print(f"   ✅ Создан: {tag.name} (slug: {tag.slug})")
    
    # 3. Проверяем связи тегов с рассказами
    print(f"\n🔗 Проверка связей тегов с рассказами:")
    stories_with_tags = Story.objects.filter(tags__isnull=False).distinct().count()
    total_stories = Story.objects.count()
    print(f"   📊 Рассказов с тегами: {stories_with_tags} из {total_stories}")
    
    # 4. Если есть рассказы без тегов, добавляем им теги
    if total_stories > 0 and stories_with_tags < total_stories:
        print(f"\n🏷️ Добавляем теги к рассказам без тегов...")
        
        # Получаем теги
        family_tag = Tag.objects.get(slug='semya')
        faith_tag = Tag.objects.get(slug='vera')
        
        stories_without_tags = Story.objects.filter(tags__isnull=True)[:5]
        for i, story in enumerate(stories_without_tags):
            # Добавляем случайные теги
            if i % 2 == 0:
                story.tags.add(family_tag)
                print(f"   ✅ К рассказу '{story.title}' добавлен тег 'семья'")
            else:
                story.tags.add(faith_tag)
                print(f"   ✅ К рассказу '{story.title}' добавлен тег 'вера'")
    
    print("\n" + "=" * 50)
    print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА!")
    print("\n🧪 Попробуйте теперь:")
    print("   http://127.0.0.1:8000/tag/doch/")
    print("   http://127.0.0.1:8000/tag/vera/")
    print("   http://127.0.0.1:8000/tag/semya/")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
