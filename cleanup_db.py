#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🗃️ СКРИПТ ОЧИСТКИ БАЗЫ ДАННЫХ ОТ КОММЕНТАРИЕВ
Удаляет все таблицы и данные связанные с комментариями
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pravoslavie_portal.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def cleanup_database():
    """Очистка БД от таблиц комментариев"""
    print("🗃️ ОЧИСТКА БАЗЫ ДАННЫХ ОТ КОММЕНТАРИЕВ")
    print("=" * 50)
    
    cursor = connection.cursor()
    
    # Список таблиц для удаления
    tables_to_drop = [
        'stories_storycomment',
        'stories_storycommentlike', 
        'stories_commentreport',
        'comments_comment',
        'comments_commentlike',
    ]
    
    print("🗑️ Удаление таблиц комментариев...")
    
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"✅ Удалена таблица: {table}")
        except Exception as e:
            print(f"⚠️ Таблица {table}: {e}")
    
    print("\n🔧 Удаление записей из django_migrations...")
    try:
        # Удаляем записи о миграциях комментариев
        cursor.execute("""
            DELETE FROM django_migrations 
            WHERE name LIKE '%comment%' 
               OR name LIKE '%youtube%'
               OR app = 'comments';
        """)
        print("✅ Записи миграций комментариев удалены")
    except Exception as e:
        print(f"⚠️ Ошибка удаления миграций: {e}")
    
    cursor.close()
    
    print("\n🎉 Очистка БД завершена!")
    
def cleanup_migration_files():
    """Удаление файлов миграций комментариев"""
    print("\n📁 ОЧИСТКА ФАЙЛОВ МИГРАЦИЙ...")
    
    import glob
    
    # Ищем файлы миграций комментариев
    migration_patterns = [
        'stories/migrations/*comment*.py',
        'stories/migrations/*youtube*.py',
        'comments/migrations/*.py' if os.path.exists('comments/migrations') else None
    ]
    
    for pattern in migration_patterns:
        if pattern:
            for file_path in glob.glob(pattern):
                if '__init__.py' not in file_path:
                    try:
                        os.remove(file_path)
                        print(f"✅ Удален файл миграции: {file_path}")
                    except Exception as e:
                        print(f"⚠️ Ошибка удаления {file_path}: {e}")

def check_models_file():
    """Проверка и очистка models.py от комментариев"""
    print("\n📄 ПРОВЕРКА stories/models.py...")
    
    models_file = 'stories/models.py'
    
    if os.path.exists(models_file):
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем наличие моделей комментариев
        comment_models = [
            'class StoryComment',
            'class StoryCommentLike', 
            'class CommentReport'
        ]
        
        found_models = []
        for model in comment_models:
            if model in content:
                found_models.append(model)
        
        if found_models:
            print("⚠️ Найдены модели комментариев в stories/models.py:")
            for model in found_models:
                print(f"   • {model}")
            print("\n🔧 НЕОБХОДИМО ВРУЧНУЮ УДАЛИТЬ эти модели из stories/models.py")
        else:
            print("✅ Модели комментариев не найдены в stories/models.py")

def main():
    print("🧹 ПОЛНАЯ ОЧИСТКА КОММЕНТАРИЕВ ИЗ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    try:
        # 1. Очистка БД
        cleanup_database()
        
        # 2. Очистка файлов миграций
        cleanup_migration_files()
        
        # 3. Проверка models.py
        check_models_file()
        
        print("\n" + "=" * 60)
        print("🎉 ОЧИСТКА ЗАВЕРШЕНА!")
        print("=" * 60)
        print("\n🚀 СЛЕДУЮЩИЕ ШАГИ:")
        print("   1. Если были найдены модели в stories/models.py - удалите их вручную")
        print("   2. Создайте новые миграции: python manage.py makemigrations")
        print("   3. Примените миграции: python manage.py migrate")
        print("   4. Запустите сервер: python manage.py runserver")
        print("   5. Проверьте работу сайта")
        print("\n✅ Теперь можно создавать новую систему комментариев!")
        
    except Exception as e:
        print(f"\n💥 ОШИБКА: {e}")
        print("\n🔧 Попробуйте:")
        print("   • Убедитесь, что Django сервер остановлен")
        print("   • Проверьте настройки базы данных")
        print("   • Запустите: python manage.py shell")

if __name__ == "__main__":
    main()
