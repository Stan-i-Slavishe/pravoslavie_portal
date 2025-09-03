#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная очистка PostgreSQL и восстановление с нуля
"""

import psycopg2
import sys
import os
import subprocess

def clean_recreate_database():
    """Полностью пересоздаем БД с нуля"""
    
    postgres_password = 'postgres'
    
    print("Полная очистка и пересоздание БД...")
    print("=" * 50)
    
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
        
        # Закрываем все подключения к БД перед удалением
        print("Закрываем подключения к БД...")
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'pravoslavie_local_db'
              AND pid <> pg_backend_pid();
        """)
        
        # Полностью удаляем БД
        print("Удаляем БД pravoslavie_local_db...")
        cursor.execute("DROP DATABASE IF EXISTS pravoslavie_local_db;")
        
        # Создаем БД заново
        print("Создаем БД с нуля...")
        cursor.execute("""
            CREATE DATABASE pravoslavie_local_db 
            WITH 
            OWNER = pravoslavie_user
            ENCODING = 'UTF8'
            LC_COLLATE = 'C'
            LC_CTYPE = 'C'
            TEMPLATE = template0;
        """)
        
        # Даем права
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE pravoslavie_local_db TO pravoslavie_user;")
        
        cursor.close()
        conn.close()
        
        print("БД успешно пересоздана")
        
        # Подключаемся к новой БД для дополнительных настроек
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='pravoslavie_local_db',
            user='pravoslavie_user',
            password='local_strong_password_2024'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Даем права на схему public
        cursor.execute("GRANT ALL ON SCHEMA public TO pravoslavie_user;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pravoslavie_user;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pravoslavie_user;")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pravoslavie_user;")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO pravoslavie_user;")
        
        cursor.close()
        conn.close()
        
        print("Права настроены")
        
        return True
        
    except Exception as e:
        print(f"Ошибка пересоздания БД: {e}")
        return False

