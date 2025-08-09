#!/usr/bin/env python
"""
Настройка прямого перенаправления на Google без промежуточной страницы
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def update_allauth_settings():
    """Обновляет настройки allauth для прямого перенаправления"""
    
    print("🔧 Настройка прямого перенаправления на Google")
    print("=" * 60)
    
    settings_file = "config/settings.py"
    
    # Читаем текущий файл настроек
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Настройки для прямого перенаправления
    direct_redirect_settings = """
# Настройки для прямого перенаправления на Google (без промежуточной страницы)
SOCIALACCOUNT_LOGIN_ON_GET = True  # Автоматический вход при GET запросе
SOCIALACCOUNT_EMAIL_AUTHENTICATION = False  # Не запрашивать email дополнительно
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True  # Автоматическое подключение email
"""
    
    # Проверяем, есть ли уже эти настройки
    if "SOCIALACCOUNT_LOGIN_ON_GET" in content:
        print("⚠️  Настройки прямого перенаправления уже существуют")
        print("✅ Проверьте, что SOCIALACCOUNT_LOGIN_ON_GET = True")
    else:
        # Добавляем новые настройки в конец файла
        content += direct_redirect_settings
        
        # Записываем обновленный файл
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Добавлены настройки прямого перенаправления:")
        print("   - SOCIALACCOUNT_LOGIN_ON_GET = True")
        print("   - SOCIALACCOUNT_EMAIL_AUTHENTICATION = False")
        print("   - SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True")
    
    print(f"\n🎯 Теперь при переходе на /accounts/google/login/")
    print(f"   произойдет прямое перенаправление на Google")
    print(f"   без промежуточной страницы подтверждения")
    
    print(f"\n🚀 Перезапустите Django сервер для применения изменений:")
    print(f"   python manage.py runserver")

if __name__ == "__main__":
    try:
        update_allauth_settings()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
