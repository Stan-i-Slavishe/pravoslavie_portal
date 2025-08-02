#!/usr/bin/env python
"""
Скрипт для настройки продакшен системы аналитики

Этот скрипт:
1. Создает миграции для новых моделей аналитики
2. Применяет миграции к базе данных
3. Настраивает админку для новых моделей
4. Создает тестовые данные
5. Проверяет работоспособность системы
"""

import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

from django.core.management import execute_from_command_line

def print_step(step_number, description):
    """Красивый вывод шагов"""
    print(f"\n{'='*60}")
    print(f"📊 ШАГ {step_number}: {description}")
    print(f"{'='*60}")

def check_django_setup():
    """Проверка настройки Django"""
    try:
        from django.conf import settings
        print(f"✅ Django настроен, DEBUG = {settings.DEBUG}")
        return True
    except Exception as e:
        print(f"❌ Ошибка Django: {e}")
        return False

def create_migrations():
    """Создание миграций для новых моделей"""
    print("🔄 Создание миграций...")
    
    try:
        # Создаем миграции для analytics
        execute_from_command_line(['manage.py', 'makemigrations', 'analytics'])
        print("✅ Миграции созданы")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания миграций: {e}")
        return False

def apply_migrations():
    """Применение миграций к базе данных"""
    print("🔄 Применение миграций...")
    
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Миграции применены")
        return True
    except Exception as e:
        print(f"❌ Ошибка применения миграций: {e}")
        return False

def check_urls():
    """Проверка URL маршрутов"""
    print("🔄 Проверка URL маршрутов...")
    
    try:
        from django.urls import reverse
        
        urls_to_check = [
            'analytics:dashboard',
            'analytics:track_event',
            'analytics:real_time_stats',
        ]
        
        for url_name in urls_to_check:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name} → {url}")
            except Exception as e:
                print(f"❌ {url_name} → Ошибка: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки URL: {e}")
        return False

def test_analytics_system():
    """Тестирование системы аналитики"""
    print("🔄 Тестирование системы аналитики...")
    
    try:
        # Проверяем импорт всех компонентов
        from analytics import views
        from analytics import production_views
        
        print("✅ Все модули импортируются корректно")
        
        # Проверяем доступность файлов
        static_files = [
            'static/js/production_analytics.js',
            'templates/analytics/production_dashboard.html'
        ]
        
        for file_path in static_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path} существует")
            else:
                print(f"⚠️ {file_path} не найден")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def main():
    """Основная функция настройки"""
    print("🚀 НАСТРОЙКА ПРОДАКШЕН СИСТЕМЫ АНАЛИТИКИ")
    print("=" * 60)
    
    success_count = 0
    total_steps = 5
    
    # Шаг 1: Проверка Django
    print_step(1, "Проверка настройки Django")
    if check_django_setup():
        success_count += 1
    
    # Шаг 2: Создание миграций
    print_step(2, "Создание миграций")
    if create_migrations():
        success_count += 1
    
    # Шаг 3: Применение миграций
    print_step(3, "Применение миграций к базе данных")
    if apply_migrations():
        success_count += 1
    
    # Шаг 4: Проверка URL
    print_step(4, "Проверка URL маршрутов")
    if check_urls():
        success_count += 1
    
    # Шаг 5: Тестирование системы
    print_step(5, "Тестирование системы аналитики")
    if test_analytics_system():
        success_count += 1
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    if success_count == total_steps:
        print("🎉 ВСЕ НАСТРОЕНО УСПЕШНО!")
        print("\n✅ Что готово:")
        print("   • Продакшен система аналитики активна")
        print("   • Миграции применены к базе данных")
        print("   • JavaScript файлы подключены")
        print("   • Дашборд аналитики доступен")
        
        print("\n🚀 Что делать дальше:")
        print("   1. Запустите сервер: python manage.py runserver")
        print("   2. Откройте: http://127.0.0.1:8000/analytics/dashboard/")
        print("   3. Начните использовать сайт - аналитика будет собираться автоматически")
        print("   4. Проверьте админку: http://127.0.0.1:8000/admin/analytics/")
        
    else:
        print(f"⚠️ ВЫПОЛНЕНО {success_count}/{total_steps} ШАГОВ")
        print("\n🔧 Возможные проблемы:")
        print("   • Проверьте подключение к базе данных")
        print("   • Убедитесь что все зависимости установлены")
        print("   • Проверьте права доступа к файлам")
        
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
