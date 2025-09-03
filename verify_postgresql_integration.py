#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная проверка работы Django с PostgreSQL
"""

import os
import sys
import django
from datetime import datetime

# Настройка Django
os.environ['DJANGO_ENV'] = 'local'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from io import StringIO

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title.upper()}")
    print('='*60)

def print_subsection(title):
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print('-'*40)

def check_database_connection():
    """Проверка подключения к базе данных"""
    print_section("DATABASE CONNECTION CHECK")
    
    try:
        # Проверяем настройки БД
        db_config = settings.DATABASES['default']
        print(f"Engine: {db_config['ENGINE']}")
        print(f"Database: {db_config['NAME']}")
        print(f"Host: {db_config.get('HOST', 'localhost')}")
        print(f"Port: {db_config.get('PORT', '5432')}")
        print(f"User: {db_config.get('USER', 'not set')}")
        
        # Тестируем подключение
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"\nPostgreSQL Version: {version[:80]}...")
            
            cursor.execute("SELECT current_database();")
            current_db = cursor.fetchone()[0]
            print(f"Current Database: {current_db}")
            
            cursor.execute("SELECT current_user;")
            current_user = cursor.fetchone()[0]
            print(f"Current User: {current_user}")
            
            # Проверяем что можем писать в БД
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cursor.fetchone()[0]
            print(f"Tables in database: {table_count}")
            
        return True
        
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False

def check_models_data():
    """Проверка данных в моделях"""
    print_section("DATA VERIFICATION")
    
    checks = []
    
    # Пользователи
    try:
        from django.contrib.auth.models import User
        users_count = User.objects.count()
        superuser_count = User.objects.filter(is_superuser=True).count()
        print(f"Users: {users_count} (Superusers: {superuser_count})")
        checks.append(('Users', users_count > 0))
        
        # Показываем суперпользователей
        if superuser_count > 0:
            print("  Superusers:")
            for user in User.objects.filter(is_superuser=True):
                print(f"    - {user.username} ({user.email})")
    except Exception as e:
        print(f"Users check failed: {e}")
        checks.append(('Users', False))
    
    # Рассказы
    try:
        from stories.models import Story
        stories_count = Story.objects.count()
        print(f"Stories: {stories_count}")
        checks.append(('Stories', stories_count > 0))
        
        if stories_count > 0:
            recent_story = Story.objects.order_by('-created_at').first()
            print(f"  Most recent: {recent_story.title[:50]}...")
    except Exception as e:
        print(f"Stories check failed: {e}")
        checks.append(('Stories', False))
    
    # Книги
    try:
        from books.models import Book
        books_count = Book.objects.count()
        print(f"Books: {books_count}")
        checks.append(('Books', books_count > 0))
        
        if books_count > 0:
            paid_books = Book.objects.filter(price__gt=0).count()
            free_books = books_count - paid_books
            print(f"  Paid: {paid_books}, Free: {free_books}")
    except Exception as e:
        print(f"Books check failed: {e}")
        checks.append(('Books', False))
    
    # Магазин
    try:
        from shop.models import Product, Order
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        print(f"Shop Products: {products_count}")
        print(f"Orders: {orders_count}")
        checks.append(('Shop', products_count > 0))
    except Exception as e:
        print(f"Shop check failed: {e}")
        checks.append(('Shop', False))
    
    # Сказки
    try:
        from fairy_tales.models import FairyTale
        fairy_tales_count = FairyTale.objects.count()
        print(f"Fairy Tales: {fairy_tales_count}")
        checks.append(('Fairy Tales', fairy_tales_count > 0))
    except Exception as e:
        print(f"Fairy Tales check failed: {e}")
        checks.append(('Fairy Tales', False))
    
    # Категории
    try:
        from core.models import Category
        categories_count = Category.objects.count()
        print(f"Categories: {categories_count}")
        checks.append(('Categories', categories_count > 0))
    except Exception as e:
        print(f"Categories check failed: {e}")
        checks.append(('Categories', False))
    
    return checks

def test_database_operations():
    """Тестируем операции записи/чтения"""
    print_section("DATABASE OPERATIONS TEST")
    
    try:
        # Тестируем создание записи
        from core.models import Category
        
        test_category_name = f"Test Category {datetime.now().strftime('%H%M%S')}"
        test_category = Category.objects.create(
            name=test_category_name,
            slug=f"test-category-{datetime.now().strftime('%H%M%S')}",
            description="Test category for PostgreSQL verification"
        )
        
        print(f"Created test category: {test_category.name}")
        
        # Проверяем что можем читать
        read_category = Category.objects.get(id=test_category.id)
        print(f"Successfully read category: {read_category.name}")
        
        # Обновляем запись
        read_category.description = "Updated description"
        read_category.save()
        print("Successfully updated category")
        
        # Удаляем тестовую запись
        read_category.delete()
        print("Successfully deleted test category")
        
        print("All database operations work correctly!")
        return True
        
    except Exception as e:
        print(f"Database operations test failed: {e}")
        return False

def check_media_files():
    """Проверяем медиа-файлы"""
    print_section("MEDIA FILES CHECK")
    
    media_root = settings.MEDIA_ROOT
    print(f"Media root: {media_root}")
    
    if not os.path.exists(media_root):
        print("Media directory does not exist")
        return False
    
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk(media_root):
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            total_files += 1
            total_size += size
    
    print(f"Total media files: {total_files}")
    print(f"Total size: {total_size/1024/1024:.1f} MB")
    
    # Проверяем основные папки
    subdirs = ['books', 'shop', 'fairy_tales']
    for subdir in subdirs:
        subdir_path = os.path.join(media_root, subdir)
        if os.path.exists(subdir_path):
            file_count = sum(len(files) for _, _, files in os.walk(subdir_path))
            print(f"  {subdir}/: {file_count} files")
        else:
            print(f"  {subdir}/: not found")
    
    return total_files > 0

def run_django_checks():
    """Запускаем встроенные проверки Django"""
    print_section("DJANGO SYSTEM CHECKS")
    
    try:
        # Перенаправляем вывод
        output = StringIO()
        call_command('check', stdout=output, stderr=output)
        
        result = output.getvalue()
        if result.strip():
            print(result)
        else:
            print("No issues found")
        
        return True
        
    except Exception as e:
        print(f"Django checks failed: {e}")
        return False

def test_admin_access():
    """Проверяем доступ к админке"""
    print_section("ADMIN INTERFACE CHECK")
    
    try:
        from django.contrib.admin import site
        from django.contrib.auth.models import User
        
        # Проверяем что есть суперпользователи
        superusers = User.objects.filter(is_superuser=True)
        if not superusers.exists():
            print("WARNING: No superusers found")
            return False
        
        print(f"Superusers available: {superusers.count()}")
        
        # Проверяем зарегистрированные модели в админке
        registered_models = len(site._registry)
        print(f"Models registered in admin: {registered_models}")
        
        # Показываем некоторые зарегистрированные модели
        print("Admin registered models:")
        for model, admin_class in list(site._registry.items())[:5]:
            print(f"  - {model._meta.app_label}.{model._meta.model_name}")
        
        if registered_models > 5:
            print(f"  ... and {registered_models - 5} more")
        
        return True
        
    except Exception as e:
        print(f"Admin check failed: {e}")
        return False

def main():
    """Основная функция проверки"""
    
    print("PostgreSQL Integration Verification")
    print(f"Timestamp: {datetime.now()}")
    print(f"Django Environment: {os.environ.get('DJANGO_ENV', 'not set')}")
    
    all_checks = []
    
    # 1. Проверка подключения к БД
    db_ok = check_database_connection()
    all_checks.append(('Database Connection', db_ok))
    
    if not db_ok:
        print("\nSKIPPING remaining checks due to database connection failure")
        return False
    
    # 2. Проверка данных
    data_checks = check_models_data()
    all_checks.extend(data_checks)
    
    # 3. Тестирование операций БД
    operations_ok = test_database_operations()
    all_checks.append(('Database Operations', operations_ok))
    
    # 4. Проверка медиа-файлов
    media_ok = check_media_files()
    all_checks.append(('Media Files', media_ok))
    
    # 5. Django системные проверки
    django_checks_ok = run_django_checks()
    all_checks.append(('Django Checks', django_checks_ok))
    
    # 6. Проверка админки
    admin_ok = test_admin_access()
    all_checks.append(('Admin Interface', admin_ok))
    
    # Итоговый отчет
    print_section("FINAL REPORT")
    
    passed = 0
    failed = 0
    
    for check_name, result in all_checks:
        status = "PASS" if result else "FAIL"
        icon = "✓" if result else "✗"
        print(f"{icon} {check_name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nSUMMARY: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 ALL CHECKS PASSED!")
        print("PostgreSQL integration is working correctly.")
        print("Ready to proceed with Docker containerization.")
        return True
    else:
        print(f"\n⚠️ {failed} CHECKS FAILED")
        print("Please resolve issues before proceeding.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nCheck interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
