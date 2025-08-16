#!/usr/bin/env python3
"""
Быстрое исправление проблемы с отображением YouTube видео
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def main():
    print("🔧 Диагностика и исправление проблемы с YouTube видео")
    print("=" * 60)
    
    # Ищем проблемный рассказ
    try:
        story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
        print(f"✅ Найден рассказ: {story.title}")
        
        print(f"\n📊 Текущие данные:")
        print(f"   YouTube URL: '{story.youtube_url}'")
        print(f"   YouTube ID: '{story.youtube_embed_id}'")
        print(f"   Опубликован: {story.is_published}")
        
        # Проверяем, есть ли YouTube ID
        if not story.youtube_embed_id and story.youtube_url:
            print(f"\n🔄 YouTube ID пустой, но URL есть. Извлекаем ID...")
            
            import re
            patterns = [
                r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\n?#]+)',
                r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&\n?#]+)',
                r'(?:https?://)?(?:www\.)?youtu\.be/([^&\n?#]+)',
            ]
            
            youtube_id = None
            for pattern in patterns:
                match = re.search(pattern, story.youtube_url)
                if match:
                    youtube_id = match.group(1)
                    break
            
            if youtube_id:
                story.youtube_embed_id = youtube_id
                story.save(update_fields=['youtube_embed_id'])
                print(f"   ✅ ID извлечен и сохранен: {youtube_id}")
            else:
                print(f"   ❌ Не удалось извлечь ID из URL")
        
        elif story.youtube_embed_id:
            print(f"\n✅ YouTube ID уже есть: {story.youtube_embed_id}")
        
        else:
            print(f"\n❌ Нет ни URL, ни ID!")
            print(f"   Нужно добавить YouTube ссылку в админке")
            return False
        
        # Проверяем итоговое состояние
        story.refresh_from_db()
        print(f"\n🎬 Итоговое состояние:")
        print(f"   YouTube ID: '{story.youtube_embed_id}'")
        
        if story.youtube_embed_id:
            embed_url = f"https://www.youtube.com/embed/{story.youtube_embed_id}"
            print(f"   Embed URL: {embed_url}")
            print(f"   ✅ Видео должно отображаться корректно!")
            
            # Тестируем условие шаблона
            if story.youtube_embed_id:
                print(f"   ✅ Условие {{% if story.youtube_embed_id %}} = True")
            else:
                print(f"   ❌ Условие {{% if story.youtube_embed_id %}} = False")
                
            return True
        else:
            print(f"   ❌ ID по-прежнему пустой")
            return False
            
    except Story.DoesNotExist:
        print(f"❌ Рассказ с slug 'kak-svyatoj-luka-doch-spas' не найден!")
        
        # Показываем все существующие рассказы
        print(f"\n📋 Доступные рассказы:")
        stories = Story.objects.all()[:10]
        for story in stories:
            print(f"   - {story.slug} ({story.title})")
        
        return False
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎉 Проблема исправлена! Теперь видео должно отображаться.")
            print(f"📍 Откройте: http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/")
        else:
            print(f"\n⚠️  Требуется дополнительная настройка через админку.")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
