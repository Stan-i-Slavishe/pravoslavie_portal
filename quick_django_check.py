#!/usr/bin/env python
"""
Быстрая диагностика Django проекта
Показывает конкретные ошибки при запуске
"""
import os
import sys
import subprocess
from pathlib import Path

def run_django_check():
    """Запускает Django проверку и показывает детальные ошибки"""
    print("🔍 БЫСТРАЯ ДИАГНОСТИКА DJANGO ПРОЕКТА")
    print("="*50)
    
    if not Path('manage.py').exists():
        print("❌ manage.py не найден в текущей директории")
        return
    
    print("\n1. Проверяем импорт Django...")
    try:
        import django
        print(f"   ✅ Django {django.get_version()} найден")
    except ImportError as e:
        print(f"   ❌ Django не найден: {e}")
        return
    
    print("\n2. Проверяем настройки проекта...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        print("   ✅ Настройки загружены успешно")
    except Exception as e:
        print(f"   ❌ Ошибка настроек: {e}")
        print("   💡 Попробуйте исправить config/settings.py")
        return
    
    print("\n3. Проверяем приложения Django...")
    try:
        from django.apps import apps
        app_configs = apps.get_app_configs()
        print(f"   ✅ Загружено {len(app_configs)} приложений")
        
        for app in app_configs:
            if app.name.startswith(('core', 'stories', 'books', 'shop', 'fairy_tales')):
                print(f"      • {app.name}")
    except Exception as e:
        print(f"   ❌ Ошибка загрузки приложений: {e}")
    
    print("\n4. Проверяем базу данных...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("   ✅ Подключение к БД работает")
    except Exception as e:
        print(f"   ❌ Ошибка БД: {e}")
        print("   💡 Проверьте настройки базы данных в settings.py")
    
    print("\n5. Проверяем миграции...")
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'showmigrations', '--list'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("   ✅ Миграции в порядке")
        else:
            print(f"   ❌ Проблемы с миграциями: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Ошибка проверки миграций: {e}")
    
    print("\n6. Полная проверка Django...")
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("   🎉 Все проверки пройдены!")
            print("   Django готов к запуску: python manage.py runserver")
        else:
            print(f"   ❌ Ошибки Django:")
            print(f"   {result.stderr}")
            
            # Пытаемся дать конкретные советы
            if "ImproperlyConfigured" in result.stderr:
                print("\n   💡 СОВЕТ: Проблема с настройками")
                print("      • Проверьте файл .env")
                print("      • Убедитесь что SECRET_KEY установлен")
                print("      • Проверьте настройки базы данных")
            
            if "ImportError" in result.stderr:
                print("\n   💡 СОВЕТ: Проблема с импортом")
                print("      • Установите зависимости: pip install -r requirements.txt")
                print("      • Активируйте виртуальное окружение")
            
            if "OperationalError" in result.stderr:
                print("\n   💡 СОВЕТ: Проблема с базой данных")
                print("      • Убедитесь что PostgreSQL запущен")
                print("      • Проверьте настройки подключения к БД")
                print("      • Запустите миграции: python manage.py migrate")
                
    except Exception as e:
        print(f"   ❌ Ошибка запуска проверки: {e}")

if __name__ == "__main__":
    run_django_check()
