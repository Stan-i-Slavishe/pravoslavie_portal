#!/usr/bin/env python
"""
Проверка состояния миграций и таблиц плейлистов
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from django.core.management.base import CommandError
import io
from contextlib import redirect_stdout, redirect_stderr

def check_migrations():
    """Проверка состояния миграций"""
    print("📋 Проверка состояния миграций...")
    
    try:
        # Захватываем вывод команды showmigrations
        output = io.StringIO()
        error = io.StringIO()
        
        with redirect_stdout(output), redirect_stderr(error):
            call_command('showmigrations', 'stories')
        
        stdout_content = output.getvalue()
        stderr_content = error.getvalue()
        
        if stderr_content:
            print(f"⚠️  Ошибки: {stderr_content}")
        
        if stdout_content:
            print("📝 Состояние миграций stories:")
            print(stdout_content)
        
        # Проверяем неприменённые миграции
        if '[ ]' in stdout_content:
            print("⚠️  Есть неприменённые миграции!")
            unapplied = [line for line in stdout_content.split('\n') if '[ ]' in line]
            for migration in unapplied:
                print(f"   {migration}")
        else:
            print("✅ Все миграции применены")
            
    except CommandError as e:
        print(f"❌ Ошибка команды миграций: {e}")
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

def check_database_tables():
    """Проверка таблиц в базе данных"""
    print("\n🗄️  Проверка таблиц в базе данных...")
    
    try:
        cursor = connection.cursor()
        
        # Список всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Всего таблиц в БД: {len(all_tables)}")
        
        # Ищем таблицы плейлистов
        playlist_tables = [table for table in all_tables if 'playlist' in table.lower()]
        
        if playlist_tables:
            print("🎵 Таблицы плейлистов:")
            for table in playlist_tables:
                print(f"   ✅ {table}")
                
                # Проверяем структуру таблицы
                cursor.execute(f"PRAGMA table_info({table});")
                columns = cursor.fetchall()
                print(f"      Столбцов: {len(columns)}")
                
                # Проверяем количество записей
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"      Записей: {count}")
        else:
            print("❌ Таблицы плейлистов не найдены!")
        
        # Проверяем таблицы stories
        story_tables = [table for table in all_tables if 'stories' in table.lower()]
        
        if story_tables:
            print("\n📚 Таблицы рассказов:")
            for table in story_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} ({count} записей)")
        
    except Exception as e:
        print(f"❌ Ошибка проверки БД: {e}")
        import traceback
        traceback.print_exc()

def check_models_import():
    """Проверка импорта моделей"""
    print("\n🔧 Проверка импорта моделей...")
    
    try:
        from stories.models import Story
        print("✅ Story импортирован успешно")
        
        from stories.models import Playlist
        print("✅ Playlist импортирован успешно")
        
        from stories.models import PlaylistItem
        print("✅ PlaylistItem импортирован успешно")
        
        from stories.models import UserPlaylistPreference
        print("✅ UserPlaylistPreference импортирован успешно")
        
        # Проверяем создание запросов
        try:
            stories_count = Story.objects.count()
            print(f"📊 Рассказов в БД: {stories_count}")
        except Exception as e:
            print(f"❌ Ошибка запроса Story: {e}")
        
        try:
            playlists_count = Playlist.objects.count()
            print(f"📊 Плейлистов в БД: {playlists_count}")
        except Exception as e:
            print(f"❌ Ошибка запроса Playlist: {e}")
        
        try:
            items_count = PlaylistItem.objects.count()
            print(f"📊 Элементов плейлистов в БД: {items_count}")
        except Exception as e:
            print(f"❌ Ошибка запроса PlaylistItem: {e}")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

def main():
    """Основная функция"""
    print("🔍 Диагностика плейлистов")
    print("=" * 50)
    
    check_migrations()
    check_database_tables()
    check_models_import()
    
    print("\n" + "=" * 50)
    print("✨ Диагностика завершена")

if __name__ == "__main__":
    main()
