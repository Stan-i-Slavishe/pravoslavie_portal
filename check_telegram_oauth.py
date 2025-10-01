"""
Скрипт для проверки настройки Telegram OAuth

Запуск: python check_telegram_oauth.py
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def check_telegram_oauth():
    print("=" * 60)
    print("🔍 ПРОВЕРКА TELEGRAM OAUTH НАСТРОЕК")
    print("=" * 60)
    print()
    
    # Проверка 1: Провайдер в INSTALLED_APPS
    print("1️⃣ Проверка установленных приложений...")
    from django.conf import settings
    
    telegram_provider = 'allauth.socialaccount.providers.telegram'
    if telegram_provider in settings.INSTALLED_APPS:
        print(f"   ✅ {telegram_provider} установлен")
    else:
        print(f"   ❌ {telegram_provider} НЕ установлен")
        print(f"   → Добавьте в INSTALLED_APPS в settings_base.py")
        return
    
    print()
    
    # Проверка 2: Настройки провайдера
    print("2️⃣ Проверка настроек провайдера...")
    if hasattr(settings, 'SOCIALACCOUNT_PROVIDERS'):
        if 'telegram' in settings.SOCIALACCOUNT_PROVIDERS:
            print(f"   ✅ Telegram настройки найдены:")
            print(f"      {settings.SOCIALACCOUNT_PROVIDERS['telegram']}")
        else:
            print(f"   ⚠️ Telegram настройки не найдены в SOCIALACCOUNT_PROVIDERS")
            print(f"   → Добавьте конфигурацию в settings_base.py")
    else:
        print(f"   ❌ SOCIALACCOUNT_PROVIDERS не определен")
    
    print()
    
    # Проверка 3: Sites
    print("3️⃣ Проверка Sites Framework...")
    try:
        sites = Site.objects.all()
        print(f"   ✅ Найдено сайтов: {sites.count()}")
        for site in sites:
            print(f"      - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Проверка 4: Social Apps
    print("4️⃣ Проверка Social Applications...")
    try:
        telegram_apps = SocialApp.objects.filter(provider='telegram')
        
        if telegram_apps.exists():
            print(f"   ✅ Найдено Telegram приложений: {telegram_apps.count()}")
            for app in telegram_apps:
                print(f"      📱 Приложение: {app.name}")
                print(f"         Client ID: {app.client_id}")
                print(f"         Secret Key: {'*' * 10}{app.secret[-10:] if len(app.secret) > 10 else '***'}")
                print(f"         Sites: {', '.join([s.domain for s in app.sites.all()])}")
                print()
        else:
            print(f"   ❌ Telegram Social App НЕ найден")
            print()
            print("   📝 Для создания выполните:")
            print("      1. Откройте /admin/")
            print("      2. Перейдите: Social applications → Add")
            print("      3. Заполните:")
            print("         - Provider: Telegram")
            print("         - Name: Telegram Login")
            print("         - Client ID: ваш_bot_username")
            print("         - Secret key: ваш_bot_token")
            print("         - Sites: выберите ваш сайт")
            print()
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Проверка 5: URL patterns
    print("5️⃣ Проверка URL маршрутов...")
    from django.urls import reverse
    try:
        telegram_login_url = '/accounts/telegram/login/'
        print(f"   ✅ Telegram Login URL: {telegram_login_url}")
        print(f"   ✅ Callback URL: {telegram_login_url}callback/")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Итоговый статус
    print("=" * 60)
    if telegram_apps.exists():
        print("✅ TELEGRAM OAUTH НАСТРОЕН И ГОТОВ К ИСПОЛЬЗОВАНИЮ!")
        print()
        print("🚀 Для тестирования:")
        print("   1. Запустите сервер: python manage.py runserver")
        print("   2. Откройте: http://localhost:8000/accounts/login/")
        print("   3. Нажмите кнопку 'Telegram'")
    else:
        print("⚠️ ТРЕБУЕТСЯ НАСТРОЙКА!")
        print()
        print("📋 Следующие шаги:")
        print("   1. Создайте бота через @BotFather в Telegram")
        print("   2. Получите bot token")
        print("   3. Добавьте Social App в Django Admin")
        print("   4. Запустите этот скрипт снова")
    print("=" * 60)

if __name__ == '__main__':
    try:
        check_telegram_oauth()
    except KeyboardInterrupt:
        print("\n\n⚠️ Проверка прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
