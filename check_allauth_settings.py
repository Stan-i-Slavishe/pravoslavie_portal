#!/usr/bin/env python
"""
Проверка настроек allauth в settings.py
"""
import os
import sys

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    
    from django.conf import settings
    
    def check_allauth_settings():
        """Проверяет настройки allauth"""
        
        print("🔍 Проверка настроек allauth")
        print("=" * 50)
        
        # Проверяем INSTALLED_APPS
        print("📦 INSTALLED_APPS:")
        allauth_apps = [app for app in settings.INSTALLED_APPS if 'allauth' in app]
        
        if allauth_apps:
            for app in allauth_apps:
                print(f"   ✅ {app}")
        else:
            print("   ❌ Allauth приложения не найдены!")
        
        # Проверяем AUTHENTICATION_BACKENDS
        print(f"\n🔐 AUTHENTICATION_BACKENDS:")
        if hasattr(settings, 'AUTHENTICATION_BACKENDS'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                print(f"   ✅ {backend}")
        else:
            print("   ❌ AUTHENTICATION_BACKENDS не настроен!")
        
        # Проверяем SITE_ID
        print(f"\n📍 SITE_ID: {getattr(settings, 'SITE_ID', 'НЕ УСТАНОВЛЕН')}")
        
        # Проверяем основные настройки allauth
        allauth_settings = [
            'LOGIN_REDIRECT_URL',
            'LOGOUT_REDIRECT_URL',
            'ACCOUNT_EMAIL_VERIFICATION',
            'SOCIALACCOUNT_AUTO_SIGNUP',
        ]
        
        print(f"\n⚙️  Настройки allauth:")
        for setting_name in allauth_settings:
            value = getattr(settings, setting_name, 'НЕ УСТАНОВЛЕН')
            print(f"   {setting_name}: {value}")
        
        # Проверяем middleware
        print(f"\n🛡️  Middleware:")
        allauth_middleware = [m for m in settings.MIDDLEWARE if 'allauth' in m]
        if allauth_middleware:
            for middleware in allauth_middleware:
                print(f"   ✅ {middleware}")
        else:
            print("   ❌ Allauth middleware не найден!")
        
        # Проверяем django.contrib.sites
        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            print("   ✅ django.contrib.sites включен")
        else:
            print("   ❌ django.contrib.sites НЕ включен!")
        
        print("\n" + "=" * 50)
        
        # Рекомендации
        if 'allauth' not in str(settings.INSTALLED_APPS):
            print("❌ ПРОБЛЕМА: allauth не установлен в INSTALLED_APPS")
        elif not hasattr(settings, 'AUTHENTICATION_BACKENDS'):
            print("❌ ПРОБЛЕМА: AUTHENTICATION_BACKENDS не настроен")
        elif not hasattr(settings, 'SITE_ID'):
            print("❌ ПРОБЛЕМА: SITE_ID не установлен")
        else:
            print("✅ Основные настройки allauth выглядят корректно")
            print("🎯 Если есть ошибка DoesNotExist - проблема в базе данных")
    
    check_allauth_settings()
    
except Exception as e:
    print(f"❌ Ошибка при проверке настроек: {e}")
    import traceback
    traceback.print_exc()
