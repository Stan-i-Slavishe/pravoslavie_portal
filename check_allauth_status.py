#!/usr/bin/env python
"""
Проверка состояния allauth в базе данных
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

def check_allauth_status():
    """Проверяет текущее состояние allauth"""
    
    print("🔍 Проверка состояния allauth...")
    print("=" * 50)
    
    # Проверяем сайты
    try:
        sites = Site.objects.all()
        print(f"📍 Сайты в базе данных:")
        for site in sites:
            print(f"   - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
        
        if not sites.exists():
            print("   ❌ Нет ни одного сайта! Нужно создать.")
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке сайтов: {e}")
    
    print()
    
    # Проверяем социальные приложения
    try:
        social_apps = SocialApp.objects.all()
        print(f"🔐 Социальные приложения:")
        
        if social_apps.exists():
            for app in social_apps:
                print(f"   - Provider: {app.provider}")
                print(f"     Name: {app.name}")
                print(f"     Client ID: {app.client_id[:20]}...")
                print(f"     Sites: {', '.join([s.domain for s in app.sites.all()])}")
                print()
        else:
            print("   ❌ Нет ни одного социального приложения!")
            print("   🎯 Это причина ошибки DoesNotExist")
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке социальных приложений: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    try:
        check_allauth_status()
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
