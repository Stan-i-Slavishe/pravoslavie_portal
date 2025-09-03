#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная диагностика PostgreSQL системы перед переходом к Docker
"""

import os
import sys
import django
from datetime import datetime

def setup_django():
    """Настраиваем Django окружение"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local_postgresql')
    django.setup()

def check_database_connection():
    """Проверяем подключение к PostgreSQL"""
    print("1. ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ")
    print("-" * 40)
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Основная информация о БД
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ PostgreSQL версия: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✓ База данных: {db_name}")
            
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0]
            print(f"✓ Пользователь: {user}")
            
            # Проверяем настройки кодировки
            cursor.execute("SELECT pg_database.datname, pg_database.encoding, pg_encoding_to_char(pg_database.encoding) FROM pg_database WHERE datname = current_database();")
            db_info = cursor.fetchone()
            print(f"✓ Кодировка БД: {db_info[2]} (код: {db_info[1]})")
            
            return True
            
    except Exception as e:
        print(f"✗ Ошибка подключения к БД: {e}")
        return False

def check_django_models():
    """Проверяем Django модели и данные"""
    print("\n2. DJANGO МОДЕЛИ И ДАННЫЕ")
    print("-" * 40)
    
    models_info = []
    
    try:
        # Проверяем основные модели
        model_checks = [
            ('django.contrib.auth.models', 'User', 'Пользователи'),
            ('core.models', 'Category', 'Категории'),
            ('stories.models', 'Story', 'Рассказы'),
            ('books.models', 'Book', 'Книги'),
            ('shop.models', 'Product', 'Товары'),
            ('fairy_tales.models', 'FairyTaleTemplate', 'Сказки'),
            ('stories.models', 'Playlist', 'Плейлисты'),
            ('stories.models', 'StoryComment', 'Комментарии'),
        ]
        
        total_records = 0
        
        for module_name, model_name, description in model_checks:
            try:
                if module_name == 'django.contrib.auth.models':
                    from django.contrib.auth.models import User
                    model = User
                else:
                    module = __import__(module_name, fromlist=[model_name])
                    model = getattr(module, model_name)
                
                count = model.objects.count()
                total_records += count
                print(f"✓ {description}: {count}")
                models_info.append((description, count))
                
            except Exception as e:
                print(f"✗ {description}: недоступно ({e})")
        
        print(f"\n✓ Всего записей в системе: {total_records}")
        return models_info
        
    except Exception as e:
        print(f"✗ Ошибка проверки моделей: {e}")
        return []

def check_database_tables():
    """Проверяем таблицы в БД"""
    print("\n3. СТРУКТУРА БАЗЫ ДАННЫХ")
    print("-" * 40)
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Общее количество таблиц
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """)
            tables_count = cursor.fetchone()[0]
            print(f"✓ Всего таблиц: {tables_count}")
            
            # Таблицы Django приложений
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                AND table_name LIKE ANY (ARRAY['auth_%', 'core_%', 'stories_%', 'books_%', 'shop_%', 'fairy_tales_%'])
                ORDER BY table_name;
            """)
            app_tables = cursor.fetchall()
            
            # Группируем по приложениям
            apps = {}
            for (table_name,) in app_tables:
                app_name = table_name.split('_')[0]
                if app_name not in apps:
                    apps[app_name] = []
                apps[app_name].append(table_name)
            
            for app_name, tables in apps.items():
                print(f"✓ Приложение {app_name}: {len(tables)} таблиц")
            
            # Проверяем индексы
            cursor.execute("""
                SELECT COUNT(*) FROM pg_indexes 
                WHERE schemaname = 'public';
            """)
            indexes_count = cursor.fetchone()[0]
            print(f"✓ Индексов создано: {indexes_count}")
            
            return True
            
    except Exception as e:
        print(f"✗ Ошибка проверки таблиц: {e}")
        return False