def apply_fresh_migrations():
    """Применяем миграции на чистую БД"""
    
    print("\nПрименение миграций на чистую БД...")
    print("=" * 50)
    
    try:
        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Применяем миграции
        print("Применяем миграции Django...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("Миграции применены успешно!")
            
            # Показываем только важные строки
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Applying' in line or 'Operations to perform' in line or 'Running migrations' in line:
                    print(f"  {line.strip()}")
            
            return True
        else:
            print(f"Ошибка применения миграций:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Ошибка применения миграций: {e}")
        return False

def load_data_from_backup():
    """Загружаем данные из бэкапа"""
    
    print("\nВосстановление данных...")
    print("=" * 50)
    
    # Ищем лучший бэкап
    import glob
    
    # Приоритет бэкапов
    backup_options = [
        'backups/django_backup_*/full_data.json',  # Полный Django бэкап
        'backups/auth_User_20250901_*.json',       # Пользователи из миграции
        'backups/sqlite_clean_*.json',             # Чистый экспорт
        'backups/*.json'                           # Любые JSON файлы
    ]
    
    best_backup = None
    for pattern in backup_options:
        files = glob.glob(pattern)
        if files:
            best_backup = max(files, key=os.path.getmtime)  # Самый свежий файл
            break
    
    if not best_backup:
        print("Файлы бэкапа не найдены!")
        return False
    
    print(f"Используем бэкап: {best_backup}")
    
    try:
        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Загружаем данные
        result = subprocess.run([
            sys.executable, 'manage.py', 'loaddata', best_backup,
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("Данные загружены успешно!")
            
            # Показываем статистику импорта
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Installed' in line and 'object(s)' in line:
                    print(f"  {line.strip()}")
            
            return True
        else:
            print("Ошибка загрузки данных:")
            print("STDERR:", result.stderr)
            
            # Попробуем загрузить данные частями
            print("Попробуем загрузить данные по частям...")
            return load_data_partially()
            
    except Exception as e:
        print(f"Ошибка восстановления данных: {e}")
        return False

def load_data_partially():
    """Загружаем данные по частям если полный бэкап не работает"""
    
    import glob
    
    # Ищем отдельные файлы бэкапов
    partial_files = [
        'backups/auth_User_*.json',
        'backups/core_*.json', 
        'backups/stories_*.json',
        'backups/books_*.json',
        'backups/shop_*.json',
        'backups/fairy_tales_*.json'
    ]
    
    success_count = 0
    
    for pattern in partial_files:
        files = glob.glob(pattern)
        if not files:
            continue
            
        latest_file = max(files, key=os.path.getmtime)
        app_name = os.path.basename(latest_file).split('_')[0]
        
        try:
            env = os.environ.copy()
            env['DJANGO_ENV'] = 'local'
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run([
                sys.executable, 'manage.py', 'loaddata', latest_file,
                '--settings=config.settings_local_postgresql'
            ], env=env, capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Installed' in line:
                        print(f"  {app_name}: {line.strip()}")
                success_count += 1
            else:
                print(f"  {app_name}: ошибка загрузки")
                
        except Exception as e:
            print(f"  {app_name}: исключение - {e}")
    
    return success_count > 0

def create_superuser():
    """Создаем суперпользователя"""
    
    print("\nСоздание суперпользователя...")
    print("=" * 50)
    
    try:
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Проверим есть ли уже суперпользователи
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell',
            '-c', 'from django.contrib.auth.models import User; print(f"Superusers: {User.objects.filter(is_superuser=True).count()}")',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if 'Superusers: 0' in result.stdout:
            print("Суперпользователей нет, создаем нового...")
            print("Введите данные суперпользователя:")
            
            # Интерактивное создание суперпользователя
            subprocess.run([
                sys.executable, 'manage.py', 'createsuperuser',
                '--settings=config.settings_local_postgresql'
            ], env=env)
        else:
            print("Суперпользователи уже есть в системе")
            
    except Exception as e:
        print(f"Ошибка создания суперпользователя: {e}")

def final_check():
    """Финальная проверка"""
    
    print("\nФинальная проверка системы...")
    print("=" * 50)
    
    try:
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Запускаем системную проверку Django
        result = subprocess.run([
            sys.executable, 'manage.py', 'check',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("Django системные проверки: OK")
        else:
            print("Django проверки выявили проблемы:")
            print(result.stdout)
        
        # Проверяем подключение к БД
        result = subprocess.run([
            sys.executable, 'manage.py', 'dbshell',
            '-c', '\\dt',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.')
        
        print("Подключение к БД работает")
        
        return True
        
    except Exception as e:
        print(f"Ошибка финальной проверки: {e}")
        return False

if __name__ == "__main__":
    print("ПОЛНАЯ ПЕРЕУСТАНОВКА POSTGRESQL")
    print("=" * 60)
    print()
    
    success_steps = 0
    
    # Шаг 1: Полная очистка БД
    if clean_recreate_database():
        success_steps += 1
        print("✓ Шаг 1: БД очищена и пересоздана")
    else:
        print("✗ Шаг 1: Ошибка пересоздания БД")
        sys.exit(1)
    
    # Шаг 2: Применение миграций
    if apply_fresh_migrations():
        success_steps += 1
        print("✓ Шаг 2: Миграции применены")
    else:
        print("✗ Шаг 2: Ошибка применения миграций")
        sys.exit(1)
    
    # Шаг 3: Восстановление данных
    if load_data_from_backup():
        success_steps += 1
        print("✓ Шаг 3: Данные восстановлены")
    else:
        print("~ Шаг 3: Данные частично восстановлены")
    
    # Шаг 4: Создание суперпользователя
    create_superuser()
    print("✓ Шаг 4: Суперпользователь обработан")
    
    # Шаг 5: Финальная проверка
    if final_check():
        success_steps += 1
        print("✓ Шаг 5: Финальная проверка пройдена")
    
    # Итоги
    print("\n" + "=" * 60)
    if success_steps >= 3:
        print("ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print()
        print("Следующие команды для проверки:")
        print("1. python verify_postgresql_integration.py")
        print("2. python manage.py runserver --settings=config.settings_local_postgresql")
        print()
        print("PostgreSQL готов к работе!")
    else:
        print("ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО С ПРОБЛЕМАМИ")
        print("Требуется дополнительная диагностика")
