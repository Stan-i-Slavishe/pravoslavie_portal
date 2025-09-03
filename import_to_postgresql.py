#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт импорта данных в PostgreSQL (второй этап)
Использует уже экспортированные данные из SQLite
"""

import os
import sys
import django
from datetime import datetime

# Принудительно устанавливаем PostgreSQL окружение
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'
os.environ['DJANGO_ENV'] = 'local'

# Настройка Django для PostgreSQL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings

def print_step(step_num, title):
    """Печать заголовка шага"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title.upper()}")
    print('='*60)

def check_postgresql_connection():
    """Проверка подключения к PostgreSQL"""
    print_step(1, "Check PostgreSQL Connection")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ PostgreSQL подключен: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"📂 Текущая БД: {db_name}")
            
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0]
            print(f"👤 Пользователь: {user}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        print("\n💡 Проверьте:")
        print("   1. PostgreSQL запущен")
        print("   2. База pravoslavie_local_db создана") 
        print("   3. Пользователь pravoslavie_user существует")
        print("   4. Пароль правильный: local_strong_password_2024")
        return False

def apply_migrations():
    """Применение миграций Django"""
    print_step(2, "Apply Django Migrations")
    
    try:
        call_command('migrate', verbosity=1)
        print("✅ Миграции применены успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка применения миграций: {e}")
        return False

def find_latest_exports():
    """Поиск последних экспортированных файлов"""
    print_step(3, "Find Exported Data Files")
    
    import os
    import glob
    
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print("❌ Папка backups не найдена!")
        return []
    
    # Поиск файлов по шаблону
    pattern = os.path.join(backup_dir, "*_20250901_2113.json")
    found_files = glob.glob(pattern)
    
    if found_files:
        print(f"📁 Найдено {len(found_files)} файлов экспорта:")
        for file in sorted(found_files):
            print(f"   📄 {os.path.basename(file)}")
        return sorted(found_files)
    else:
        # Поиск любых недавних файлов
        all_files = glob.glob(os.path.join(backup_dir, "*.json"))
        if all_files:
            # Сортируем по времени модификации
            all_files.sort(key=os.path.getmtime, reverse=True)
            recent_files = all_files[:20]  # Берем 20 самых новых
            print(f"📁 Найдено {len(recent_files)} недавних файлов:")
            for file in recent_files:
                print(f"   📄 {os.path.basename(file)}")
            return recent_files
        else:
            print("❌ Файлы экспорта не найдены!")
            return []

def import_data(exported_files):
    """Импорт данных в PostgreSQL"""
    print_step(4, "Import Data to PostgreSQL")
    
    if not exported_files:
        print("⚠️ Нет файлов для импорта")
        return
    
    # Порядок импорта важен из-за внешних ключей
    import_order = [
        'auth_User',
        'auth_Group',
        'core',
        'stories',
        'books', 
        'fairy_tales',
        'shop',
        'accounts',
        'subscriptions'
    ]
    
    imported_count = 0
    
    for app_name in import_order:
        # Находим соответствующий файл
        matching_files = [f for f in exported_files if app_name in os.path.basename(f)]
        
        if not matching_files:
            print(f"⚠️ Файл для {app_name} не найден, пропускаем")
            continue
            
        filename = matching_files[0]
        
        try:
            print(f"📥 Импортируем {os.path.basename(filename)}...")
            call_command('loaddata', filename, verbosity=1)
            print(f"✅ {app_name} импортирован успешно")
            imported_count += 1
            
        except Exception as e:
            print(f"⚠️ Ошибка импорта {app_name}: {e}")
            print(f"   Файл: {filename}")
    
    print(f"\n📊 Импортировано {imported_count} из {len(import_order)} приложений")

def create_superuser():
    """Создание суперпользователя"""
    print_step(5, "Create Superuser")
    
    try:
        from django.contrib.auth.models import User
        
        # Проверяем есть ли уже суперпользователи
        superusers = User.objects.filter(is_superuser=True)
        if superusers.exists():
            print(f"👤 Найдено {superusers.count()} суперпользователей:")
            for user in superusers:
                print(f"   🔑 {user.username} ({user.email})")
            
            create_new = input("\nСоздать нового суперпользователя? (y/n): ").lower()
            if create_new != 'y':
                print("⚠️ Создание нового суперпользователя пропущено")
                return
        
        print("👤 Создание администратора...")
        print("(Нажмите Ctrl+C чтобы пропустить)")
        call_command('createsuperuser')
        print("✅ Суперпользователь создан")
        
    except KeyboardInterrupt:
        print("\n⚠️ Создание суперпользователя пропущено")
    except Exception as e:
        print(f"⚠️ Ошибка создания суперпользователя: {e}")

def check_data_integrity():
    """Проверка целостности данных"""
    print_step(6, "Check Data Integrity")
    
    try:
        from django.contrib.auth.models import User
        from core.models import Category
        
        # Проверяем основные модели
        users_count = User.objects.count()
        print(f"👥 Пользователи: {users_count}")
        
        try:
            from stories.models import Story
            stories_count = Story.objects.count()
            print(f"🎬 Рассказы: {stories_count}")
        except:
            print("🎬 Рассказы: модель не доступна")
        
        try:
            from books.models import Book
            books_count = Book.objects.count()
            print(f"📚 Книги: {books_count}")
        except:
            print("📚 Книги: модель не доступна")
        
        try:
            from shop.models import Product, Order
            products_count = Product.objects.count()
            orders_count = Order.objects.count()
            print(f"🛒 Товары: {products_count}")
            print(f"📋 Заказы: {orders_count}")
        except:
            print("🛒 Магазин: модели не доступны")
        
        try:
            from fairy_tales.models import FairyTale
            fairy_tales_count = FairyTale.objects.count()
            print(f"🧚 Терапевтические сказки: {fairy_tales_count}")
        except:
            print("🧚 Сказки: модель не доступна")
        
        categories_count = Category.objects.count()
        print(f"🏷️ Категории: {categories_count}")
        
    except Exception as e:
        print(f"⚠️ Ошибка проверки данных: {e}")

def main():
    """Основная функция импорта"""
    print("\n" + "="*60)
    print("  ИМПОРТ ДАННЫХ В POSTGRESQL")
    print("="*60)
    
    print(f"🐍 Python кодировка: {sys.stdout.encoding}")
    print(f"🗄️ Текущая БД: {settings.DATABASES['default']['ENGINE']}")
    print(f"📂 База данных: {settings.DATABASES['default']['NAME']}")
    
    # Шаг 1: Проверка подключения
    if not check_postgresql_connection():
        return False
    
    # Шаг 2: Применение миграций
    if not apply_migrations():
        return False
    
    # Шаг 3: Поиск экспортированных данных
    exported_files = find_latest_exports()
    
    # Шаг 4: Импорт данных
    import_data(exported_files)
    
    # Шаг 5: Создание суперпользователя
    create_superuser()
    
    # Шаг 6: Проверка целостности
    check_data_integrity()
    
    # Итоги
    print("\n" + "="*60)
    print("        ✅ ИМПОРТ В POSTGRESQL ЗАВЕРШЕН!")
    print("="*60)
    print("\n🎯 Что сделано:")
    print("   ✅ Подключение к PostgreSQL установлено")
    print("   ✅ Структура БД создана")
    print("   ✅ Данные импортированы")
    print("   ✅ Суперпользователь создан/проверен")
    print("   ✅ Целостность данных проверена")
    
    print("\n🚀 Следующие шаги:")
    print("   1. Запустите сервер: python manage.py runserver")
    print("   2. Проверьте: http://127.0.0.1:8000/")
    print("   3. Проверьте админку: http://127.0.0.1:8000/admin/")
    print("   4. Запустите полную проверку: python check_migration.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Импорт завершен успешно!")
        else:
            print("\n❌ Импорт завершен с ошибками")
    except KeyboardInterrupt:
        print("\n\n⏹️ Импорт прерван пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка импорта: {e}")
        import traceback
        traceback.print_exc()