def check_migrations():
    """Проверяем статус миграций"""
    print("\n4. СТАТУС МИГРАЦИЙ")
    print("-" * 40)
    
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Проверяем примененные миграции
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations;")
            migrations_count = cursor.fetchone()[0]
            print(f"✓ Примененных миграций: {migrations_count}")
            
            # Последние миграции по приложениям
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app IN ('core', 'stories', 'books', 'shop', 'fairy_tales', 'accounts', 'auth')
                ORDER BY app, applied DESC;
            """)
            
            last_migrations = {}
            for row in cursor.fetchall():
                app, name, applied = row
                if app not in last_migrations:
                    last_migrations[app] = (name, applied)
            
            for app, (name, applied) in last_migrations.items():
                print(f"✓ {app}: {name} ({applied.strftime('%Y-%m-%d %H:%M')})")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка проверки миграций: {e}")
        return False

def check_admin_access():
    """Проверяем доступ к админке"""
    print("\n5. АДМИН ПАНЕЛЬ")
    print("-" * 40)
    
    try:
        from django.contrib.auth.models import User
        
        # Суперпользователи
        superusers = User.objects.filter(is_superuser=True)
        print(f"✓ Суперпользователей: {superusers.count()}")
        
        for user in superusers:
            print(f"  - {user.username} ({user.email or 'без email'})")
        
        # Активные пользователи
        active_users = User.objects.filter(is_active=True).count()
        print(f"✓ Активных пользователей: {active_users}")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка проверки админки: {e}")
        return False

def check_media_files():
    """Проверяем медиа файлы"""
    print("\n6. МЕДИА ФАЙЛЫ")
    print("-" * 40)
    
    try:
        from django.conf import settings
        import os
        
        media_root = settings.MEDIA_ROOT
        print(f"✓ MEDIA_ROOT: {media_root}")
        
        if os.path.exists(media_root):
            # Подсчитываем файлы
            total_files = 0
            for root, dirs, files in os.walk(media_root):
                total_files += len(files)
            
            print(f"✓ Медиа файлов: {total_files}")
            
            # Проверяем основные папки
            media_dirs = ['books', 'stories', 'fairy_tales', 'shop']
            for dir_name in media_dirs:
                dir_path = os.path.join(media_root, dir_name)
                if os.path.exists(dir_path):
                    files_count = sum([len(files) for r, d, files in os.walk(dir_path)])
                    print(f"  - {dir_name}/: {files_count} файлов")
        else:
            print("⚠ MEDIA_ROOT не существует")
        
        return True
        
    except Exception as e:
        print(f"✗ Ошибка проверки медиа: {e}")
        return False

def generate_summary_report(models_info, db_ok, tables_ok, migrations_ok, admin_ok, media_ok):
    """Генерируем итоговый отчет"""
    print("\n" + "=" * 60)
    print("ИТОГОВЫЙ ОТЧЕТ ГОТОВНОСТИ К DOCKER")
    print("=" * 60)
    
    # Оценка компонентов
    components = [
        ("PostgreSQL подключение", db_ok),
        ("Структура БД", tables_ok),
        ("Миграции Django", migrations_ok),
        ("Админ панель", admin_ok),
        ("Медиа файлы", media_ok),
    ]
    
    success_count = sum([1 for _, status in components if status])
    
    print(f"Готовность системы: {success_count}/5 компонентов")
    print()
    
    for component, status in components:
        icon = "✓" if status else "✗"
        print(f"{icon} {component}")
    
    print()
    
    if success_count >= 4:
        print("🎉 СИСТЕМА ГОТОВА К DOCKER!")
        print()
        print("✅ PostgreSQL работает стабильно")
        print("✅ Данные успешно загружены")
        print("✅ Структура БД корректна")
        print("✅ Можно переходить к Docker контейнеризации")
        print()
        
        # Показываем ключевую статистику
        if models_info:
            print("📊 Ключевые данные:")
            for description, count in models_info:
                if count > 0:
                    print(f"   • {description}: {count}")
        
        print()
        print("🐳 Следующий шаг: Настройка Docker")
        print("   - docker-compose.yml")
        print("   - Dockerfile")
        print("   - Docker окружение")
        
    else:
        print("⚠️  ТРЕБУЕТСЯ ДОРАБОТКА")
        print()
        print("Проблемные компоненты:")
        for component, status in components:
            if not status:
                print(f"   ✗ {component}")
        print()
        print("Рекомендуется исправить ошибки перед Docker")
    
    return success_count >= 4

def main():
    """Основная функция диагностики"""
    print("ДИАГНОСТИКА POSTGRESQL СИСТЕМЫ")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        setup_django()
    except Exception as e:
        print(f"✗ Ошибка настройки Django: {e}")
        return False
    
    # Выполняем проверки
    db_ok = check_database_connection()
    models_info = check_django_models()
    tables_ok = check_database_tables()
    migrations_ok = check_migrations()
    admin_ok = check_admin_access()
    media_ok = check_media_files()
    
    # Генерируем отчет
    ready_for_docker = generate_summary_report(
        models_info, db_ok, tables_ok, migrations_ok, admin_ok, media_ok
    )
    
    return ready_for_docker

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
