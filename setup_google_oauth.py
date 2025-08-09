#!/usr/bin/env python
"""
Скрипт для настройки Google OAuth в Django Allauth
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

def setup_google_oauth():
    """Настраивает Google OAuth приложение"""
    
    print("🚀 Настройка Google OAuth...")
    
    # Получаем или создаем сайт
    try:
        site = Site.objects.get(pk=1)
        print(f"✅ Найден сайт: {site.domain}")
    except Site.DoesNotExist:
        site = Site.objects.create(
            pk=1,
            domain='127.0.0.1:8000',
            name='Православный портал (разработка)'
        )
        print(f"✅ Создан новый сайт: {site.domain}")
    
    # Проверяем существующее Google приложение
    google_apps = SocialApp.objects.filter(provider=GoogleProvider.id)
    
    if google_apps.exists():
        print("⚠️  Google OAuth приложение уже существует:")
        for app in google_apps:
            print(f"   - {app.name} (ID: {app.client_id[:10]}...)")
            print(f"   - Сайты: {', '.join([s.domain for s in app.sites.all()])}")
        
        choice = input("\n🤔 Хотите пересоздать Google приложение? (y/N): ").lower()
        if choice == 'y':
            google_apps.delete()
            print("🗑️  Старые Google приложения удалены")
        else:
            print("⏭️  Пропускаем создание Google приложения")
            return
    
    # Создаем новое Google приложение
    print("\n📝 Создание нового Google OAuth приложения...")
    print("=" * 50)
    
    # Тестовые данные для разработки
    client_id = "your-google-client-id.apps.googleusercontent.com"
    client_secret = "your-google-client-secret"
    
    print(f"""
🔑 Для настройки Google OAuth вам нужно:

1. Перейти в Google Cloud Console: https://console.cloud.google.com/
2. Создать новый проект или выбрать существующий
3. Включить Google+ API
4. Создать OAuth 2.0 учетные данные
5. Добавить redirect URI: http://127.0.0.1:8000/accounts/google/login/callback/

📋 Текущие redirect URI для разработки:
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:8000/accounts/google/login/callback/
   - https://127.0.0.1:8000/accounts/google/login/callback/
   - https://localhost:8000/accounts/google/login/callback/
""")
    
    print("\n" + "=" * 50)
    
    # Запрашиваем реальные данные от пользователя
    user_client_id = input(f"🔑 Введите Google Client ID (или Enter для тестового): ").strip()
    if user_client_id:
        client_id = user_client_id
    
    user_client_secret = input(f"🔐 Введите Google Client Secret (или Enter для тестового): ").strip()
    if user_client_secret:
        client_secret = user_client_secret
    
    # Создаем приложение
    google_app = SocialApp.objects.create(
        provider=GoogleProvider.id,
        name="Google OAuth (Православный портал)",
        client_id=client_id,
        secret=client_secret,
    )
    
    # Привязываем к сайту
    google_app.sites.add(site)
    
    print(f"\n✅ Google OAuth приложение создано:")
    print(f"   - Provider: {google_app.provider}")
    print(f"   - Name: {google_app.name}")
    print(f"   - Client ID: {google_app.client_id[:20]}...")
    print(f"   - Sites: {', '.join([s.domain for s in google_app.sites.all()])}")
    
    print(f"\n🌐 Теперь вы можете войти через Google:")
    print(f"   http://127.0.0.1:8000/accounts/google/login/")
    
    if client_id.startswith("your-google-"):
        print(f"\n⚠️  ВНИМАНИЕ: Используются тестовые ключи!")
        print(f"   Для реальной работы замените их на настоящие в админке:")
        print(f"   http://127.0.0.1:8000/admin/socialaccount/socialapp/")

def main():
    """Главная функция"""
    try:
        setup_google_oauth()
        print(f"\n🎉 Настройка Google OAuth завершена!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при настройке: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
