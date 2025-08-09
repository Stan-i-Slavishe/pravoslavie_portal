#!/usr/bin/env python
"""
Обновление Google OAuth ключей реальными данными
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

def update_google_oauth_keys():
    """Обновляет Google OAuth ключи реальными данными"""
    
    print("🔑 Обновление Google OAuth ключей")
    print("=" * 50)
    
    # Реальные ключи из Google Cloud Console
    real_client_id = "616741227224-o6rc2o68tb3lb7scjb2pcpr6mo4jq7vm.apps.googleusercontent.com"
    real_client_secret = "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"
    
    try:
        # Находим Google OAuth приложение
        google_app = SocialApp.objects.get(provider='google')
        
        print(f"📋 Найдено Google приложение:")
        print(f"   Название: {google_app.name}")
        print(f"   Старый Client ID: {google_app.client_id}")
        print(f"   Старый Secret: {google_app.secret[:10]}...")
        
        # Обновляем ключи
        google_app.client_id = real_client_id
        google_app.secret = real_client_secret
        google_app.name = "Google OAuth (Добрые истории)"  # Обновляем название под проект
        google_app.save()
        
        print(f"\n✅ Ключи успешно обновлены!")
        print(f"   Новый Client ID: {google_app.client_id}")
        print(f"   Новый Secret: {google_app.secret[:15]}...")
        print(f"   Название: {google_app.name}")
        
        # Проверяем привязку к сайтам
        sites = google_app.sites.all()
        print(f"\n📍 Привязанные сайты:")
        for site in sites:
            print(f"   - {site.domain}")
        
        print(f"\n🎉 Google OAuth готов к работе с настоящими ключами!")
        print(f"📋 Настроенные redirect URIs в Google Console:")
        print(f"   - http://127.0.0.1:8000/accounts/google/login/callback/")
        print(f"   - http://localhost:8000/accounts/google/login/callback/")
        
        print(f"\n🚀 Теперь можно полноценно входить через Google!")
        
    except SocialApp.DoesNotExist:
        print("❌ Google OAuth приложение не найдено!")
        print("🛠️  Сначала запустите: master_fix_google_oauth.bat")
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении: {e}")

if __name__ == "__main__":
    try:
        update_google_oauth_keys()
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
