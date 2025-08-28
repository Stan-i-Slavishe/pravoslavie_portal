#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования PWA функциональности
Православный портал - Добрые истории
"""

import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_pwa_files():
    """Проверяет наличие всех необходимых PWA файлов"""
    print("🔍 Проверка PWA файлов...")
    
    required_files = [
        'static/manifest.json',
        'static/sw.js', 
        'static/js/pwa.js',
        'static/browserconfig.xml',
        'templates/offline/offline.html',
        'pwa/models.py',
        'pwa/views.py',
        'pwa/urls.py',
        'pwa/admin.py',
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 Результат: {len(existing_files)}/{len(required_files)} файлов найдено")
    
    if missing_files:
        print(f"\n⚠️  Отсутствующие файлы:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Все PWA файлы на месте!")
    return True

def test_pwa_urls():
    """Проверяет доступность PWA URL маршрутов"""
    print("\n🌐 Проверка PWA URL маршрутов...")
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    pwa_urls = [
        ('pwa:manifest', 'manifest.json'),
        ('pwa:service_worker', 'sw.js'),
        ('pwa:offline', 'offline/'),
        ('pwa:get_csrf_token', 'get-csrf-token/'),
        ('pwa:ping', 'ping/'),
    ]
    
    working_urls = []
    broken_urls = []
    
    for url_name, url_path in pwa_urls:
        try:
            url = reverse(url_name)
            response = client.get(url)
            
            if response.status_code == 200:
                working_urls.append((url_name, url_path, response.status_code))
                print(f"✅ {url_path} → {response.status_code}")
            else:
                broken_urls.append((url_name, url_path, response.status_code))
                print(f"⚠️  {url_path} → {response.status_code}")
                
        except Exception as e:
            broken_urls.append((url_name, url_path, str(e)))
            print(f"❌ {url_path} → {str(e)}")
    
    print(f"\n📊 Результат: {len(working_urls)}/{len(pwa_urls)} URL работают")
    
    if broken_urls:
        print(f"\n⚠️  Проблемные URL:")
        for url_name, url_path, error in broken_urls:
            print(f"   - {url_path}: {error}")
        return False
    
    print("✅ Все PWA URL работают!")
    return True

def test_pwa_settings():
    """Проверяет настройки Django для PWA"""
    print("\n⚙️  Проверка настроек Django...")
    
    from django.conf import settings
    
    checks = [
        ('pwa в INSTALLED_APPS', 'pwa' in settings.INSTALLED_APPS),
        ('STATIC_URL настроен', hasattr(settings, 'STATIC_URL')),
        ('STATIC_ROOT настроен', hasattr(settings, 'STATIC_ROOT')),
        ('TEMPLATES настроены', hasattr(settings, 'TEMPLATES')),
    ]
    
    passed_checks = []
    failed_checks = []
    
    for check_name, check_result in checks:
        if check_result:
            passed_checks.append(check_name)
            print(f"✅ {check_name}")
        else:
            failed_checks.append(check_name)
            print(f"❌ {check_name}")
    
    print(f"\n📊 Результат: {len(passed_checks)}/{len(checks)} проверок пройдено")
    
    if failed_checks:
        print(f"\n⚠️  Неудачные проверки:")
        for check in failed_checks:
            print(f"   - {check}")
        return False
    
    print("✅ Все настройки Django корректны!")
    return True

def test_pwa_models():
    """Проверяет модели PWA"""
    print("\n🗄️  Проверка моделей PWA...")
    
    try:
        from pwa.models import PushSubscription, PWAInstallEvent, OfflineAction, PWAAnalytics, CachedContent
        
        models = [
            ('PushSubscription', PushSubscription),
            ('PWAInstallEvent', PWAInstallEvent), 
            ('OfflineAction', OfflineAction),
            ('PWAAnalytics', PWAAnalytics),
            ('CachedContent', CachedContent),
        ]
        
        for model_name, model_class in models:
            try:
                # Проверяем, что модель может выполнить базовые операции
                model_class.objects.all().count()
                print(f"✅ {model_name}")
            except Exception as e:
                print(f"❌ {model_name}: {str(e)}")
                return False
        
        print("✅ Все модели PWA работают!")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта моделей: {str(e)}")
        return False

def generate_test_report():
    """Генерирует полный отчет о тестировании PWA"""
    print("="*60)
    print("🚀 ТЕСТИРОВАНИЕ PWA - ПРАВОСЛАВНЫЙ ПОРТАЛ")
    print("="*60)
    
    tests = [
        ("PWA файлы", test_pwa_files),
        ("PWA URL маршруты", test_pwa_urls),
        ("Django настройки", test_pwa_settings),
        ("PWA модели", test_pwa_models),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"))
        except Exception as e:
            results.append((test_name, f"❌ ОШИБКА: {str(e)}"))
            print(f"❌ Неожиданная ошибка: {str(e)}")
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ PWA")
    print("="*60)
    
    passed_tests = sum(1 for _, result in results if result.startswith("✅"))
    total_tests = len(results)
    
    for test_name, result in results:
        print(f"{result} {test_name}")
    
    print(f"\n🎯 Результат: {passed_tests}/{total_tests} тестов пройдено")
    
    if passed_tests == total_tests:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! PWA готов к работе!")
        print("\n📋 Следующие шаги:")
        print("   1. Создать иконки PWA (72x72, 192x192, 512x512)")
        print("   2. Выполнить миграции: python manage.py migrate pwa")
        print("   3. Протестировать в браузере Chrome/Edge")
        print("   4. Проверить установку PWA на мобильном")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} тестов провалено. Требуется доработка.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    generate_test_report()
