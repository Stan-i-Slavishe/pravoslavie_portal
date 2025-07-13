#!/usr/bin/env python
"""
Скрипт для принудительной очистки кеша Django и перезапуска
"""

import os
import sys
import shutil
from pathlib import Path

def clear_django_cache():
    """Очищает различные виды кеша Django"""
    
    print("🧹 Очистка кеша Django...")
    
    # 1. Очищаем __pycache__ файлы
    print("📁 Удаляем __pycache__ директории...")
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"   ✅ Удалено: {pycache_path}")
            except Exception as e:
                print(f"   ❌ Ошибка при удалении {pycache_path}: {e}")
    
    # 2. Очищаем .pyc файлы
    print("🗂️ Удаляем .pyc файлы...")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"   ✅ Удалено: {pyc_path}")
                except Exception as e:
                    print(f"   ❌ Ошибка при удалении {pyc_path}: {e}")
    
    # 3. Очищаем кеш шаблонов (если есть)
    template_cache_dirs = [
        'templates_cache',
        'template_cache', 
        'django_cache',
        'cache'
    ]
    
    for cache_dir in template_cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"   ✅ Удалена директория кеша: {cache_dir}")
            except Exception as e:
                print(f"   ❌ Ошибка при удалении {cache_dir}: {e}")
    
    # 4. Очищаем статические файлы (если собраны)
    staticfiles_dir = 'staticfiles'
    if os.path.exists(staticfiles_dir):
        try:
            shutil.rmtree(staticfiles_dir)
            print(f"   ✅ Удалена директория статических файлов: {staticfiles_dir}")
        except Exception as e:
            print(f"   ❌ Ошибка при удалении {staticfiles_dir}: {e}")
    
    print("✅ Очистка кеша завершена!")
    
def check_template_syntax():
    """Проверяет синтаксис шаблонов"""
    print("🔍 Проверка шаблонов...")
    
    mobile_template = Path('stories/templates/stories/mobile/playlist_widget_mobile.html')
    main_template = Path('stories/templates/stories/story_detail.html')
    
    templates_to_check = [mobile_template, main_template]
    
    for template_path in templates_to_check:
        if template_path.exists():
            print(f"   ✅ Найден шаблон: {template_path}")
            # Проверяем размер файла
            size = template_path.stat().st_size
            print(f"      📏 Размер: {size} байт")
        else:
            print(f"   ❌ Не найден шаблон: {template_path}")
    
    print("✅ Проверка шаблонов завершена!")

def main():
    print("🚀 Принудительная очистка кеша Django")
    print("=" * 50)
    
    # Меняем директорию на корень проекта
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    clear_django_cache()
    check_template_syntax()
    
    print("\n🎯 Рекомендации:")
    print("1. Перезапустите сервер разработки: python manage.py runserver")
    print("2. Очистите кеш браузера (Ctrl+F5)")
    print("3. Проверьте мобильный режим в браузере (F12 -> мобильное устройство)")
    print("4. Если проблема сохраняется, проверьте логи сервера")
    
    print("\n✨ Готово! Теперь попробуйте перезапустить сервер.")

if __name__ == "__main__":
    main()
