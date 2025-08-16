#!/usr/bin/env python
"""
Диагностический скрипт для проверки админки Django
Проверяет основные проблемы и предлагает решения
"""

import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка инициализации Django: {e}")
    sys.exit(1)

def check_admin_issues():
    """Проверяет основные проблемы с админкой"""
    
    print("🔍 ДИАГНОСТИКА АДМИНКИ DJANGO")
    print("=" * 50)
    
    issues_found = []
    
    # 1. Проверка базы данных
    print("\n1️⃣ Проверка подключения к базе данных...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ База данных доступна")
    except Exception as e:
        print(f"❌ Проблема с базой данных: {e}")
        issues_found.append("База данных недоступна")
    
    # 2. Проверка миграций
    print("\n2️⃣ Проверка миграций...")
    try:
        from django.core.management import execute_from_command_line
        from io import StringIO
        import contextlib
        
        # Захватываем вывод команды
        f = StringIO()
        with contextlib.redirect_stdout(f):
            try:
                execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
                print("✅ Миграции в порядке")
            except SystemExit:
                pass
    except Exception as e:
        print(f"⚠️ Не удалось проверить миграции: {e}")
        issues_found.append("Возможные проблемы с миграциями")
    
    # 3. Проверка пользователей админки
    print("\n3️⃣ Проверка пользователей админки...")
    try:
        from django.contrib.auth.models import User
        admin_users = User.objects.filter(is_superuser=True)
        if admin_users.exists():
            print(f"✅ Найдено {admin_users.count()} суперпользователей")
        else:
            print("⚠️ Нет суперпользователей! Создайте через: python manage.py createsuperuser")
            issues_found.append("Нет суперпользователей")
    except Exception as e:
        print(f"❌ Ошибка проверки пользователей: {e}")
        issues_found.append("Ошибка проверки пользователей")
    
    # 4. Проверка статических файлов
    print("\n4️⃣ Проверка статических файлов...")
    try:
        from django.conf import settings
        static_root = getattr(settings, 'STATIC_ROOT', None)
        static_url = getattr(settings, 'STATIC_URL', None)
        
        if static_url:
            print(f"✅ STATIC_URL: {static_url}")
        else:
            print("⚠️ STATIC_URL не настроен")
            issues_found.append("STATIC_URL не настроен")
            
        if static_root:
            print(f"✅ STATIC_ROOT: {static_root}")
        else:
            print("⚠️ STATIC_ROOT не настроен")
    except Exception as e:
        print(f"❌ Ошибка проверки статических файлов: {e}")
        
    # 5. Проверка middleware
    print("\n5️⃣ Проверка middleware...")
    try:
        from django.conf import settings
        middleware = getattr(settings, 'MIDDLEWARE', [])
        
        # Проверяем проблемные middleware
        problematic = [
            'stories.middleware.AdminPerformanceMiddleware',
            'stories.middleware.DatabaseOptimizationMiddleware'
        ]
        
        for mw in problematic:
            if mw in middleware:
                print(f"⚠️ Найден проблемный middleware: {mw}")
                issues_found.append(f"Проблемный middleware: {mw}")
            else:
                print(f"✅ Middleware {mw} отключен")
                
    except Exception as e:
        print(f"❌ Ошибка проверки middleware: {e}")
    
    # 6. Проверка Stories модели
    print("\n6️⃣ Проверка модели Stories...")
    try:
        from stories.models import Story
        story_count = Story.objects.count()
        print(f"✅ Найдено {story_count} рассказов")
        
        # Проверяем конкретный рассказ
        try:
            story = Story.objects.get(id=187)
            print(f"✅ Рассказ ID=187 найден: '{story.title}'")
        except Story.DoesNotExist:
            print("⚠️ Рассказ ID=187 не существует")
            issues_found.append("Рассказ ID=187 не найден")
            
    except Exception as e:
        print(f"❌ Ошибка проверки Stories: {e}")
        issues_found.append("Ошибка при работе с моделью Stories")
    
    # Итоговый отчет
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 50)
    
    if not issues_found:
        print("🎉 Все проверки прошли успешно!")
        print("💡 Если админка все еще не работает, попробуйте:")
        print("   1. Очистить кеш браузера (Ctrl+Shift+Delete)")
        print("   2. Открыть страницу в приватном режиме")
        print("   3. Перезапустить сервер Django")
    else:
        print(f"⚠️ Найдено {len(issues_found)} проблем:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:")
        if "Проблемный middleware" in str(issues_found):
            print("   • Middleware уже отключены - перезапустите сервер")
        if "База данных недоступна" in issues_found:
            print("   • Проверьте настройки базы данных в settings.py")
        if "Нет суперпользователей" in issues_found:
            print("   • Выполните: python manage.py createsuperuser")
        if "Рассказ ID=187 не найден" in issues_found:
            print("   • Проверьте существование рассказа в админке")

if __name__ == "__main__":
    check_admin_issues()
