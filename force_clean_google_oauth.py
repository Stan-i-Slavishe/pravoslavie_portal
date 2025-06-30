#!/usr/bin/env python3
"""
Диагностика и принудительная очистка Google OAuth приложений
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site
from django.conf import settings
from decouple import config

def diagnose_and_fix():
    print("🔍 Диагностика Google OAuth приложений...\n")
    
    # Проверяем все Google приложения
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"📊 Всего Google приложений: {google_apps.count()}")
    
    for i, app in enumerate(google_apps, 1):
        print(f"   {i}. ID: {app.id}, Name: {app.name}, Client ID: {app.client_id[:20]}...")
    
    # Проверяем аккаунты
    google_accounts = SocialAccount.objects.filter(provider='google')
    print(f"📊 Всего Google аккаунтов: {google_accounts.count()}")
    
    # Проверяем токены
    google_tokens = SocialToken.objects.filter(app__provider='google')
    print(f"📊 Всего Google токенов: {google_tokens.count()}")
    
    print("\n🧹 ПОЛНАЯ ОЧИСТКА...")
    
    # Удаляем ВСЕ связанное с Google OAuth
    print("1. Удаляем токены...")
    google_tokens.delete()
    
    print("2. Удаляем аккаунты...")
    google_accounts.delete()
    
    print("3. Удаляем приложения...")
    google_apps.delete()
    
    print("✅ Все Google OAuth данные удалены")
    
    # Создаем новое чистое приложение
    print("\n🆕 Создание нового приложения...")
    
    client_id = config('GOOGLE_OAUTH2_CLIENT_ID', default='')
    secret = config('GOOGLE_OAUTH2_SECRET', default='')
    
    if not client_id or not secret:
        print("❌ Учетные данные не найдены в .env!")
        return False
    
    # Убеждаемся, что сайт существует
    site, created = Site.objects.get_or_create(
        pk=settings.SITE_ID,
        defaults={'domain': '127.0.0.1:8000', 'name': 'Разработка'}
    )
    
    print(f"📍 Сайт: {site.domain} (ID: {site.id})")
    
    # Создаем приложение
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google OAuth2 Clean',
        client_id=client_id,
        secret=secret,
    )
    
    # Привязываем к сайту
    google_app.sites.add(site)
    
    print(f"✅ Создано приложение: {google_app.name} (ID: {google_app.id})")
    print(f"✅ Client ID: {google_app.client_id}")
    print(f"✅ Secret: {google_app.secret[:10]}...")
    
    # Финальная проверка
    final_apps = SocialApp.objects.filter(provider='google')
    print(f"\n📋 Итоговое количество Google приложений: {final_apps.count()}")
    
    if final_apps.count() == 1:
        print("🎉 SUCCESS! Теперь только одно Google приложение")
        return True
    else:
        print("❌ Проблема не решена")
        return False

if __name__ == '__main__':
    try:
        success = diagnose_and_fix()
        if success:
            print("\n🚀 Теперь попробуйте:")
            print("http://127.0.0.1:8000/accounts/google/login/")
        else:
            print("\n❌ Требуется ручное вмешательство")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
