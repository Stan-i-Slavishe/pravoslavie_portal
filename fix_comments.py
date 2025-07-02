#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления подсчета комментариев в Django проекте
Запустите из корневой папки проекта: python fix_comments.py
"""

import os
import re
import shutil
from datetime import datetime

def print_header():
    print("=" * 50)
    print("🔧 ИСПРАВЛЕНИЕ СЧЕТЧИКА КОММЕНТАРИЕВ")
    print("=" * 50)
    print()

def check_django_project():
    """Проверяем, что мы в корне Django проекта"""
    if not os.path.exists('manage.py'):
        print("❌ ОШИБКА: Файл manage.py не найден!")
        print("Запустите этот скрипт из корневой папки Django проекта")
        return False
    print("✅ Django проект найден")
    return True

def create_backup(file_path):
    """Создаем резервную копию файла"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup"
        shutil.copy2(file_path, backup_path)
        print(f"   ✓ {file_path} → {backup_path}")
        return True
    return False

def fix_views_py():
    """Исправляем stories/views.py"""
    views_path = 'stories/views.py'
    
    if not os.path.exists(views_path):
        print(f"❌ Файл {views_path} не найден")
        return False
    
    print(f"🔨 Исправляем {views_path}...")
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Добавляем импорты если их нет
    if 'from django.db.models import Count, Q' not in content:
        content = re.sub(
            r'(from django.shortcuts import.*)', 
            r'\1\nfrom django.db.models import Count, Q', 
            content
        )
        print("   ✓ Добавлены импорты Count, Q")
    
    # Исправляем функцию story_detail
    new_story_detail = '''def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    
    # ИСПРАВЛЕНИЕ: Считаем только основные комментарии (без ответов)
    main_comments = Comment.objects.filter(
        story=story, 
        parent=None  # Только основные комментарии, не ответы
    ).select_related('user').prefetch_related('replies')
    
    # Количество основных комментариев (для консистентности)
    comments_count = main_comments.count()
    
    # Пагинация комментариев
    from django.core.paginator import Paginator
    paginator = Paginator(main_comments, 10)  # 10 комментариев на страницу
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    context = {
        'story': story,
        'comments': comments,
        'comments_count': comments_count,  # Передаем правильный счетчик
        'total_comments': comments_count,  # Для совместимости
    }'''
    
    # Заменяем функцию story_detail
    pattern = r'def story_detail\(request, slug\):.*?context = \{[^}]*\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_story_detail, content, flags=re.DOTALL)
        print("   ✓ Функция story_detail обновлена")
    else:
        print("   ⚠️ Функция story_detail не найдена для замены")
    
    # Исправляем функцию stories_list
    new_stories_list = '''def stories_list(request):
    stories = Story.objects.annotate(
        # ИСПРАВЛЕНИЕ: Аннотируем только основными комментариями
        comments_count=Count('comments', filter=Q(comments__parent=None))
    ).order_by('-created_at')
    
    context = {
        'stories': stories,
    }'''
    
    pattern = r'def stories_list\(request\):.*?context = \{[^}]*\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_stories_list, content, flags=re.DOTALL)
        print("   ✓ Функция stories_list обновлена")
    else:
        print("   ⚠️ Функция stories_list не найдена для замены")
    
    # Сохраняем файл
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {views_path} успешно обновлен")
    return True

def fix_template():
    """Исправляем шаблон story_detail.html"""
    template_path = 'templates/stories/story_detail.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Файл {template_path} не найден")
        return False
    
    print(f"🔨 Исправляем {template_path}...")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем hardcoded значения на переменные
    replacements = [
        ('data-count="24"', 'data-count="{{ comments_count }}"'),
        ('>24</span>', '>{{ comments_count }}</span>'),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"   ✓ Заменено: {old} → {new}")
    
    # Регулярные выражения для более сложных замен
    regex_replacements = [
        (r'id="comments-count-sidebar">24', 'id="comments-count-sidebar">{{ comments_count }}'),
        (r'id="comments-count-meta">24', 'id="comments-count-meta">{{ comments_count }}'),
    ]
    
    for pattern, replacement in regex_replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"   ✓ Заменено по паттерну: {pattern}")
    
    # Сохраняем файл
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {template_path} успешно обновлен")
    return True

def main():
    print_header()
    
    # Проверяем Django проект
    if not check_django_project():
        return
    
    print()
    
    # Создаем резервные копии
    print("📦 Создаем резервные копии файлов...")
    create_backup('stories/views.py')
    create_backup('templates/stories/story_detail.html')
    
    print()
    
    # Исправляем файлы
    views_ok = fix_views_py()
    template_ok = fix_template()
    
    print()
    print("=" * 50)
    
    if views_ok and template_ok:
        print("✅ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ УСПЕШНО!")
        print()
        print("📋 Что было сделано:")
        print("   • Созданы резервные копии (.backup)")
        print("   • Обновлен stories/views.py")
        print("   • Обновлен story_detail.html")
        print("   • Добавлены необходимые импорты")
        print("   • Исправлена логика подсчета комментариев")
        print()
        print("🚀 Теперь запустите сервер и проверьте:")
        print("   python manage.py runserver")
    else:
        print("❌ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ С ОШИБКАМИ!")
        print("💡 Проверьте структуру проекта и пути к файлам")
    
    print()
    print("💡 Если что-то пошло не так, восстановите из .backup файлов")
    print("=" * 50)

if __name__ == '__main__':
    main()