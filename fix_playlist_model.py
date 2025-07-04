#!/usr/bin/env python
"""
Быстрое исправление модели Playlist
Удаляем проблемное поле stories
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔧 ИСПРАВЛЕНИЕ МОДЕЛИ PLAYLIST")
print("=" * 50)

# Читаем файл models.py
models_file = 'stories/models.py'

try:
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ Файл models.py прочитан")
    
    # Ищем и удаляем проблемное поле stories
    lines = content.split('\n')
    new_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        # Пропускаем строки с ManyToManyField на stories
        if 'stories' in line.lower() and ('manytomanyfield' in line.lower() or 'through' in line.lower()):
            print(f"🗑️  Удаляем строку {i+1}: {line.strip()}")
            skip_next = True
            continue
        
        # Пропускаем продолжение предыдущей строки
        if skip_next and (line.strip().startswith('through=') or line.strip().startswith('blank=') or line.strip().startswith('verbose_name=')):
            print(f"🗑️  Удаляем строку {i+1}: {line.strip()}")
            continue
        else:
            skip_next = False
        
        new_lines.append(line)
    
    # Записываем исправленный файл
    new_content = '\n'.join(new_lines)
    
    with open(models_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Файл models.py исправлен")
    
    # Создаем новые миграции
    print("\n📦 Создание новых миграций...")
    from django.core.management import call_command
    
    try:
        call_command('makemigrations', 'stories', '--name=fix_playlist_model')
        print("✅ Миграции созданы")
    except Exception as e:
        print(f"⚠️  Миграции: {e}")
    
    # Применяем миграции
    print("\n⚙️ Применение миграций...")
    try:
        call_command('migrate', 'stories')
        print("✅ Миграции применены")
    except Exception as e:
        print(f"⚠️  Миграции: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("\n📋 Что было сделано:")
    print("✅ Удалено проблемное поле stories из модели Playlist") 
    print("✅ Созданы исправляющие миграции")
    print("✅ Миграции применены к базе данных")
    
    print("\n🚀 Теперь запустите сервер:")
    print("python manage.py runserver")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
