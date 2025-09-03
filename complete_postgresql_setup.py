#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Завершение настройки PostgreSQL после миграций
"""

import os
import sys
import subprocess
import glob

def check_migrations_status():
    """Проверяем статус миграций"""
    
    print("Проверка статуса миграций...")
    print("=" * 40)
    
    try:
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Проверяем применены ли миграции
        result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations',
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.', encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("Миграции проверены успешно")
            # Считаем количество примененных миграций
            applied_count = result.stdout.count('[X]')
            unapplied_count = result.stdout.count('[ ]')
            print(f"Применено: {applied_count}, Не применено: {unapplied_count}")
            
            if unapplied_count == 0:
                print("Все миграции применены!")
                return True
            else:
                print(f"Есть неприменённые миграции: {unapplied_count}")
                return False
        else:
            print("Ошибка проверки миграций")
            return False
            
    except Exception as e:
        print(f"Исключение при проверке миграций: {e}")
        return False

def load_backup_data():
    """Загружаем данные из бэкапа"""
    
    print("\nЗагрузка данных из бэкапа...")
    print("=" * 40)
    
    # Ищем лучший бэкап
    backup_files = glob.glob('backups/django_backup_*/full_data.json')
    if not backup_files:
        backup_files = glob.glob('backups/sqlite_*.json') 
    if not backup_files:
        backup_files = glob.glob('backups/*.json')
    
    if not backup_files:
        print("Файлы бэкапа не найдены")
        return False
    
    # Берем самый новый файл
    best_backup = max(backup_files, key=os.path.getmtime)
    print(f"Используем бэкап: {best_backup}")
    
    try:
        env = os.environ.copy()
        env['DJANGO_ENV'] = 'local'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run([
            sys.executable, 'manage.py', 'loaddata', best_backup,
            '--settings=config.settings_local_postgresql'
        ], env=env, capture_output=True, text=True, cwd='.', encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("Данные загружены успешно!")
            # Подсчитываем импортированные объекты
            installed_count = result.stdout.count('Installed')
            print(f"Импортировано записей: {installed_count}")
            return True
        else:
            print("Ошибка загрузки данных:")
            print(result.stderr[:500])  # Первые 500 символов ошибки
            return False
            
    except Exception as e:
        print(f"Исключение при загрузке данных: {e}")
        return False

def test_django_connection():
    """Тестируем подключение Django"""
    
    print("\nТест подключения Django...")
    print("=" * 40)
    
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
            print(f"PostgreSQL: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"База данных: {db_name}")
            
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0]
            print(f"Пользователь: {user}")
        
        # Проверка данных
        try:
            users_count = User.objects.count()
            superusers = User.objects.filter(is_superuser=True).count()
            print(f"Пользователей: {users_count} (суперпользователей: {superusers})")
        except:
            print("Модель User недоступна")
        
        # Проверка других моделей
        model_checks = [
            ('stories.models', 'Story', 'Рассказов'),
            ('books.models', 'Book', 'Книг'),
            ('shop.models', 'Product', 'Товаров'),
            ('fairy_tales.models', 'FairyTale', 'Сказок')
        ]
        
        for module_name, model_name, description in model_checks:
            try:
                module = __import__(module_name, fromlist=[model_name])
                model = getattr(module, model_name)
                count = model.objects.count()
                print(f"{description}: {count}")
            except:
                print(f"{description}: недоступно")
        
        return True
        
    except Exception as e:
        print(f"Ошибка теста Django: {e}")
        return False

def create_superuser_if_needed():
    """Создаем суперпользователя если нет"""
    
    print("\nПроверка суперпользователей...")
    print("=" * 40)
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local_postgresql')
        django.setup()
        
        from django.contrib.auth.models import User
        
        superuser_count = User.objects.filter(is_superuser=True).count()
        
        if superuser_count == 0:
            print("Суперпользователей нет. Создаем...")
            
            # Создаем суперпользователя программно
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@pravoslavie-portal.ru',
                password='admin123'  # Временный пароль
            )
            print(f"Создан суперпользователь: {admin_user.username}")
            print("Логин: admin")
            print("Пароль: admin123 (измените через админку)")
        else:
            print(f"Найдено суперпользователей: {superuser_count}")
            
        return True
        
    except Exception as e:
        print(f"Ошибка создания суперпользователя: {e}")
        return False

def main():
    print("ЗАВЕРШЕНИЕ НАСТРОЙКИ POSTGRESQL")
    print("=" * 50)
    print()
    
    results = []
    
    # Проверяем миграции
    results.append(("Миграции", check_migrations_status()))
    
    # Загружаем данные
    results.append(("Загрузка данных", load_backup_data()))
    
    # Тестируем Django
    results.append(("Django подключение", test_django_connection()))
    
    # Создаем суперпользователя
    results.append(("Суперпользователь", create_superuser_if_needed()))
    
    # Итоги
    print("\n" + "=" * 50)
    print("ИТОГИ НАСТРОЙКИ:")
    print("=" * 50)
    
    success_count = 0
    for task, success in results:
        status = "УСПЕШНО" if success else "ОШИБКА"
        icon = "✓" if success else "✗"
        print(f"{icon} {task}: {status}")
        if success:
            success_count += 1
    
    if success_count >= 3:
        print("\nПОСТГРЕSQL НАСТРОЕН УСПЕШНО!")
        print("\nДля проверки выполните:")
        print("1. python verify_postgresql_integration.py")
        print("2. python manage.py runserver --settings=config.settings_local_postgresql")
        print("\nАдмин панель: http://127.0.0.1:8000/admin/")
        print("Логин: admin, Пароль: admin123")
    else:
        print("\nЕСТЬ ПРОБЛЕМЫ В НАСТРОЙКЕ")
        print("Требуется дополнительная диагностика")
    
    return success_count >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
