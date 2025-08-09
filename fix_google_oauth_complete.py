#!/usr/bin/env python
"""
Комплексное исправление проблемы с Google OAuth
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

def fix_google_oauth_complete():
    """Полное исправление Google OAuth"""
    
    print("🚀 Комплексное исправление Google OAuth")
    print("=" * 60)
    
    # Шаг 1: Проверка и создание сайта
    print("📍 Шаг 1: Настройка сайта...")
    
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Православный портал (Dev)'
        }
    )
    
    if created:
        print(f"   ✅ Создан новый сайт: {site.domain}")
    else:
        # Обновляем существующий сайт для разработки
        if site.domain == 'example.com':
            site.domain = '127.0.0.1:8000'
            site.name = 'Православный портал (Dev)'
            site.save()
            print(f"   ✅ Обновлен сайт: {site.domain}")
        else:
            print(f"   ✅ Сайт уже настроен: {site.domain}")
    
    # Шаг 2: Очистка старых Google приложений
    print("\n🗑️  Шаг 2: Очистка старых приложений...")
    
    old_google_apps = SocialApp.objects.filter(provider='google')
    if old_google_apps.exists():
        count = old_google_apps.count()
        old_google_apps.delete()
        print(f"   ✅ Удалено старых Google приложений: {count}")
    else:
        print("   ✅ Старых Google приложений не найдено")
    
    # Шаг 3: Создание нового тестового Google приложения
    print("\n🔐 Шаг 3: Создание Google OAuth приложения...")
    
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google OAuth (Православный портал)',
        client_id='test-google-client-id.apps.googleusercontent.com',
        secret='test-google-client-secret',
    )
    
    # Привязываем к сайту
    google_app.sites.add(site)
    
    print(f"   ✅ Создано Google приложение:")
    print(f"      Provider: {google_app.provider}")
    print(f"      Name: {google_app.name}")
    print(f"      Client ID: {google_app.client_id}")
    print(f"      Сайты: {', '.join([s.domain for s in google_app.sites.all()])}")
    
    # Шаг 4: Проверка
    print("\n🔍 Шаг 4: Финальная проверка...")
    
    all_sites = Site.objects.all()
    all_social_apps = SocialApp.objects.all()
    
    print(f"   📍 Всего сайтов: {all_sites.count()}")
    print(f"   🔐 Всего социальных приложений: {all_social_apps.count()}")
    print(f"   📍 Google приложений: {SocialApp.objects.filter(provider='google').count()}")
    
    # Шаг 5: Инструкции
    print("\n" + "=" * 60)
    print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)
    
    print(f"\n✅ Что исправлено:")
    print(f"   - Создан/настроен сайт для разработки")
    print(f"   - Удалены конфликтующие Google приложения")
    print(f"   - Создано новое тестовое Google OAuth приложение")
    print(f"   - Приложение привязано к сайту")
    
    print(f"\n🚀 Что делать дальше:")
    print(f"   1. Перезапустите Django сервер")
    print(f"   2. Попробуйте войти через Google: http://127.0.0.1:8000/accounts/google/login/")
    print(f"   3. Ошибка DoesNotExist должна исчезнуть")
    
    print(f"\n⚠️  Для реальной работы:")
    print(f"   1. Получите настоящие Google OAuth ключи:")
    print(f"      https://console.cloud.google.com/")
    print(f"   2. Замените тестовые ключи в админке:")
    print(f"      http://127.0.0.1:8000/admin/socialaccount/socialapp/")
    print(f"   3. Добавьте Authorized redirect URIs в Google Console:")
    print(f"      - http://127.0.0.1:8000/accounts/google/login/callback/")
    print(f"      - http://localhost:8000/accounts/google/login/callback/")
    
    print("\n" + "=" * 60)
    
    return google_app

if __name__ == "__main__":
    try:
        fix_google_oauth_complete()
        
    except Exception as e:
        print(f"\n❌ Ошибка при исправлении: {e}")
        import traceback
        traceback.print_exc()
        
        print(f"\n🛠️  Что можно попробовать:")
        print(f"   1. Убедитесь, что сервер Django не запущен")
        print(f"   2. Проверьте права доступа к базе данных")
        print(f"   3. Выполните: python manage.py migrate")
        print(f"   4. Попробуйте снова запустить этот скрипт")
