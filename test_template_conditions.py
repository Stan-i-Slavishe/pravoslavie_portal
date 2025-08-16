#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from django.template import Template, Context
from django.template.loader import render_to_string

try:
    # Получаем рассказ
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    
    print("=" * 70)
    print("🔍 ТЕСТИРОВАНИЕ ШАБЛОННЫХ УСЛОВИЙ")
    print("=" * 70)
    
    # Тестируем различные условия
    test_conditions = [
        "story.youtube_embed_id",
        "story.youtube_embed_id is not None",
        "story.youtube_embed_id != ''",
        "story.youtube_embed_id|length > 0",
        "story.youtube_url",
        "story.youtube_url is not None"
    ]
    
    for condition in test_conditions:
        template_code = f"""
        {{% load static %}}
        {{% if {condition} %}}
            УСЛОВИЕ ИСТИННО: {condition}
            YouTube ID: {{{{ story.youtube_embed_id }}}}
            Embed URL: https://www.youtube.com/embed/{{{{ story.youtube_embed_id }}}}
        {{% else %}}
            УСЛОВИЕ ЛОЖНО: {condition}
            YouTube ID: '{{{{ story.youtube_embed_id }}}}'
            Тип: {{{{ story.youtube_embed_id|default:"None" }}}}
        {{% endif %}}
        """
        
        try:
            template = Template(template_code)
            context = Context({'story': story})
            result = template.render(context)
            
            print(f"\n🧪 ТЕСТ: {condition}")
            print("-" * 50)
            print(result.strip())
            
        except Exception as e:
            print(f"\n❌ ОШИБКА в условии {condition}: {e}")
    
    print("\n" + "=" * 70)
    print("🎭 СИМУЛЯЦИЯ РЕАЛЬНОГО ШАБЛОНА")
    print("=" * 70)
    
    # Тестируем точную копию условия из шаблона
    video_template = """
    {% if story.youtube_embed_id %}
        <div class="embed-responsive embed-responsive-16by9">
            <iframe width="100%" 
                    src="https://www.youtube.com/embed/{{ story.youtube_embed_id }}" 
                    frameborder="0" 
                    allowfullscreen>
            </iframe>
        </div>
    {% else %}
        <div class="video-placeholder">
            <i class="bi bi-play-circle"></i>
            <p>Видео не найдено</p>
            <p>Debug: '{{ story.youtube_embed_id }}'</p>
            <p>Type: {{ story.youtube_embed_id|default:"None"|add:""|length }}</p>
        </div>
    {% endif %}
    """
    
    try:
        template = Template(video_template)
        context = Context({'story': story})
        result = template.render(context)
        
        print("HTML РЕЗУЛЬТАТ:")
        print("-" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ ОШИБКА рендеринга: {e}")
    
    print("\n" + "=" * 70)
    print("🔧 ПРОВЕРКА САМОГО ШАБЛОНА STORY_DETAIL.HTML")
    print("=" * 70)
    
    # Попробуем отрендерить настоящий шаблон
    try:
        from django.http import HttpRequest
        from django.contrib.auth.models import AnonymousUser
        
        # Создаем фиктивный request
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = 'GET'
        request.session = {}
        
        # Контекст как в enhanced_story_detail
        context = {
            'story': story,
            'related_stories': [],
            'recommendations': [],
            'user_playlists': [],
            'story_in_playlists': [],
            'story_in_watch_later': [],
            'story_in_favorites': [],
            'user_liked': False,
            'likes_count': 0,
            'comments': [],
            'comments_count': 0,
            'user_reactions': {},
            'previous_story': None,
            'next_story': None,
        }
        
        # Пытаемся отрендерить шаблон
        html = render_to_string('stories/story_detail.html', context, request)
        
        # Ищем секцию с видео в результате
        if 'video-container' in html:
            lines = html.split('\n')
            for i, line in enumerate(lines):
                if 'video-container' in line:
                    print(f"🎬 Найдена секция video-container на строке {i+1}")
                    # Показываем 10 строк вокруг
                    start = max(0, i-5)
                    end = min(len(lines), i+15)
                    for j in range(start, end):
                        marker = ">>> " if j == i else "    "
                        print(f"{marker}{j+1:3}: {lines[j].strip()}")
                    break
        else:
            print("❌ Секция video-container НЕ НАЙДЕНА в HTML")
            
        # Ищем iframe или video-placeholder
        if 'iframe' in html:
            print("✅ iframe НАЙДЕН в HTML")
        elif 'video-placeholder' in html:
            print("❌ Показывается video-placeholder")
        else:
            print("❓ Ни iframe, ни placeholder не найдены")
            
    except Exception as e:
        print(f"❌ ОШИБКА рендеринга шаблона: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ ОБЩАЯ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

input("\nНажмите Enter для выхода...")
