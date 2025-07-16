#!/usr/bin/env python
"""
Скрипт для исправления slug'ов с кириллицей
"""
import os
import sys
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from django.utils.text import slugify
import re

def transliterate_cyrillic(text):
    """Транслитерация кириллицы в латиницу"""
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    
    result = ""
    for char in text:
        if char in cyrillic_to_latin:
            result += cyrillic_to_latin[char]
        else:
            result += char
    
    return result

def create_safe_slug(title):
    """Создает безопасный slug из заголовка"""
    # Транслитерируем кириллицу
    transliterated = transliterate_cyrillic(title)
    
    # Создаем slug с помощью Django
    slug = slugify(transliterated)
    
    # Если slug пустой (только спецсимволы), используем ID
    if not slug:
        slug = f"story-{hash(title) % 100000}"
    
    return slug

def fix_story_slugs():
    """Исправляет проблемные slug'и"""
    print("🔧 Исправление slug'ов с кириллицей...")
    print()
    
    # Находим все истории с кириллическими slug'ами
    stories_with_cyrillic = []
    
    for story in Story.objects.all():
        # Проверяем, содержит ли slug кириллицу
        if re.search(r'[а-яё]', story.slug, re.IGNORECASE):
            stories_with_cyrillic.append(story)
    
    print(f"📊 Найдено историй с кириллическими slug'ами: {len(stories_with_cyrillic)}")
    
    if not stories_with_cyrillic:
        print("✅ Все slug'и корректны!")
        return
    
    fixed_count = 0
    
    for story in stories_with_cyrillic:
        old_slug = story.slug
        new_slug = create_safe_slug(story.title)
        
        # Проверяем уникальность
        counter = 1
        original_slug = new_slug
        while Story.objects.filter(slug=new_slug).exclude(id=story.id).exists():
            new_slug = f"{original_slug}-{counter}"
            counter += 1
        
        try:
            story.slug = new_slug
            story.save()
            fixed_count += 1
            print(f"✅ Исправлено: '{old_slug}' → '{new_slug}'")
        except Exception as e:
            print(f"❌ Ошибка при исправлении '{old_slug}': {e}")
    
    print()
    print(f"🎉 Исправлено slug'ов: {fixed_count}")
    print()
    print("🚀 Теперь можете проверить сайт:")
    print("   http://127.0.0.1:8000/stories/")

if __name__ == '__main__':
    fix_story_slugs()
