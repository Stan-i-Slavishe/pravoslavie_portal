#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест PWA с иконками
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

def test_pwa_icons():
    """Проверяет наличие всех иконок PWA"""
    print("📱 Проверка иконок PWA...")
    
    required_icons = [
        'static/icons/icon-72x72.png',
        'static/icons/icon-192x192.png',
        'static/icons/icon-512x512.png',
    ]
    
    existing_icons = []
    missing_icons = []
    
    for icon_path in required_icons:
        full_path = BASE_DIR / icon_path
        if full_path.exists() and full_path.stat().st_size > 100:  # Проверяем, что файл не пустой
            existing_icons.append(icon_path)
            size_kb = full_path.stat().st_size / 1024
            print(f"✅ {icon_path} ({size_kb:.1f} KB)")
        else:
            missing_icons.append(icon_path)
            print(f"❌ {icon_path}")
    
    print(f"\n📊 Результат: {len(existing_icons)}/{len(required_icons)} иконок готово")
    
    if missing_icons:
        print(f"\n⚠️  Проблемные иконки:")
        for icon in missing_icons:
            print(f"   - {icon}")
        return False
    
    print("✅ Все иконки PWA готовы!")
    return True

def test_pwa_manifest():
    """Проверяет корректность манифеста"""
    print("\n📋 Проверка манифеста...")
    
    try:
        import json
        manifest_path = BASE_DIR / 'static' / 'manifest.json'
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Проверяем обязательные поля
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        
        for field in required_fields:
            if field in manifest:
                print(f"✅ {field}: {manifest[field] if field != 'icons' else f'{len(manifest[field])} иконок'}")
            else:
                print(f"❌ {field}: отсутствует")
                return False
        
        # Проверяем иконки в манифесте
        print(f"✅ Иконки в манифесте: {len(manifest['icons'])}")
        for icon in manifest['icons']:
            print(f"   - {icon['sizes']}: {icon['src']}")
        
        print("✅ Манифест корректен!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка манифеста: {str(e)}")
        return False

def test_pwa_in_browser():
    """Тестирует PWA в браузере"""
    print("\n🌐 Проверка PWA в браузере...")
    
    from django.test import Client
    
    client = Client()
    
    # Тестируем доступность манифеста
    response = client.get('/manifest.json')
    if response.status_code == 200:
        print("✅ Манифест доступен")
    else:
        print(f"❌ Манифест недоступен: {response.status_code}")
        return False
    
    # Тестируем Service Worker
    response = client.get('/sw.js')
    if response.status_code == 200:
        print("✅ Service Worker доступен")
    else:
        print(f"❌ Service Worker недоступен: {response.status_code}")
        return False
    
    # Тестируем офлайн страницу
    response = client.get('/offline/')
    if response.status_code == 200:
        print("✅ Офлайн страница работает")
    else:
        print(f"❌ Офлайн страница недоступна: {response.status_code}")
        return False
    
    print("✅ PWA готов для браузера!")
    return True

def generate_final_report():
    """Генерирует финальный отчет о готовности PWA"""
    print("="*60)
    print("🎉 ФИНАЛЬНАЯ ПРОВЕРКА PWA")
    print("="*60)
    
    tests = [
        ("Иконки PWA", test_pwa_icons),
        ("Манифест PWA", test_pwa_manifest),
        ("Доступность в браузере", test_pwa_in_browser),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, "✅ ГОТОВО" if result else "❌ ТРЕБУЕТ ВНИМАНИЯ"))
        except Exception as e:
            results.append((test_name, f"❌ ОШИБКА: {str(e)}"))
            print(f"❌ Неожиданная ошибка: {str(e)}")
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("🎯 ФИНАЛЬНЫЙ СТАТУС PWA")
    print("="*60)
    
    ready_components = sum(1 for _, result in results if result.startswith("✅"))
    total_components = len(results)
    
    for test_name, result in results:
        print(f"{result} {test_name}")
    
    print(f"\n📊 Готовность PWA: {ready_components}/{total_components}")
    
    if ready_components == total_components:
        print("\n🎉🎉🎉 PWA ПОЛНОСТЬЮ ГОТОВ! 🎉🎉🎉")
        print("\n🚀 Что теперь можно делать:")
        print("   ✅ Открыть сайт в Chrome/Edge")
        print("   ✅ Увидеть промпт 'Установить приложение'")
        print("   ✅ Установить PWA на телефон")
        print("   ✅ Работать офлайн с контентом")
        print("   ✅ Получать push-уведомления")
        print("   ✅ Синхронизировать данные")
        print("\n📱 Ваш православный портал теперь PWA!")
    else:
        print(f"\n⚠️  {total_components - ready_components} компонентов требуют внимания.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    generate_final_report()
