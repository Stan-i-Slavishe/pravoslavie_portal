#!/usr/bin/env python
"""
Тест исправления Google OAuth
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider

def test_google_oauth_fix():
    """Тестирует, что Google OAuth исправлен"""
    
    print("🧪 Тестирование исправления Google OAuth")
    print("=" * 50)
    
    success = True
    
    # Тест 1: Проверка сайта
    print("📍 Тест 1: Проверка сайта...")
    try:
        site = Site.objects.get(pk=1)
        print(f"   ✅ Сайт найден: {site.domain}")
    except Site.DoesNotExist:
        print("   ❌ Сайт не найден!")
        success = False
    
    # Тест 2: Проверка Google приложения
    print("\n🔐 Тест 2: Проверка Google OAuth приложения...")
    try:
        google_apps = SocialApp.objects.filter(provider=GoogleProvider.id)
        if google_apps.exists():
            google_app = google_apps.first()
            print(f"   ✅ Google приложение найдено: {google_app.name}")
            print(f"      Client ID: {google_app.client_id[:20]}...")
            
            # Проверяем привязку к сайту
            if google_app.sites.filter(pk=1).exists():
                print("   ✅ Приложение привязано к сайту")
            else:
                print("   ❌ Приложение НЕ привязано к сайту!")
                success = False
                
        else:
            print("   ❌ Google приложение не найдено!")
            success = False
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке: {e}")
        success = False
    
    # Тест 3: Симуляция запроса OAuth
    print("\n🌐 Тест 3: Симуляция обработки OAuth запроса...")
    try:
        from allauth.socialaccount.adapter import get_adapter
        from django.http import HttpRequest
        
        # Создаем фейковый запрос
        request = HttpRequest()
        request.META['HTTP_HOST'] = '127.0.0.1:8000'
        request.META['SERVER_NAME'] = '127.0.0.1'
        request.META['SERVER_PORT'] = '8000'
        
        # Пытаемся получить Google provider
        adapter = get_adapter(request)
        provider = adapter.get_provider(request, provider=GoogleProvider.id)
        
        print(f"   ✅ Google provider получен: {provider}")
        
    except Exception as e:
        print(f"   ❌ Ошибка при получении provider: {e}")
        success = False
    
    # Финальный результат
    print("\n" + "=" * 50)
    if success:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✅ Google OAuth должен работать корректно")
        print("\n🚀 Что делать дальше:")
        print("   1. Запустите Django сервер: python manage.py runserver")
        print("   2. Перейдите по ссылке: http://127.0.0.1:8000/accounts/google/login/")
        print("   3. Ошибка DoesNotExist должна исчезнуть")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ!")
        print("🛠️  Попробуйте запустить fix_google_oauth_complete.py еще раз")
    
    print("=" * 50)
    
    return success

if __name__ == "__main__":
    try:
        test_google_oauth_fix()
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
