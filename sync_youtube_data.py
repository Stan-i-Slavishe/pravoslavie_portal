#!/usr/bin/env python3
"""
Синхронизация YouTube данных в рассказах
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
import re

def extract_youtube_id(url):
    """Извлекает YouTube ID из различных форматов URL"""
    if not url:
        return ''
        
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\n?#]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&\n?#]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([^&\n?#]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ''

def sync_youtube_data():
    """Синхронизируем YouTube данные"""
    
    print("🔄 Синхронизация YouTube данных")
    print("=" * 50)
    
    stories = Story.objects.all()
    updated_count = 0
    
    for story in stories:
        original_id = story.youtube_embed_id
        
        # Извлекаем ID из URL, если ID пустой или отличается
        if story.youtube_url and not story.youtube_embed_id:
            extracted_id = extract_youtube_id(story.youtube_url)
            if extracted_id:
                story.youtube_embed_id = extracted_id
                story.save(update_fields=['youtube_embed_id'])
                updated_count += 1
                print(f"✅ Обновлен {story.title}: ID = {extracted_id}")
            else:
                print(f"❌ Не удалось извлечь ID из {story.youtube_url}")
        elif story.youtube_embed_id:
            print(f"ℹ️  {story.title}: ID уже есть = {story.youtube_embed_id}")
        else:
            print(f"⚠️  {story.title}: Нет YouTube URL")
    
    print(f"\n📊 Результат:")
    print(f"   Обновлено записей: {updated_count}")
    
    # Проверяем конкретный рассказ
    print(f"\n🔍 Проверка проблемного рассказа:")
    try:
        story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
        print(f"   Название: {story.title}")
        print(f"   YouTube URL: {story.youtube_url}")
        print(f"   YouTube ID: {story.youtube_embed_id}")
        
        if story.youtube_url and not story.youtube_embed_id:
            extracted_id = extract_youtube_id(story.youtube_url)
            if extracted_id:
                story.youtube_embed_id = extracted_id
                story.save(update_fields=['youtube_embed_id'])
                print(f"   ✅ Исправлено! Новый ID: {extracted_id}")
            else:
                print(f"   ❌ Не удалось извлечь ID из URL")
        elif story.youtube_embed_id:
            print(f"   ✅ ID уже корректный: {story.youtube_embed_id}")
        else:
            print(f"   ❌ Нет YouTube данных")
            
    except Story.DoesNotExist:
        print(f"   ❌ Рассказ не найден!")

if __name__ == "__main__":
    try:
        sync_youtube_data()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
