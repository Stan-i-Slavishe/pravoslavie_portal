#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полное восстановление PostgreSQL БД с данными
"""

import psycopg2
import sys
import os

def recreate_database():
    """Пересоздаем базу данных с нуля"""
    
    postgres_password = 'postgres'
    
    print("Восстановление базы данных pravoslavie_local_db...")
    print("=" * 60)
    
    try:
        # Подключение как суперпользователь
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password=postgres_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Подключение к PostgreSQL успешно")
        
        # Показываем существующие БД
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        existing_dbs = [row[0] for row in cursor.fetchall()]
        print(f"Существующие БД: {existing_dbs}")
        
        # Удаляем БД если существует
        if 'pravoslavie_local_db' in existing_dbs:
            print("Удаляем существующую БД...")
            cursor.execute("DROP DATABASE pravoslavie_local_db;")
        
        # Создаем БД заново
        print("Создаем новую базу данных...")
        cursor.execute("""
            CREATE DATABASE pravoslavie_local_db 
            WITH 
            OWNER = pravoslavie_user
            ENCODING = 'UTF8'
            LC_COLLATE = 'C'
            LC_CTYPE = 'C'
            TEMPLATE = template0;
        """)
        print("База данных pravoslavie_local_db создана")
        
        # Предоставляем права
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE pravoslavie_local_db TO pravoslavie_user;")
        print("Права предоставлены")
        
        cursor.close()
        conn.close()
        
        # Тестируем подключение к новой БД
        print("\nТестируем подключение к новой БД...")
        test_conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='pravoslavie_local_db',
            user='pravoslavie_user',
            password='local_strong_password_2024'
        )
        
        test_cursor = test_conn.cursor()
        test_cursor.execute("SELECT current_database();")
        db_name = test_cursor.fetchone()[0]
        print(f"Подключение успешно! БД: {db_name}")
        
        test_cursor.close()
        test_conn.close()
        
        return True
        
    except Exception as e:
        print(f"Ошибка создания БД: {e}")
        return False

def apply_django_migrations():
    """Применяем миграции Django"""
    
    print("\n" + "=" * 60)
    print("ПРИМЕНЕНИЕ МИГРАЦИЙ DJANGO")
    print("=" * 60)
    
    try:
        import subprocess
        
        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['DJANGO_SETTINGS_MODULE'] = 'config.settings_local_postgresql'
        
        # Применяем миграции
        print("Применяем миграции Django...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("Миграции применены успешно!")
            print("STDOUT:", result.stdout)
            return True
        else:
            print(f"Ошибка применения миграций: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Ошибка применения миграций: {e}")
        return False

def restore_data_from_backup():
    """Восстанавливаем данные из бэкапа"""
    
    print("\n" + "=" * 60)
    print("ВОССТАНОВЛЕНИЕ ДАННЫХ ИЗ БЭКАПА")
    print("=" * 60)
    
    # Ищем последний бэкап
    import glob
    
    backup_patterns = [
        'backups/django_backup_*/full_data.json',
        'backups/*_20250901_2113.json',
        'backups/sqlite_*.json'
    ]
    
    backup_file = None
    for pattern in backup_patterns:
        files = glob.glob(pattern)
        if files:
            backup_file = max(files)  # Берем последний по имени
            break
    
    if not backup_file:
        print("Файлы бэкапа не найдены")
        print("Доступные файлы в backups/:")
        try:
            backup_files = glob.glob('backups/*.json')
            for f in backup_files[:10]:  # Показываем первые 10
                print(f"  {f}")
        except:
            pass
        return False
    
    print(f"Найден бэкап: {backup_file}")
    
    try:
        import subprocess
        
        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['DJANGO_SETTINGS_MODULE'] = 'config.settings_local_postgresql'
        
        # Загружаем данные
        print("Загружаем данные из бэкапа...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'loaddata', backup_file,
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("Данные восстановлены успешно!")
            # Показываем только важные строки вывода
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Installed' in line and 'object(s)' in line:
                    print(f"  {line}")
            return True
        else:
            print(f"Ошибка загрузки данных: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Ошибка восстановления данных: {e}")
        return False

def final_verification():
    """Финальная проверка системы"""
    
    print("\n" + "=" * 60)
    print("ФИНАЛЬНАЯ ПРОВЕРКА")
    print("=" * 60)
    
    try:
        # Настройка Django
        import django
        
        os.environ['DJANGO_ENV'] = 'local'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local_postgresql')
        
        sys.path.append('.')
        django.setup()
        
        from django.db import connection
        from django.contrib.auth.models import User
        
        # Проверка подключения
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"PostgreSQL версия: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"База данных: {db_name}")
        
        # Проверка данных
        users_count = User.objects.count()
        superuser_count = User.objects.filter(is_superuser=True).count()
        print(f"Пользователей: {users_count} (суперпользователей: {superuser_count})")
        
        # Проверка других моделей
        try:
            from stories.models import Story
            stories_count = Story.objects.count()
            print(f"Рассказов: {stories_count}")
        except:
            print("Рассказы: не доступны")
        
        try:
            from books.models import Book
            books_count = Book.objects.count()
            print(f"Книг: {books_count}")
        except:
            print("Книги: не доступны")
        
        try:
            from shop.models import Product
            products_count = Product.objects.count()
            print(f"Товаров: {products_count}")
        except:
            print("Товары: не доступны")
        
        return True
        
    except Exception as e:
        print(f"Ошибка финальной проверки: {e}")
        return False

if __name__ == "__main__":
    print("ПОЛНОЕ ВОССТАНОВЛЕНИЕ POSTGRESQL")
    print("=" * 60)
    print()
    
    # Шаг 1: Пересоздаем БД
    step1_ok = recreate_database()
    if not step1_ok:
        print("Не удалось создать БД. Остановка.")
        sys.exit(1)
    
    # Шаг 2: Применяем миграции
    step2_ok = apply_django_migrations()
    if not step2_ok:
        print("Не удалось применить миграции. Остановка.")
        sys.exit(1)
    
    # Шаг 3: Восстанавливаем данные
    step3_ok = restore_data_from_backup()
    if not step3_ok:
        print("Предупреждение: Данные не восстановлены")
    
    # Шаг 4: Финальная проверка
    step4_ok = final_verification()
    
    # Итоги
    print("\n" + "=" * 60)
    if step1_ok and step2_ok and step4_ok:
        print("ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("PostgreSQL готов к работе с Django")
        print()
        print("Следующие шаги:")
        print("1. Запустить: python verify_postgresql_integration.py")
        print("2. Протестировать сайт: python manage.py runserver --settings=config.settings_local_postgresql")
        print("3. При необходимости создать суперпользователя: python manage.py createsuperuser --settings=config.settings_local_postgresql")
    else:
        print("ЕСТЬ ПРОБЛЕМЫ В ВОССТАНОВЛЕНИИ")
        print("Требуется дополнительная диагностика")
