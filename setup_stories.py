#!/usr/bin/env python3
"""
Скрипт для настройки Stories приложения
"""

import os
import django
import sys

# Добавляем путь к проекту
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.db import transaction
from core.models import Category, Tag
from stories.models import Story


def create_test_data():
    """Создает тестовые данные для Stories"""
    print("📝 Создаем тестовые данные для Stories...")
    
    with transaction.atomic():
        # Создаем категории если их нет
        video_category, created = Category.objects.get_or_create(
            name="Видео-рассказы",
            defaults={
                'slug': 'video-stories',
                'description': 'Духовные видео-рассказы и поучения'
            }
        )
        if created:
            print(f"✅ Создана категория: {video_category.name}")
        
        orthodox_category, created = Category.objects.get_or_create(
            name="Православие",
            defaults={
                'slug': 'orthodoxy',
                'description': 'Православные темы и учения'
            }
        )
        if created:
            print(f"✅ Создана категория: {orthodox_category.name}")
        
        # Создаем теги если их нет
        tags_data = [
            ('духовность', 'spirituality', '#2B5AA0'),
            ('молитва', 'prayer', '#D4AF37'),
            ('семья', 'family', '#FF6B9D'),
            ('дети', 'children', '#4ADE80'),
            ('праздники', 'holidays', '#F59E0B'),
        ]
        
        for tag_name, tag_slug, tag_color in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={
                    'slug': tag_slug,
                    'color': tag_color
                }
            )
            if created:
                print(f"✅ Создан тег: {tag.name}")
        
        # Создаем тестовые рассказы
        test_stories = [
            {
                'title': 'О молитве и духовной жизни',
                'slug': 'o-molitve-i-duhovnoy-zhizni',
                'description': 'Рассказ о важности молитвы в повседневной жизни христианина.',
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'category': orthodox_category,
                'tags': ['духовность', 'молитва'],
                'is_featured': True,
            },
            {
                'title': 'Православная семья и воспитание детей',
                'slug': 'pravoslavnaya-semya-i-vospitanie-detey',
                'description': 'Размышления о том, как воспитывать детей в православной традиции.',
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'category': video_category,
                'tags': ['семья', 'дети'],
                'is_featured': False,
            },
            {
                'title': 'Пасха - Воскресение Христово',
                'slug': 'pasha-voskresenie-hristovo',
                'description': 'Рассказ о главном празднике православия - Светлом Христовом Воскресении.',
                'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'category': orthodox_category,
                'tags': ['праздники', 'духовность'],
                'is_featured': True,
            }
        ]
        
        for story_data in test_stories:
            # Извлекаем теги отдельно
            tag_names = story_data.pop('tags', [])
            
            # Создаем рассказ
            story, created = Story.objects.get_or_create(
                slug=story_data['slug'],
                defaults=story_data
            )
            
            if created:
                # Добавляем теги
                for tag_name in tag_names:
                    try:
                        tag = Tag.objects.get(name=tag_name)
                        story.tags.add(tag)
                    except Tag.DoesNotExist:
                        print(f"⚠️  Тег '{tag_name}' не найден")
                
                print(f"✅ Создан рассказ: {story.title}")
            else:
                print(f"📖 Рассказ уже существует: {story.title}")


def main():
    """Основная функция настройки"""
    print("🚀 Настройка Stories приложения...")
    
    try:
        # Применяем миграции
        print("📦 Применяем миграции...")
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Миграции применены")
        
        # Создаем тестовые данные
        create_test_data()
        
        print("\n🎉 Stories приложение успешно настроено!")
        print("📋 Что доступно в админке:")
        print("   • Рассказы (Stories) - управление видео-контентом")
        print("   • Лайки рассказов (Story Likes) - статистика лайков")
        print("\n🔗 Функции:")
        print("   • Автоматическое извлечение YouTube ID")
        print("   • Превью видео в админке")
        print("   • Система категорий и тегов")
        print("   • Счетчик просмотров")
        print("   • Система лайков")
        print("   • SEO-friendly URL")
        
    except Exception as e:
        print(f"❌ Ошибка при настройке: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    if success:
        print("\n✨ Теперь вы можете:")
        print("   1. Перейти в админку Django")
        print("   2. Найти раздел 'Stories'")
        print("   3. Добавить новые видео-рассказы")
        print("   4. Управлять категориями и тегами")
    else:
        print("\n❌ Настройка не завершена. Проверьте ошибки выше.")
