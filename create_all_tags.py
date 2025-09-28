"""
Скрипт для создания всех необходимых тегов в системе
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

def main():
    print("\n" + "=" * 70)
    print("СОЗДАНИЕ И СИНХРОНИЗАЦИЯ ТЕГОВ")
    print("=" * 70)
    
    # Полный список тегов для видео-рассказов
    required_tags = [
        ('алкоголь', '#e74c3c'),
        ('бабушка', '#9b59b6'),
        ('бандиты', '#2c3e50'),
        ('внутренняя сила', '#f39c12'),
        ('ВОВ', '#c0392b'),
        ('вразумление', '#3498db'),
        ('врачебные истории', '#16a085'),
        ('гонения', '#d35400'),
        ('дедушка', '#8e44ad'),
        ('дети', '#e91e63'),
        ('доброе слово', '#27ae60'),
        ('дочь', '#ff6b9d'),
        ('жертвенность', '#00b894'),
        ('животные', '#fdcb6e'),
        ('за пределами логики', '#6c5ce7'),
        ('испытания', '#e17055'),
        ('истории из жизни', '#74b9ff'),
        ('исцеление', '#a29bfe'),
        ('кротость', '#00cec9'),
        ('мама', '#fd79a8'),
        ('молитва', '#74b9ff'),
        ('моя половинка', '#ff7675'),
        ('папа', '#0984e3'),
        ('покаяние (изменение)', '#00b894'),
        ('простая радость', '#ffeaa7'),
        ('семья', '#fab1a0'),
        ('сильная личность', '#e17055'),
        ('смирение', '#81ecec'),
        ('сострадание', '#55efc4'),
        ('сын', '#6c5ce7'),
        ('христианская любовь', '#ff6348'),
        ('чудеса', '#a29bfe'),
        ('школа', '#fdcb6e')
    ]
    
    created_count = 0
    updated_count = 0
    
    print("\nСоздание/обновление тегов:")
    print("-" * 40)
    
    for tag_name, color in required_tags:
        tag, created = CoreTag.objects.get_or_create(
            name=tag_name,
            defaults={
                'is_active': True,
                'description': f'Тег для видео-рассказов',
                'color': color
            }
        )
        
        if created:
            print(f"✅ Создан тег: {tag.name} (цвет: {color})")
            created_count += 1
        else:
            # Обновляем цвет и активность существующего тега
            changed = False
            if tag.color != color:
                tag.color = color
                changed = True
            if not tag.is_active:
                tag.is_active = True
                changed = True
            
            if changed:
                tag.save()
                updated_count += 1
                print(f"🔄 Обновлен тег: {tag.name} (цвет: {color})")
            else:
                print(f"✔️ Тег уже существует: {tag.name}")
    
    # Очистка битых ссылок
    print("\n" + "-" * 40)
    print("Очистка битых ссылок...")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM stories_story_tags 
            WHERE tag_id NOT IN (SELECT id FROM core_tag);
        """)
        deleted_count = cursor.rowcount
        
        if deleted_count > 0:
            print(f"🗑️ Удалено битых ссылок: {deleted_count}")
        else:
            print("✅ Битых ссылок не найдено")
    
    # Проверка результатов
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ:")
    print("-" * 40)
    print(f"✅ Создано новых тегов: {created_count}")
    print(f"🔄 Обновлено тегов: {updated_count}")
    print(f"📊 Всего тегов в системе: {CoreTag.objects.count()}")
    print(f"✨ Активных тегов: {CoreTag.objects.filter(is_active=True).count()}")
    
    # Проверяем связи с рассказами
    stories_with_tags = Story.objects.filter(tags__isnull=False).distinct().count()
    print(f"📚 Рассказов с тегами: {stories_with_tags}")
    
    print("\n✅ ГОТОВО! Теги успешно синхронизированы.")
    print("Теперь они должны отображаться в разделе /tags/")
    
if __name__ == '__main__':
    main()
