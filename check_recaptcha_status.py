#!/usr/bin/env python
"""
Быстрая проверка: работает ли reCAPTCHA в текущем окружении
"""
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from accounts.forms import CustomSignupForm

print("🔍 ПРОВЕРКА РАБОТЫ reCAPTCHA В ТЕКУЩЕМ ОКРУЖЕНИИ")
print("=" * 60)

# Проверяем режим
debug_mode = settings.DEBUG
env_name = "Локальная разработка (DEBUG=True)" if debug_mode else "Продакшен (DEBUG=False)"

print(f"🌍 Окружение: {env_name}")
print(f"📁 Настройки: {settings.SETTINGS_MODULE}")
print()

# Создаем форму и проверяем наличие капчи
form = CustomSignupForm()
has_captcha = 'captcha' in form.fields

print("📋 Поля формы регистрации:")
print("-" * 60)
for field_name in form.fields.keys():
    print(f"  • {field_name}")
print("-" * 60)
print()

# Результат
print("🎯 РЕЗУЛЬТАТ:")
print("=" * 60)

if debug_mode:
    if has_captcha:
        print("⚠️ НЕОЖИДАННО: Капча присутствует в режиме DEBUG=True")
        print("   Это может вызвать ошибки!")
    else:
        print("✅ ПРАВИЛЬНО: Капча отключена в режиме разработки")
        print()
        print("📝 Что это означает:")
        print("   • Регистрация работает БЕЗ проверки капчи")
        print("   • Нет запросов к Google API")
        print("   • Удобно для тестирования")
        print()
        print("🚀 На продакшене (когда DEBUG=False):")
        print("   • Капча ВКЛЮЧИТСЯ автоматически")
        print("   • Будет полная защита от ботов")
        print("   • Google будет анализировать поведение")
else:
    if has_captcha:
        print("✅ ПРАВИЛЬНО: Капча активна на продакшене")
        print()
        print("🛡️ Что это означает:")
        print("   • Google reCAPTCHA v3 работает")
        print("   • Анализируется поведение пользователей")
        print("   • Боты блокируются автоматически")
        print()
        print("📊 Настройки защиты:")
        public_key = settings.RECAPTCHA_PUBLIC_KEY[:15] + "..."
        score = settings.RECAPTCHA_REQUIRED_SCORE
        print(f"   • Публичный ключ: {public_key}")
        print(f"   • Порог безопасности: {score} (высокий)")
    else:
        print("❌ ОШИБКА: Капча должна быть активна на продакшене!")
        print("   Проверьте настройки!")

print()
print("=" * 60)
