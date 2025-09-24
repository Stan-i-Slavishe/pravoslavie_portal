#!/usr/bin/env python
"""
Проверка настройки reCAPTCHA на продакшен сервере
"""
import os
import sys
import django
from pathlib import Path

# Настройка Django для продакшена
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_ENV', 'production')  # Принудительно продакшен
django.setup()

def check_production_recaptcha():
    """Проверяем настройки reCAPTCHA для продакшена"""
    from django.conf import settings
    
    print("🛡️ ПРОВЕРКА GOOGLE reCAPTCHA v3 - ПРОДАКШЕН СЕРВЕР")
    print("=" * 60)
    
    # Определяем окружение
    environment = getattr(settings, 'DEBUG', True)
    env_name = "⚠️ РАЗРАБОТКА (DEBUG=True)" if environment else "✅ ПРОДАКШЕН (DEBUG=False)"
    print(f"🌍 Окружение: {env_name}")
    print(f"📁 Настройки: {settings.SETTINGS_MODULE}")
    print()
    
    if environment:
        print("⚠️ ВНИМАНИЕ: Сервер работает в режиме DEBUG=True!")
        print("   Это НЕ безопасно для продакшена!")
        print("   reCAPTCHA будет отключена в этом режиме")
        print()
    
    # Проверяем настройки reCAPTCHA
    print("🔍 Проверка настроек Google reCAPTCHA v3...")
    print("-" * 50)
    
    checks = {
        "DEBUG отключен": not getattr(settings, 'DEBUG', True),
        "RECAPTCHA_PUBLIC_KEY": getattr(settings, 'RECAPTCHA_PUBLIC_KEY', None),
        "RECAPTCHA_PRIVATE_KEY": getattr(settings, 'RECAPTCHA_PRIVATE_KEY', None), 
        "RECAPTCHA_REQUIRED_SCORE": getattr(settings, 'RECAPTCHA_REQUIRED_SCORE', None),
        "django_recaptcha установлен": 'django_recaptcha' in settings.INSTALLED_APPS,
        "ACCOUNT_FORMS настроен": hasattr(settings, 'ACCOUNT_FORMS'),
    }
    
    all_ok = True
    
    for check_name, value in checks.items():
        if value:
            if check_name.endswith('_KEY') and len(str(value)) > 10:
                # Скрываем ключи для безопасности
                display_value = f"{str(value)[:10]}...{str(value)[-4:]}"
                print(f"✅ {check_name}: {display_value}")
            else:
                print(f"✅ {check_name}: {value}")
        else:
            print(f"❌ {check_name}: НЕ НАСТРОЕНО")
            all_ok = False
    
    # Проверяем что ключи не тестовые
    public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', '')
    if public_key.startswith('6LeIxAcTAAAAAJ'):
        print("⚠️ ВНИМАНИЕ: Используются ТЕСТОВЫЕ ключи Google!")
        print("   На продакшене должны быть реальные ключи для dobrist.com")
        all_ok = False
    
    print("-" * 50)
    
    if all_ok:
        print("🎉 Настройки reCAPTCHA готовы для продакшена!")
    else:
        print("⚠️ Обнаружены проблемы с настройками продакшена")
    
    print()
    return all_ok

def check_domain_configuration():
    """Проверяем настройки домена"""
    from django.conf import settings
    
    print("🌐 Проверка настроек домена...")
    print("-" * 50)
    
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    required_domains = ['dobrist.com', 'www.dobrist.com']
    
    print(f"ALLOWED_HOSTS: {allowed_hosts}")
    
    domain_ok = True
    for domain in required_domains:
        if domain in allowed_hosts:
            print(f"✅ Домен {domain} разрешен")
        else:
            print(f"❌ Домен {domain} НЕ найден в ALLOWED_HOSTS")
            domain_ok = False
    
    print("-" * 50)
    return domain_ok

def check_form_integration():
    """Проверяем интеграцию формы"""
    print("📝 Проверка кастомной формы...")
    print("-" * 50)
    
    try:
        from accounts.forms import CustomSignupForm
        from django.conf import settings
        
        # Создаем форму
        form = CustomSignupForm()
        
        # В продакшене должна быть капча
        has_captcha = 'captcha' in form.fields
        is_production = not settings.DEBUG
        
        if is_production:
            if has_captcha:
                print("✅ reCAPTCHA поле присутствует в форме (продакшен)")
            else:
                print("❌ reCAPTCHA поле отсутствует в продакшен форме!")
                return False
        else:
            if not has_captcha:
                print("✅ reCAPTCHA поле отсутствует (режим разработки)")
            else:
                print("⚠️ reCAPTCHA поле присутствует в режиме разработки")
        
        print("✅ Кастомная форма создается корректно")
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке формы: {e}")
        print("-" * 50)
        return False

def main():
    """Главная функция проверки"""
    print("🔒 ПРОВЕРКА ГОТОВНОСТИ reCAPTCHA К ПРОДАКШЕН ДЕПЛОЮ")
    print("=" * 60)
    
    # Запускаем все проверки
    tests = [
        check_production_recaptcha,
        check_domain_configuration, 
        check_form_integration,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")
            results.append(False)
        print()
    
    # Итоговый результат
    print("=" * 60)
    if all(results):
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! ГОТОВО К ДЕПЛОЮ!")
        print("\n🚀 Команды для деплоя:")
        print("   git add .")
        print("   git commit -m 'Настроена Google reCAPTCHA v3 для продакшена'")
        print("   git push origin main")
        print("   ./deploy.sh")
        print()
        print("📊 После деплоя мониторинг:")
        print("   • Google reCAPTCHA Admin: https://www.google.com/recaptcha/admin")
        print("   • Тест формы: https://dobrist.com/accounts/signup/")
        exit_code = 0
    else:
        failed_count = len([r for r in results if not r])
        print(f"⚠️ {failed_count} из {len(results)} проверок провалились")
        print("\n🔧 Что нужно исправить:")
        print("   1. Убедитесь что DEBUG=False в продакшен настройках")
        print("   2. Проверьте что используются реальные ключи reCAPTCHA")
        print("   3. Убедитесь что домены настроены корректно")
        exit_code = 1
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
