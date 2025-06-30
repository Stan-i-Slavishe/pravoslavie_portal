#!/usr/bin/env python3
"""
Скрипт для тестирования Google OAuth настроек
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('/path/to/your/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def check_google_oauth_setup():
    print("🔍 Проверка настроек Google OAuth...")
    
    # Проверяем настройки
    print(f"✅ Google провайдер в SOCIALACCOUNT_PROVIDERS: {'google' in settings.SOCIALACCOUNT_PROVIDERS}")
    print(f"✅ SITE_ID: {settings.SITE_ID}")
    
    # Проверяем сайт
    try:
        site = Site.objects.get(pk=settings.SITE_ID)
        print(f"✅ Сайт: {site.domain} ({site.name})")
    except Site.DoesNotExist:
        print("❌ Сайт не найден! Создаем...")
        site = Site.objects.create(
            pk=settings.SITE_ID,
            domain='127.0.0.1:8000',
            name='Православие Портал (Разработка)'
        )
        print(f"✅ Создан сайт: {site.domain}")
    
    # Проверяем Google приложение
    try:
        google_app = SocialApp.objects.get(provider='google')
        print(f"✅ Google приложение найдено: {google_app.name}")
        print(f"   Client ID: {google_app.client_id[:10]}..." if google_app.client_id else "   ❌ Client ID не задан")
        print(f"   Secret: {'✅ Задан' if google_app.secret else '❌ Не задан'}")
        
        # Проверяем привязку к сайту
        if site in google_app.sites.all():
            print("✅ Приложение привязано к сайту")
        else:
            print("❌ Приложение НЕ привязано к сайту! Исправляем...")
            google_app.sites.add(site)
            print("✅ Приложение привязано к сайту")
            
    except SocialApp.DoesNotExist:
        print("❌ Google приложение не найдено!")
        print("💡 Создайте приложение вручную через админку или выполните:")
        print("   python manage.py shell")
        print("   >>> from setup_google_oauth import create_google_app")
        print("   >>> create_google_app('YOUR_CLIENT_ID', 'YOUR_SECRET')")

def create_google_app(client_id, secret):
    """Создает Google OAuth приложение"""
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    
    # Создаем или обновляем приложение
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth2',
            'client_id': client_id,
            'secret': secret,
        }
    )
    
    if not created:
        google_app.client_id = client_id
        google_app.secret = secret
        google_app.save()
        print("🔄 Google приложение обновлено")
    else:
        print("✅ Google приложение создано")
    
    # Привязываем к сайту
    site = Site.objects.get(pk=settings.SITE_ID)
    google_app.sites.add(site)
    print(f"✅ Приложение привязано к сайту {site.domain}")
    
    return google_app

def setup_local_site():
    """Настраивает локальный сайт для разработки"""
    from django.contrib.sites.models import Site
    
    site, created = Site.objects.get_or_create(
        pk=settings.SITE_ID,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Православие Портал (Разработка)'
        }
    )
    
    if not created and site.domain != '127.0.0.1:8000':
        site.domain = '127.0.0.1:8000'
        site.name = 'Православие Портал (Разработка)'
        site.save()
        print("🔄 Сайт обновлен для локальной разработки")
    
    return site

if __name__ == '__main__':
    print("🚀 Настройка Google OAuth для разработки\n")
    
    # Настраиваем сайт
    setup_local_site()
    
    # Проверяем настройки
    check_google_oauth_setup()
    
    print("\n📋 Следующие шаги:")
    print("1. Создайте приложение в Google Cloud Console")
    print("2. Получите Client ID и Secret")
    print("3. Добавьте их в .env файл:")
    print("   GOOGLE_OAUTH2_CLIENT_ID=ваш_client_id")
    print("   GOOGLE_OAUTH2_SECRET=ваш_secret")
    print("4. Выполните миграции: python manage.py migrate")
    print("5. Запустите: python setup_google_oauth.py")
