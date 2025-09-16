#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Тест системы мониторинга
Создан автоматически для проверки интеграции
"""

import os
import sys
import django
import requests
import time

# Добавляем путь к проекту
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_health_checks():
    """Тестирование health check endpoints"""
    print("🏥 Тестирование health checks...")
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/health/simple/",
        "/health/detailed/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {endpoint} - {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ {endpoint} - Ошибка: {e}")

def test_monitoring_dashboard():
    """Тестирование dashboard мониторинга"""
    print("📊 Тестирование dashboard мониторинга...")
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/admin/monitoring/dashboard/",
        "/admin/monitoring/api/system/",
        "/admin/monitoring/api/database/",
        "/admin/monitoring/api/cache/",
        "/admin/monitoring/api/application/",
        "/admin/monitoring/api/logs/",
        "/admin/monitoring/api/alerts/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if endpoint.endswith('dashboard/'):
                # Dashboard требует авторизации
                status = "✅" if response.status_code in [200, 302, 403] else "❌"
            else:
                # API endpoints тоже требуют авторизации
                status = "✅" if response.status_code in [200, 403] else "❌"
            print(f"   {status} {endpoint} - {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ {endpoint} - Ошибка: {e}")

def test_middleware():
    """Тестирование middleware мониторинга"""
    print("🔧 Тестирование middleware...")
    
    try:
        from core.middleware.monitoring import PerformanceMonitoringMiddleware
        print("   ✅ PerformanceMonitoringMiddleware импортирован")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта PerformanceMonitoringMiddleware: {e}")
    
    try:
        from core.middleware.monitoring import SecurityMonitoringMiddleware
        print("   ✅ SecurityMonitoringMiddleware импортирован")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта SecurityMonitoringMiddleware: {e}")

def test_management_commands():
    """Тестирование Django команд"""
    print("⚙️ Тестирование management команд...")
    
    commands = [
        "monitor_system",
        "cleanup_logs", 
        "monitoring_report"
    ]
    
    for cmd in commands:
        try:
            from django.core.management import get_commands
            available_commands = get_commands()
            if cmd in available_commands:
                print(f"   ✅ Команда {cmd} доступна")
            else:
                print(f"   ❌ Команда {cmd} не найдена")
        except Exception as e:
            print(f"   ❌ Ошибка проверки команды {cmd}: {e}")

def test_cache_monitoring():
    """Тестирование мониторинга кеша"""
    print("🔄 Тестирование мониторинга кеша...")
    
    try:
        from django.core.cache import cache
        
        # Тест записи/чтения
        test_key = 'monitoring_test'
        test_value = 'test_value_123'
        
        cache.set(test_key, test_value, 60)
        retrieved = cache.get(test_key)
        
        if retrieved == test_value:
            print("   ✅ Кеш работает корректно")
        else:
            print("   ❌ Кеш не работает")
            
    except Exception as e:
        print(f"   ❌ Ошибка тестирования кеша: {e}")

def test_database_monitoring():
    """Тестирование мониторинга БД"""
    print("🗄️ Тестирование мониторинга БД...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            
        if result and result[0] == 1:
            print("   ✅ База данных доступна")
        else:
            print("   ❌ База данных не отвечает")
            
    except Exception as e:
        print(f"   ❌ Ошибка подключения к БД: {e}")

def test_psutil():
    """Тестирование psutil для системных метрик"""
    print("💻 Тестирование psutil...")
    
    try:
        import psutil
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent if os.name == 'posix' else psutil.disk_usage('C:').percent
        
        print(f"   ✅ CPU: {cpu}%")
        print(f"   ✅ Память: {memory}%") 
        print(f"   ✅ Диск: {disk:.1f}%")
        
    except ImportError:
        print("   ❌ psutil не установлен. Выполните: pip install psutil")
    except Exception as e:
        print(f"   ❌ Ошибка psutil: {e}")

def test_directories():
    """Проверка создания директорий"""
    print("📁 Проверка директорий...")
    
    directories = [
        "logs",
        "scripts", 
        "templates/admin/monitoring"
    ]
    
    for dir_name in directories:
        dir_path = os.path.join(project_path, dir_name)
        if os.path.exists(dir_path):
            print(f"   ✅ Директория {dir_name} существует")
        else:
            print(f"   ❌ Директория {dir_name} не найдена")

def test_files():
    """Проверка созданных файлов"""
    print("📄 Проверка файлов...")
    
    files = [
        "config/monitoring_settings.py",
        "core/middleware/monitoring.py",
        "core/monitoring_views.py",
        "core/management/commands/monitor_system.py",
        "core/management/commands/cleanup_logs.py",
        "core/management/commands/monitoring_report.py",
        "templates/admin/monitoring/dashboard.html",
        "scripts/monitoring_check.sh",
        "scripts/monitoring_check.bat"
    ]
    
    for file_name in files:
        file_path = os.path.join(project_path, file_name)
        if os.path.exists(file_path):
            print(f"   ✅ Файл {file_name} создан")
        else:
            print(f"   ❌ Файл {file_name} не найден")

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТ СИСТЕМЫ МОНИТОРИНГА ПРАВОСЛАВНОГО ПОРТАЛА")
    print("=" * 60)
    
    test_directories()
    print()
    
    test_files()
    print()
    
    test_psutil()
    print()
    
    test_middleware()
    print()
    
    test_management_commands()
    print()
    
    test_database_monitoring()
    print()
    
    test_cache_monitoring()
    print()
    
    # Эти тесты требуют запущенного сервера
    print("⚠️ Следующие тесты требуют запущенного Django сервера:")
    print("   Запустите: python manage.py runserver")
    print("   Затем выполните: python scripts/test_monitoring.py --server-tests")
    
    if '--server-tests' in sys.argv:
        print()
        test_health_checks()
        print()
        
        test_monitoring_dashboard()
    
    print()
    print("🎉 Тестирование завершено!")
    print("📚 Для полного тестирования:")
    print("   1. Запустите сервер: python manage.py runserver")
    print("   2. Откройте: http://localhost:8000/admin/monitoring/dashboard/")
    print("   3. Войдите как администратор")

if __name__ == "__main__":
    main()
