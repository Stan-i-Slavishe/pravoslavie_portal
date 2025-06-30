#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
✅ СКРИПТ ПРОВЕРКИ ЧИСТОТЫ ПРОЕКТА
Проверяет, что все файлы комментариев удалены
"""

import os
import glob

def check_cleanup():
    print("✅ ПРОВЕРКА ЧИСТОТЫ ПРОЕКТА ОТ КОММЕНТАРИЕВ")
    print("=" * 50)
    
    issues = []
    
    # 1. Проверка файлов в корне
    print("📁 Проверка корневой директории...")
    root_patterns = [
        '*comment*.py',
        '*comment*.bat',
        'diagnose_*.py', 
        'diagnose_*.bat',
        'fix_*.py',
        'fix_*.bat',
        'test_*.py',
        'test_*.bat',
        'emergency_*.py',
        'emergency_*.bat'
    ]
    
    for pattern in root_patterns:
        files = glob.glob(pattern)
        if files:
            for file in files:
                if file not in ['cleanup_db.py', 'cleanup_all_comments.bat', 'check_cleanup.py']:
                    issues.append(f"❌ Найден файл: {file}")
    
    # 2. Проверка директорий
    print("📂 Проверка директорий...")
    dirs_to_check = [
        'comments',
        'templates/stories/comments',
        'static/comments',
        'staticfiles/comments'
    ]
    
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            issues.append(f"❌ Найдена директория: {dir_path}")
    
    # 3. Проверка файлов в stories/
    print("📄 Проверка stories/...")
    stories_patterns = [
        'stories/comment_*.py',
        'stories/views_comments.py',
        'stories/*comment*.py'
    ]
    
    for pattern in stories_patterns:
        files = glob.glob(pattern)
        if files:
            for file in files:
                issues.append(f"❌ Найден файл: {file}")
    
    # 4. Проверка статических файлов
    print("🎨 Проверка статических файлов...")
    static_patterns = [
        'static/stories/js/*comment*.js',
        'static/stories/css/*comment*.css',
        'static/stories/js/youtube_*.js',
        'staticfiles/stories/js/*comment*.js',
        'staticfiles/stories/css/*comment*.css'
    ]
    
    for pattern in static_patterns:
        files = glob.glob(pattern)
        if files:
            for file in files:
                issues.append(f"❌ Найден файл: {file}")
    
    # 5. Проверка миграций
    print("🔄 Проверка миграций...")
    migration_patterns = [
        'stories/migrations/*comment*.py',
        'stories/migrations/*youtube*.py'
    ]
    
    for pattern in migration_patterns:
        files = glob.glob(pattern)
        if files:
            for file in files:
                issues.append(f"❌ Найдена миграция: {file}")
    
    # 6. Проверка шаблонов
    print("📝 Проверка шаблонов...")
    template_patterns = [
        'templates/stories/*comment*.html',
        'templates/stories/partials/*comment*.html',
        'templates/stories/partials/youtube_*.html'
    ]
    
    for pattern in template_patterns:
        files = glob.glob(pattern)
        if files:
            for file in files:
                issues.append(f"❌ Найден шаблон: {file}")
    
    # 7. Проверка stories/urls.py
    print("🔗 Проверка URLs...")
    if os.path.exists('stories/urls.py'):
        with open('stories/urls.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        problematic_terms = [
            'comment_views',
            'ajax/comment/',
            'ajax/reply/',
            'ajax/comments/',
            'simple/comment/'
        ]
        
        for term in problematic_terms:
            if term in content:
                issues.append(f"❌ В stories/urls.py найден: {term}")
    
    # 8. Проверка stories/models.py
    print("📊 Проверка моделей...")
    if os.path.exists('stories/models.py'):
        with open('stories/models.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        comment_models = [
            'class StoryComment',
            'class StoryCommentLike',
            'class CommentReport'
        ]
        
        for model in comment_models:
            if model in content:
                issues.append(f"❌ В stories/models.py найдена модель: {model}")
    
    # Результат проверки
    print("\n" + "=" * 50)
    print("📋 РЕЗУЛЬТАТ ПРОВЕРКИ:")
    print("=" * 50)
    
    if not issues:
        print("🎉 ОТЛИЧНО! Проект полностью очищен от комментариев!")
        print("✅ Все файлы и директории комментариев удалены")
        print("✅ URLs очищены")
        print("✅ Модели комментариев не найдены")
        print("\n🚀 Готово к созданию новой системы комментариев!")
        return True
    else:
        print("⚠️ НАЙДЕНЫ ОСТАТКИ КОММЕНТАРИЕВ:")
        for issue in issues:
            print(f"   {issue}")
        
        print(f"\n📊 Всего найдено проблем: {len(issues)}")
        print("\n🔧 НЕОБХОДИМО:")
        print("   • Удалить найденные файлы вручную")
        print("   • Или запустить cleanup_all_comments.bat еще раз")
        return False

if __name__ == "__main__":
    check_cleanup()
