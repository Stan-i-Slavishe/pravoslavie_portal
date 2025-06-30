#!/usr/bin/env python3
"""
Отладка проблемы MultipleObjectsReturned
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider
from django.core.cache import cache

def debug_google_provider():
    print("🔍 Детальная отладка Google провайдера...\n")
    
    # Очищаем кеш
    print("1. Очистка кеша...")
    cache.clear()
    print("✅ Кеш очищен")
    
    # Проверяем приложения в базе
    print("\n2. Проверка базы данных:")
    all_apps = SocialApp.objects.all()
    print(f"   Всего приложений: {all_apps.count()}")
    
    for app in all_apps:
        print(f"   - ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
    
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"   Google приложений: {google_apps.count()}")
    
    # Пытаемся получить приложение как это делает allauth
    print("\n3. Тестируем получение приложения:")
    try:
        from allauth.socialaccount import app_settings
        from django.http import HttpRequest
        
        # Создаем фиктивный request
        request = HttpRequest()
        request.method = 'GET'
        
        # Создаем провайдер
        provider = GoogleProvider(request)
        print(f"   Провайдер создан: {provider}")
        
        # Пытаемся получить приложение
        app = provider.get_app(request)
        print(f"   Приложение получено: {app}")
        print(f"   App ID: {app.id}")
        print(f"   App Name: {app.name}")
        
    except Exception as e:
        print(f"   ❌ Ошибка при получении приложения: {e}")
        import traceback
        traceback.print_exc()
    
    # Проверяем настройки
    print("\n4. Проверка настроек:")
    from django.conf import settings
    
    if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
        google_settings = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
        print(f"   Google настройки: {google_settings}")
        
        app_settings = google_settings.get('APP', {})
        client_id = app_settings.get('client_id', '')
        print(f"   Client ID из настроек: {client_id[:20]}..." if client_id else "   Client ID: не задан")
    
    print("\n5. Принудительное пересоздание:")
    
    # Удаляем все и создаем заново с уникальным именем
    SocialApp.objects.filter(provider='google').delete()
    
    from decouple import config
    from django.contrib.sites.models import Site
    
    client_id = config('GOOGLE_OAUTH2_CLIENT_ID', default='')
    secret = config('GOOGLE_OAUTH2_SECRET', default='')
    
    app = SocialApp.objects.create(
        provider='google',
        name=f'Google OAuth Clean v2',  # Уникальное имя
        client_id=client_id,
        secret=secret,
    )
    
    site = Site.objects.get(pk=settings.SITE_ID)
    app.sites.add(site)
    
    print(f"   ✅ Создано новое приложение: {app.name} (ID: {app.id})")
    
    # Финальная проверка
    final_count = SocialApp.objects.filter(provider='google').count()
    print(f"   ✅ Итого Google приложений: {final_count}")

if __name__ == '__main__':
    debug_google_provider()
    print("\n🚀 Попробуйте снова: http://127.0.0.1:8000/accounts/google/login/")
