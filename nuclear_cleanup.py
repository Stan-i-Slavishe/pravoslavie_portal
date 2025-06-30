#!/usr/bin/env python3
"""
ОКОНЧАТЕЛЬНОЕ РЕШЕНИЕ ПРОБЛЕМЫ КОММЕНТАРИЕВ
Полное удаление всех проблемных файлов и создание простейшей системы
"""

import os
import shutil
import sys

def delete_file_safely(file_path):
    """Безопасное удаление файла"""
    try:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"✅ Удален файл: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"✅ Удалена папка: {file_path}")
            return True
    except Exception as e:
        print(f"❌ Ошибка при удалении {file_path}: {e}")
        return False

def main():
    base_path = r'E:\pravoslavie_portal'
    
    print("🚨 РАДИКАЛЬНАЯ ОЧИСТКА СИСТЕМЫ КОММЕНТАРИЕВ")
    print("=" * 60)
    
    # Список ВСЕХ файлов для удаления
    files_to_delete = [
        # JavaScript файлы (ALL)
        'static/js/youtube_comments_fixed.js',
        'static/js/youtube_comments.js', 
        'static/js/comments_debug.js',
        'static/stories/js/youtube_comments.js',
        
        # Staticfiles (кеш)
        'staticfiles',
        
        # Старые шаблоны комментариев
        'stories/templates/stories/partials',
        'stories/templates/stories/comments',
        
        # Python файлы
        'stories/views_comments.py',
        'stories/test_comments_views.py',
        'stories/test_clean_views.py',
        
        # Документация и тесты
        'test_youtube_comments.py',
        'YOUTUBE_COMMENTS_INTEGRATION.md',
        'cleanup_comments.py',
        'clear_cache.py',
        
        # Bat файлы
        'launch_youtube_comments_final.bat',
        'run_youtube_comments.bat',
        
        # Старые шаблоны
        'stories/templates/stories/story_detail.html',
        'stories/templates/stories/story_detail_fixed.html',
        'stories/templates/stories/story_test_comments.html',
        'stories/templates/stories/comments_test.html',
        'test_comments_clean.html',
    ]
    
    print("1️⃣ Удаление проблемных файлов...")
    deleted_count = 0
    
    for file_path in files_to_delete:
        full_path = os.path.join(base_path, file_path)
        if delete_file_safely(full_path):
            deleted_count += 1
    
    print(f"\n✅ Удалено {deleted_count} файлов/папок")
    
    print("\n2️⃣ Очистка __pycache__ и .pyc файлов...")
    
    # Очистка Python кеша
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs[:]:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                delete_file_safely(pycache_path)
                dirs.remove(dir_name)
        
        for file_name in files:
            if file_name.endswith('.pyc'):
                pyc_path = os.path.join(root, file_name)
                delete_file_safely(pyc_path)
    
    print("\n🎉 ОЧИСТКА ЗАВЕРШЕНА!")
    print("=" * 60)
    print("✅ Все проблемные файлы удалены")
    print("✅ Кеш очищен") 
    print("✅ Система готова к новой реализации")
    print("\n🚀 Теперь запустите create_simple_comments.py")

if __name__ == "__main__":
    main()
