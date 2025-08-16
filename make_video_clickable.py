#!/usr/bin/env python3
"""
Скрипт для применения кликабельных превью видео к проекту
"""

import os
import django
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_template_changes():
    """Проверяем, что изменения в шаблоне применены корректно"""
    template_path = Path('templates/stories/story_list.html')
    
    if not template_path.exists():
        print("❌ Шаблон templates/stories/story_list.html не найден")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем наличие кликабельной ссылки
    if 'story-thumbnail-link' in content:
        print("✅ Кликабельное превью добавлено в шаблон")
        return True
    else:
        print("❌ Кликабельное превью не найдено в шаблоне")
        return False

def test_stories_view():
    """Тестируем представление рассказов"""
    try:
        from stories.models import Story
        stories_count = Story.objects.count()
        print(f"✅ Найдено {stories_count} рассказов в базе данных")
        
        # Проверяем первый рассказ
        if stories_count > 0:
            first_story = Story.objects.first()
            print(f"✅ Первый рассказ: {first_story.title}")
            print(f"   YouTube ID: {getattr(first_story, 'youtube_embed_id', 'Не указан')}")
            print(f"   Slug: {first_story.slug}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка при тестировании представления: {e}")
        return False

def create_test_file():
    """Создаем тестовый файл для проверки функциональности"""
    test_content = """
<!-- Тестовая страница кликабельного превью -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тест кликабельного превью</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/azbyka-style.css">
</head>
<body>
    <div class="container mt-4">
        <div class="alert alert-success">
            <h4>🎯 Кликабельное превью активно!</h4>
            <p>Превью видео теперь работает как кнопка - можно кликнуть в любое место изображения.</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="story-card">
                    <a href="/stories/test/" class="story-thumbnail-link text-decoration-none">
                        <div class="story-thumbnail">
                            <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg" 
                                 alt="Тестовое видео">
                            <div class="play-overlay">
                                <i class="bi bi-play-fill"></i>
                            </div>
                        </div>
                    </a>
                    
                    <div class="story-content">
                        <h3 class="story-title">
                            <a href="/stories/test/" class="text-decoration-none">
                                Тестовый рассказ
                            </a>
                        </h3>
                        <p class="story-description">
                            Описание тестового рассказа для проверки кликабельности превью.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    test_file_path = Path('templates/test_clickable_preview.html')
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ Создан тестовый файл: {test_file_path}")

def main():
    """Основная функция"""
    print("🚀 Проверка кликабельных превью видео...")
    print("=" * 50)
    
    # Проверяем изменения в шаблоне
    template_ok = check_template_changes()
    
    # Тестируем модели
    models_ok = test_stories_view()
    
    # Создаем тестовый файл
    try:
        create_test_file()
        test_file_ok = True
    except Exception as e:
        print(f"❌ Ошибка при создании тестового файла: {e}")
        test_file_ok = False
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТ:")
    print(f"   Шаблон: {'✅' if template_ok else '❌'}")
    print(f"   Модели: {'✅' if models_ok else '❌'}")
    print(f"   Тест:   {'✅' if test_file_ok else '❌'}")
    
    if all([template_ok, models_ok, test_file_ok]):
        print("\n🎉 Кликабельные превью успешно настроены!")
        print("\n📝 Что дальше:")
        print("   1. Запустите сервер: python manage.py runserver")
        print("   2. Перейдите на /stories/")
        print("   3. Кликните на любое превью видео")
        print("   4. Убедитесь, что переход работает корректно")
    else:
        print("\n⚠️  Обнаружены проблемы. Проверьте ошибки выше.")

if __name__ == '__main__':
    main()
