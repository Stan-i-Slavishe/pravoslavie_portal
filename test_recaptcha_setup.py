#!/usr/bin/env python
"""
Тест настройки Google reCAPTCHA v3 для формы регистрации
"""
import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_recaptcha_settings():
    """Проверяем настройки reCAPTCHA"""
    from django.conf import settings
    
    print("🔍 Проверка настроек Google reCAPTCHA v3...")
    print("-" * 50)
    
    # Проверяем наличие настроек
    checks = {
        "RECAPTCHA_PUBLIC_KEY": getattr(settings, 'RECAPTCHA_PUBLIC_KEY', None),
        "RECAPTCHA_PRIVATE_KEY": getattr(settings, 'RECAPTCHA_PRIVATE_KEY', None),
        "RECAPTCHA_REQUIRED_SCORE": getattr(settings, 'RECAPTCHA_REQUIRED_SCORE', None),
        "django_recaptcha в INSTALLED_APPS": 'django_recaptcha' in settings.INSTALLED_APPS,
    }
    
    all_ok = True
    
    for check_name, value in checks.items():
        if value:
            if check_name.endswith('_KEY'):
                # Скрываем ключи для безопасности
                display_value = f"{str(value)[:10]}...{str(value)[-4:]}" if len(str(value)) > 14 else "***"
                print(f"✅ {check_name}: {display_value}")
            else:
                print(f"✅ {check_name}: {value}")
        else:
            print(f"❌ {check_name}: НЕ НАСТРОЕНО")
            all_ok = False
    
    print("-" * 50)
    
    if all_ok:
        print("🎉 Все настройки reCAPTCHA корректны!")
    else:
        print("⚠️ Обнаружены проблемы с настройками")
    
    return all_ok

def test_custom_signup_form():
    """Проверяем кастомную форму регистрации"""
    print("\n📝 Проверка кастомной формы регистрации...")
    print("-" * 50)
    
    try:
        from accounts.forms import CustomSignupForm
        from django_recaptcha.fields import ReCaptchaField
        
        # Создаем экземпляр формы
        form = CustomSignupForm()
        
        checks = {
            "Форма создается": True,
            "Поле captcha существует": hasattr(form, 'fields') and 'captcha' in form.fields,
            "Поле captcha - ReCaptchaField": isinstance(form.fields.get('captcha'), ReCaptchaField) if 'captcha' in form.fields else False,
            "Поле email настроено": 'email' in form.fields,
            "Поле password1 настроено": 'password1' in form.fields,
            "Поле password2 настроено": 'password2' in form.fields,
        }
        
        all_ok = True
        for check_name, status in checks.items():
            if status:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_ok = False
        
        print("-" * 50)
        
        if all_ok:
            print("🎉 Кастомная форма регистрации настроена корректно!")
        else:
            print("⚠️ Обнаружены проблемы с кастомной формой")
            
        return all_ok
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def test_allauth_integration():
    """Проверяем интеграцию с django-allauth"""
    print("\n🔗 Проверка интеграции с django-allauth...")
    print("-" * 50)
    
    from django.conf import settings
    
    checks = {
        "allauth в INSTALLED_APPS": 'allauth' in settings.INSTALLED_APPS,
        "allauth.account в INSTALLED_APPS": 'allauth.account' in settings.INSTALLED_APPS,
        "ACCOUNT_FORMS настроен": hasattr(settings, 'ACCOUNT_FORMS') and 'signup' in getattr(settings, 'ACCOUNT_FORMS', {}),
        "Кастомная форма указана": getattr(settings, 'ACCOUNT_FORMS', {}).get('signup') == 'accounts.forms.CustomSignupForm',
    }
    
    all_ok = True
    for check_name, status in checks.items():
        if status:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_ok = False
    
    print("-" * 50)
    
    if all_ok:
        print("🎉 Интеграция с django-allauth настроена корректно!")
    else:
        print("⚠️ Обнаружены проблемы с интеграцией allauth")
    
    return all_ok

def main():
    """Главная функция тестирования"""
    print("🛡️ ТЕСТ НАСТРОЙКИ GOOGLE reCAPTCHA v3 ДЛЯ РЕГИСТРАЦИИ")
    print("=" * 60)
    
    # Определяем окружение
    from django.conf import settings
    environment = getattr(settings, 'DEBUG', False)
    env_name = "Локальная разработка" if environment else "Продакшен"
    print(f"🌍 Окружение: {env_name}")
    print(f"📁 Настройки: {settings.SETTINGS_MODULE}")
    print()
    
    # Запускаем все тесты
    tests = [
        test_recaptcha_settings,
        test_custom_signup_form,
        test_allauth_integration,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")
            results.append(False)
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! reCAPTCHA готова к использованию")
        print("\n📋 Что можно делать дальше:")
        print("   1. Запустить сервер: python manage.py runserver")
        print("   2. Перейти на страницу регистрации: /accounts/signup/")
        print("   3. Протестировать регистрацию нового пользователя")
        print("   4. Развернуть на продакшен: ./deploy.sh")
        exit_code = 0
    else:
        failed_count = len([r for r in results if not r])
        print(f"⚠️ {failed_count} из {len(results)} тестов провалились")
        print("\n📋 Что нужно исправить:")
        print("   1. Проверьте настройки в config/settings*.py")
        print("   2. Убедитесь что django-recaptcha установлен")
        print("   3. Проверьте правильность ключей reCAPTCHA")
        exit_code = 1
    
    print("\n🔗 Полезные ссылки:")
    print("   • Google reCAPTCHA Admin: https://www.google.com/recaptcha/admin")
    print("   • Документация django-recaptcha: https://github.com/praekelt/django-recaptcha")
    print("   • Тестовые ключи: https://developers.google.com/recaptcha/docs/faq")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
