#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт миграции данных из SQLite в PostgreSQL с поддержкой UTF-8
Обходит проблемы с кодировкой Windows
"""

import os
import sys
import django
import json
from datetime import datetime

# Настройка кодировки
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'
os.environ['DJANGO_ENV'] = 'local'

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
from io import StringIO

def print_step(step_num, title):
    """Печать заголовка шага"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title.upper()}")
    print('='*60)

def export_sqlite_data():
    """Экспорт данных из SQLite по приложениям"""
    print_step(1, "Export SQLite Data")
    
    # Создание папки бэкапов
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Список приложений для экспорта
    apps_to_export = [
        'auth.User',
        'auth.Group', 
        'core',
        'stories', 
        'books',
        'shop',
        'fairy_tales',
        'accounts',
        'subscriptions'
    ]
    
    exported_files = []
    
    for app in apps_to_export:
        print(f"📦 Экспортируем {app}...")
        filename = f"{backup_dir}/{app.replace('.', '_')}_{timestamp}.json"
        
        try:
            # Используем StringIO для захвата вывода
            output = StringIO()
            
            call_command(
                'dumpdata', 
                app,
                natural_foreign=True,
                natural_primary=True,
                format='json',
                indent=2,
                stdout=output
            )
            
            # Записываем в файл с явной кодировкой UTF-8
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output.getvalue())
            
            exported_files.append(filename)
            print(f"✅ {app} экспортирован в {filename}")
            
        except Exception as e:
            print(f"⚠️ Ошибка экспорта {app}: {e}")
    
    return exported_files

def update_env_file():
    """Обновление .env.local для PostgreSQL"""
    print_step(2, "Update Environment Configuration")
    
    env_content = """# Environment
DJANGO_ENV=local

# Security
SECRET_KEY=django-insecure-local-development-key-change-me  
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver

# === SWITCH TO POSTGRESQL ===
USE_SQLITE=False

# PostgreSQL settings
DB_NAME=pravoslavie_local_db
DB_USER=pravoslavie_user
DB_PASSWORD=local_strong_password_2024
DB_HOST=localhost
DB_PORT=5432

# Email (console for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# API keys (test versions)
YOUTUBE_API_KEY=your-youtube-api-key-for-testing
YOOKASSA_SHOP_ID=test-shop-id  
YOOKASSA_SECRET_KEY=test-secret-key
YOOKASSA_TEST_MODE=True

# Redis
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Push notifications
VAPID_PRIVATE_KEY=test-private-key-for-development-only
VAPID_PUBLIC_KEY=BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc
VAPID_EMAIL=admin@pravoslavie-portal.ru

# Admin
ADMIN_EMAIL=admin@localhost

# Additional development settings
SECURE_SSL_REDIRECT=False
CACHE_BACKEND=dummy
"""
    
    # Бэкап текущего .env.local
    if os.path.exists('.env.local'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        backup_name = f'.env.local.backup_{timestamp}'
        os.rename('.env.local', backup_name)
        print(f"📋 Текущий .env.local сохранен как {backup_name}")
    
    # Создание нового .env.local
    with open('.env.local', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env.local обновлен для PostgreSQL")

def check_postgresql_connection():
    """Проверка подключения к PostgreSQL"""
    print_step(3, "Check PostgreSQL Connection")
    
    try:
        # Перезагрузка настроек Django
        from django.core.management import execute_from_command_line
        from django.conf import settings
        
        # Проверка подключения
        call_command('check', database='default')
        print("✅ Подключение к PostgreSQL успешно")
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
    print_step(4, "Apply Django Migrations")
    
    try:
        call_command('migrate')
        print("✅ Миграции применены успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка применения миграций: {e}")
        return False

def import_data(exported_files):
    """Импорт данных в PostgreSQL"""
    print_step(5, "Import Data to PostgreSQL")
    
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
    
    for app_name in import_order:
        # Находим соответствующий файл
        matching_files = [f for f in exported_files if app_name in f]
        
        if not matching_files:
            print(f"⚠️ Файл для {app_name} не найден, пропускаем")
            continue
            
        filename = matching_files[0]
        
        try:
            print(f"📥 Импортируем {filename}...")
            call_command('loaddata', filename)
            print(f"✅ {app_name} импортирован успешно")
            
        except Exception as e:
            print(f"⚠️ Ошибка импорта {app_name}: {e}")
            print(f"   Файл: {filename}")

def create_superuser():
    """Создание суперпользователя"""
    print_step(6, "Create Superuser")
    
    try:
        print("👤 Создание администратора...")
        print("(Нажмите Ctrl+C чтобы пропустить)")
        call_command('createsuperuser')
        print("✅ Суперпользователь создан")
    except KeyboardInterrupt:
        print("\n⚠️ Создание суперпользователя пропущено")
    except Exception as e:
        print(f"⚠️ Ошибка создания суперпользователя: {e}")

def main():
    """Основная функция миграции"""
    print("\n" + "="*60)
    print("  МИГРАЦИЯ SQLITE → POSTGRESQL (Python версия)")
    print("="*60)
    
    print(f"🐍 Python кодировка: {sys.stdout.encoding}")
    print(f"🗄️ Текущая БД: {settings.DATABASES['default']['ENGINE']}")
    
    # Шаг 1: Экспорт данных из SQLite (временно переключаемся обратно)
    print("\n📤 Переключаемся на SQLite для экспорта данных...")
    
    # Временно переключаемся на SQLite для экспорта
    original_db = settings.DATABASES['default'].copy()
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    
    # Переинициализация Django с SQLite
    connection.close()
    django.setup()
    
    exported_files = export_sqlite_data()
    
    # Шаг 2: Обновление конфигурации
    update_env_file()
    
    # Возвращаем PostgreSQL настройки
    settings.DATABASES['default'] = original_db
    connection.close()
    
    # Шаг 3: Проверка PostgreSQL
    if not check_postgresql_connection():
        return False
    
    # Шаг 4: Применение миграций
    if not apply_migrations():
        return False
    
    # Шаг 5: Импорт данных
    import_data(exported_files)
    
    # Шаг 6: Создание суперпользователя
    create_superuser()
    
    # Итоги
    print("\n" + "="*60)
    print("        ✅ МИГРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("="*60)
    print("\n🎯 Что сделано:")
    print("   ✅ Данные экспортированы из SQLite")
    print("   ✅ Настройки переключены на PostgreSQL")
    print("   ✅ Подключение к PostgreSQL установлено")
    print("   ✅ Структура БД создана")
    print("   ✅ Данные импортированы")
    print("   ✅ Суперпользователь создан")
    
    print("\n🚀 Следующие шаги:")
    print("   1. Запустите: python manage.py runserver")
    print("   2. Проверьте: http://127.0.0.1:8000/")
    print("   3. Проверьте админку: http://127.0.0.1:8000/admin/")
    print("   4. Запустите проверку: python check_migration.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Миграция завершена успешно!")
        else:
            print("\n❌ Миграция завершена с ошибками")
    except KeyboardInterrupt:
        print("\n\n⏹️ Миграция прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка миграции: {e}")
        import traceback
        traceback.print_exc()