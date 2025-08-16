#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для исправления ошибок в детальной странице рассказов
Исправляет:
1. TemplateSyntaxError с неправильным endblock
2. AttributeError с youtube_embed поля в модели Story
3. Проблемы с отображением видео
"""

import os
import sys
import django
import re
from pathlib import Path

# Добавляем путь к проекту
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from django.core.management import call_command

def extract_youtube_id(url):
    """Извлекает ID видео из YouTube URL"""
    if not url:
        return None
    
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def fix_story_youtube_ids():
    """Исправляет YouTube ID для всех рассказов"""
    print("🔧 Исправляем YouTube ID для рассказов...")
    
    stories = Story.objects.all()
    fixed_count = 0
    
    for story in stories:
        if story.youtube_url and not story.youtube_embed_id:
            youtube_id = extract_youtube_id(story.youtube_url)
            if youtube_id:
                story.youtube_embed_id = youtube_id
                story.save(update_fields=['youtube_embed_id'])
                print(f"✅ Исправлен ID для '{story.title}': {youtube_id}")
                fixed_count += 1
            else:
                print(f"❌ Не удалось извлечь ID из URL: {story.youtube_url}")
    
    print(f"🎉 Исправлено {fixed_count} рассказов")

def backup_original_template():
    """Создает резервную копию оригинального шаблона"""
    original_path = project_root / 'templates' / 'stories' / 'story_detail.html'
    backup_path = project_root / 'templates' / 'stories' / 'story_detail_backup.html'
    
    if original_path.exists() and not backup_path.exists():
        with open(original_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Создана резервная копия: {backup_path}")
    else:
        print("⚠️  Резервная копия уже существует или оригинал не найден")

def replace_template():
    """Заменяет проблемный шаблон на исправленный"""
    original_path = project_root / 'templates' / 'stories' / 'story_detail.html'
    fixed_path = project_root / 'templates' / 'stories' / 'story_detail_fixed.html'
    
    if fixed_path.exists():
        # Создаем резервную копию
        backup_original_template()
        
        # Читаем исправленный шаблон
        with open(fixed_path, 'r', encoding='utf-8') as f:
            fixed_content = f.read()
        
        # Записываем в оригинальный файл
        with open(original_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Шаблон заменен: {original_path}")
        print("🔄 Перезапустите сервер для применения изменений")
    else:
        print(f"❌ Исправленный шаблон не найден: {fixed_path}")

def check_story_model():
    """Проверяет наличие нужных полей в модели Story"""
    print("🔍 Проверяем модель Story...")
    
    # Проверяем первый рассказ
    story = Story.objects.first()
    if story:
        fields_to_check = [
            'youtube_url', 'youtube_embed_id', 'title', 'slug', 
            'description', 'created_at', 'views_count'
        ]
        
        missing_fields = []
        for field in fields_to_check:
            if not hasattr(story, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Отсутствуют поля: {', '.join(missing_fields)}")
            print("🔧 Необходимо выполнить миграции")
            return False
        else:
            print("✅ Все необходимые поля присутствуют")
            return True
    else:
        print("⚠️  Рассказы не найдены в базе данных")
        return True

def create_test_story():
    """Создает тестовый рассказ для проверки"""
    print("🧪 Создаем тестовый рассказ...")
    
    test_story, created = Story.objects.get_or_create(
        slug='test-story-fix',
        defaults={
            'title': 'Тестовый рассказ (исправление)',
            'description': 'Этот рассказ создан для тестирования исправлений. Можно удалить после проверки.',
            'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Rick Roll для теста
            'youtube_embed_id': 'dQw4w9WgXcQ',
            'views_count': 0,
        }
    )
    
    if created:
        print(f"✅ Создан тестовый рассказ: {test_story.title}")
        print(f"🔗 URL: /stories/{test_story.slug}/")
    else:
        print("📝 Тестовый рассказ уже существует")
    
    return test_story

def main():
    """Основная функция исправления"""
    print("🚀 Запуск исправления ошибок рассказов")
    print("=" * 50)
    
    try:
        # 1. Проверяем модель
        if not check_story_model():
            print("❌ Проблемы с моделью. Выполните миграции и повторите")
            return
        
        # 2. Исправляем YouTube ID
        fix_story_youtube_ids()
        
        # 3. Заменяем шаблон
        replace_template()
        
        # 4. Создаем тестовый рассказ
        test_story = create_test_story()
        
        print("\n" + "=" * 50)
        print("🎉 ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ!")
        print("\n📋 Что было сделано:")
        print("   ✅ Исправлены YouTube ID для рассказов")
        print("   ✅ Заменен проблемный шаблон story_detail.html")
        print("   ✅ Создан тестовый рассказ для проверки")
        
        print(f"\n🧪 Протестируйте:")
        print(f"   1. Перезапустите сервер Django")
        print(f"   2. Откройте: http://127.0.0.1:8000/stories/{test_story.slug}/")
        print(f"   3. Проверьте отображение видео и отсутствие ошибок")
        
        print("\n⚠️  Если проблемы остались:")
        print("   1. Проверьте логи сервера")
        print("   2. Убедитесь что все миграции применены")
        print("   3. Проверьте настройки URL в stories/urls.py")
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении: {e}")
        print("📋 Попробуйте:")
        print("   1. Убедитесь что Django настроен правильно")
        print("   2. Проверьте подключение к базе данных")
        print("   3. Выполните: python manage.py migrate")

if __name__ == '__main__':
    main()
