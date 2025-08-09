#!/usr/bin/env python
"""
Быстрое исправление: создание Google OAuth приложения
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

def quick_fix_google_oauth():
    """Быстро создает Google OAuth приложение для тестирования"""
    
    print("🚀 Быстрое исправление Google OAuth...")
    
    # Получаем или создаем сайт
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Православный портал (разработка)'
        }
    )
    
    if created:
        print(f"✅ Создан новый сайт: {site.domain}")
    else:
        print(f"✅ Используется сайт: {site.domain}")
    
    # Удаляем старые Google приложения если есть
    old_apps = SocialApp.objects.filter(provider='google')
    if old_apps.exists():
        old_apps.delete()
        print("🗑️  Удалены старые Google приложения")
    
    # Создаем новое тестовое Google приложение
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google OAuth (Тестовое)',
        client_id='test-client-id.apps.googleusercontent.com',
        secret='test-client-secret',
    )
    
    # Привязываем к сайту
    google_app.sites.add(site)
    
    print(f"✅ Создано тестовое Google OAuth приложение:")
    print(f"   - Provider: {google_app.provider}")
    print(f"   - Name: {google_app.name}")
    print(f"   - Client ID: {google_app.client_id}")
    print(f"   - Sites: {', '.join([s.domain for s in google_app.sites.all()])}")
    
    print(f"\n🎯 Теперь ошибка DoesNotExist должна исчезнуть!")
    print(f"📝 Для реальной работы замените тестовые ключи в админке:")
    print(f"   http://127.0.0.1:8000/admin/socialaccount/socialapp/")
    
    print(f"\n📋 Инструкция для получения реальных ключей:")
    print(f"1. Перейдите в Google Cloud Console: https://console.cloud.google.com/")
    print(f"2. Создайте проект или выберите существующий")
    print(f"3. Включите Google+ API или Google Sign-In API")
    print(f"4. Создайте OAuth 2.0 учетные данные")
    print(f"5. Добавьте Authorized redirect URIs:")
    print(f"   - http://127.0.0.1:8000/accounts/google/login/callback/")
    print(f"   - http://localhost:8000/accounts/google/login/callback/")
    
    return google_app

if __name__ == "__main__":
    try:
        app = quick_fix_google_oauth()
        print(f"\n🎉 Исправление завершено! Попробуйте снова войти через Google.")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
