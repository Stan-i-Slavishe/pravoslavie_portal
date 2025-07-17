#!/usr/bin/env python
"""
🚀 Скрипт для оптимизации производительности Django проекта
"""
import os
import sys
import django
from pathlib import Path
import shutil

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def clean_logs():
    """Очистка логов"""
    print("🧹 Очистка логов...")
    logs_dir = BASE_DIR / 'logs'
    if logs_dir.exists():
        for log_file in logs_dir.glob('*.log'):
            if log_file.stat().st_size > 1024 * 1024:  # Больше 1MB
                print(f"  Очищаем {log_file.name} ({log_file.stat().st_size // 1024}KB)")
                log_file.write_text('')

def clean_cache():
    """Очистка кеша"""
    print("🗑️ Очистка кеша...")
    try:
        from django.core.cache import cache
        cache.clear()
        print("  ✅ Кеш очищен")
    except:
        print("  ⚠️ Не удалось очистить кеш")

def clean_sessions():
    """Очистка старых сессий"""
    print("🔄 Очистка сессий...")
    try:
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        from datetime import timedelta
        
        expired_sessions = Session.objects.filter(
            expire_date__lt=timezone.now() - timedelta(days=7)
        )
        count = expired_sessions.count()
        expired_sessions.delete()
        print(f"  ✅ Удалено {count} старых сессий")
    except Exception as e:
        print(f"  ⚠️ Ошибка при очистке сессий: {e}")

def clean_migrations():
    """Очистка лишних миграций"""
    print("📦 Проверка миграций...")
    migrations_to_check = []
    
    for app_dir in BASE_DIR.iterdir():
        if app_dir.is_dir() and (app_dir / 'migrations').exists():
            migrations_dir = app_dir / 'migrations'
            migration_files = list(migrations_dir.glob('*.py'))
            if len(migration_files) > 10:  # Много миграций
                migrations_to_check.append((app_dir.name, len(migration_files)))
    
    if migrations_to_check:
        print("  ⚠️ Приложения с большим количеством миграций:")
        for app_name, count in migrations_to_check:
            print(f"    {app_name}: {count} миграций")
        print("  💡 Рекомендуется сделать squashmigrations")

def clean_staticfiles():
    """Очистка статических файлов"""
    print("🎨 Очистка статических файлов...")
    staticfiles_dir = BASE_DIR / 'staticfiles'
    if staticfiles_dir.exists():
        size_before = sum(f.stat().st_size for f in staticfiles_dir.rglob('*') if f.is_file())
        shutil.rmtree(staticfiles_dir)
        print(f"  ✅ Удалено {size_before // 1024}KB статических файлов")

def optimize_database():
    """Оптимизация базы данных"""
    print("🗃️ Оптимизация базы данных...")
    try:
        from django.db import connection
        
        # Для SQLite
        if 'sqlite' in connection.settings_dict['ENGINE']:
            with connection.cursor() as cursor:
                cursor.execute("VACUUM;")
                cursor.execute("ANALYZE;")
            print("  ✅ SQLite оптимизирована")
        
        # Статистика
        from django.contrib.auth.models import User
        from django.contrib.sessions.models import Session
        
        users_count = User.objects.count()
        sessions_count = Session.objects.count()
        
        print(f"  📊 Пользователей: {users_count}")
        print(f"  📊 Активных сессий: {sessions_count}")
        
    except Exception as e:
        print(f"  ⚠️ Ошибка при оптимизации БД: {e}")

def check_performance():
    """Проверка производительности"""
    print("⚡ Проверка производительности...")
    
    # Проверка размера БД
    db_file = BASE_DIR / 'db.sqlite3'
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024 * 1024)
        print(f"  📁 Размер БД: {size_mb:.2f}MB")
        
        if size_mb > 10:
            print("  ⚠️ База данных большая, рекомендуется очистка тестовых данных")
    
    # Проверка медиа файлов
    media_dir = BASE_DIR / 'media'
    if media_dir.exists():
        media_size = sum(f.stat().st_size for f in media_dir.rglob('*') if f.is_file())
        print(f"  📁 Размер медиа: {media_size / (1024 * 1024):.2f}MB")

def main():
    """Основная функция оптимизации"""
    print("🚀 Начинаем оптимизацию Django проекта...")
    print("=" * 50)
    
    clean_logs()
    clean_cache()
    clean_sessions()
    clean_migrations()
    clean_staticfiles()
    optimize_database()
    check_performance()
    
    print("=" * 50)
    print("✅ Оптимизация завершена!")
    print("\n💡 Рекомендации:")
    print("1. Перезапустите сервер разработки")
    print("2. Используйте .env.lightweight для разработки")
    print("3. Регулярно очищайте тестовые данные")
    print("4. Отключите DEBUG в продакшене")

if __name__ == "__main__":
    main()
