"""
Проверка статуса OAuth провайдеров
"""
import os
import sys
import django

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def check_oauth_status():
    """Проверяет статус настройки OAuth провайдеров"""
    
    print("🔐 Проверка статуса OAuth провайдеров\n")
    print("=" * 60)
    
    # Получаем текущий сайт
    try:
        site = Site.objects.get_current()
        print(f"📍 Текущий сайт: {site.domain} (ID: {site.id})")
    except Exception as e:
        print(f"⚠️ Ошибка получения сайта: {e}")
        return
    
    print("=" * 60)
    print()
    
    # Список провайдеров для проверки
    providers = ['google', 'vk', 'telegram', 'mailru', 'yandex']
    provider_names = {
        'google': 'Google',
        'vk': 'ВКонтакте',
        'telegram': 'Telegram',
        'mailru': 'Mail.ru',
        'yandex': 'Яндекс'
    }
    
    configured = []
    not_configured = []
    
    for provider_id in providers:
        provider_name = provider_names.get(provider_id, provider_id)
        
        try:
            # Проверяем, есть ли приложение для этого провайдера
            apps = SocialApp.objects.filter(provider=provider_id)
            
            if apps.exists():
                app = apps.first()
                # Проверяем, привязан ли к нужному сайту
                if site in app.sites.all():
                    print(f"✅ {provider_name:15} - Настроен и активен")
                    print(f"   Client ID: {app.client_id[:20]}...")
                    print(f"   Привязан к сайту: {site.domain}")
                    configured.append(provider_name)
                else:
                    print(f"⚠️ {provider_name:15} - Настроен, но НЕ привязан к сайту!")
                    print(f"   Нужно добавить сайт '{site.domain}' в админке")
                    not_configured.append(provider_name)
            else:
                print(f"❌ {provider_name:15} - НЕ настроен")
                print(f"   Нужно добавить в Django Admin")
                not_configured.append(provider_name)
                
        except Exception as e:
            print(f"❌ {provider_name:15} - Ошибка: {e}")
            not_configured.append(provider_name)
        
        print()
    
    # Итоговая статистика
    print("=" * 60)
    print("📊 СТАТИСТИКА:")
    print(f"   Настроено: {len(configured)}/5")
    print(f"   Не настроено: {len(not_configured)}/5")
    print("=" * 60)
    
    if configured:
        print(f"\n✅ Работают: {', '.join(configured)}")
    
    if not_configured:
        print(f"\n❌ Требуют настройки: {', '.join(not_configured)}")
        print("\n💡 Для настройки:")
        print("   1. Откройте OAUTH_QUICK_STEPS.md")
        print("   2. Зарегистрируйте приложения в соцсетях")
        print("   3. Добавьте их в Django Admin:")
        print("      http://localhost:8000/admin/socialaccount/socialapp/")
    
    print("\n" + "=" * 60)
    print("🔗 Полезные ссылки:")
    print("   📝 Быстрая инструкция: OAUTH_QUICK_STEPS.md")
    print("   📖 Подробный гайд: OAUTH_SETUP_GUIDE.md")
    print("   🔧 Django Admin: http://localhost:8000/admin/")
    print("=" * 60)

if __name__ == '__main__':
    try:
        check_oauth_status()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
