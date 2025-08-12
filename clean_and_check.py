#!/usr/bin/env python
"""
Скрипт для очистки кеша Python и диагностики проблем
"""
import os
import shutil
import sys

def clean_python_cache():
    """Очистка __pycache__ директорий"""
    print("🧹 Очистка Python кеша...")
    
    project_root = r'E:\pravoslavie_portal'
    cleaned_count = 0
    
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_path)
                print(f"   ✅ Удален: {cache_path}")
                cleaned_count += 1
            except Exception as e:
                print(f"   ❌ Ошибка при удалении {cache_path}: {e}")
        
        # Удаляем .pyc файлы
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"   ✅ Удален .pyc: {pyc_path}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"   ❌ Ошибка при удалении {pyc_path}: {e}")
    
    print(f"🎉 Очистка завершена! Удалено элементов: {cleaned_count}")

def check_structure():
    """Проверка структуры файлов"""
    print("\n📁 Проверка структуры файлов...")
    
    important_files = [
        'core/views/__init__.py',
        'core/views/main_views.py', 
        'core/views/seo_views.py',
        'core/seo/__init__.py',
        'core/seo/meta_tags.py',
        'core/models.py',
        'core/forms.py',
        'core/urls.py',
    ]
    
    for file_path in important_files:
        full_path = os.path.join(r'E:\pravoslavie_portal', file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - НЕ НАЙДЕН!")

if __name__ == '__main__':
    clean_python_cache()
    check_structure()
    print("\n🚀 Теперь можно запускать сервер!")
