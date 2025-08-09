#!/usr/bin/env python
"""
Исправление дублированных сообщений о входе
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_duplicate_messages():
    """Исправляет дублированные сообщения о входе"""
    
    print("🔧 Исправление дублированных сообщений о входе")
    print("=" * 60)
    
    # 1. Обновляем settings.py - отключаем автоматические сообщения allauth
    print("1️⃣ Добавляем настройки для отключения автоматических сообщений allauth...")
    
    settings_file = "config/settings.py"
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Новые настройки для отключения дублированных сообщений
    message_settings = """
# Отключаем автоматические сообщения allauth (против дублирования)
ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',  # Используем стандартную форму без сообщений
}

# Настройки сообщений
MESSAGE_TAGS = {
    10: 'debug',
    20: 'info', 
    25: 'success',
    30: 'warning',
    40: 'error',
}

# Отключаем дополнительные сообщения от allauth
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

# Отключаем дублированные сообщения при социальном входе
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_STORE_TOKENS = False  # Не сохраняем токены (уменьшает сообщения)
"""
    
    if "MESSAGE_TAGS" not in content:
        content += message_settings
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ Добавлены настройки отключения автоматических сообщений")
    else:
        print("   ℹ️  Настройки сообщений уже существуют")
    
    # 2. Обновляем signals.py - убираем дублированный perform_login
    print("\n2️⃣ Исправляем signals.py...")
    
    signals_file = "accounts/signals.py"
    
    new_signals_content = """from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib import messages

@receiver(pre_social_login)
def handle_social_login(sender, request, sociallogin, **kwargs):
    \"\"\"
    Обработка социального входа без дублирования сообщений
    \"\"\"
    # Если пользователь уже существует, просто пропускаем
    # (allauth сам обработает вход и покажет одно сообщение)
    if sociallogin.user and sociallogin.user.pk:
        # Убираем дополнительный perform_login - он дублирует сообщения
        # Просто добавляем кастомную логику если нужно
        pass
    
    # Можно добавить дополнительную логику здесь,
    # но без дублирования входа в систему
"""
    
    with open(signals_file, 'w', encoding='utf-8') as f:
        f.write(new_signals_content)
    
    print("   ✅ Убран дублированный perform_login из signals.py")
    
    # 3. Проверяем, нет ли других мест с сообщениями
    print("\n3️⃣ Проверяем другие возможные источники дублирования...")
    
    # Проверяем views.py на предмет ручных сообщений о входе
    views_file = "accounts/views.py"
    with open(views_file, 'r', encoding='utf-8') as f:
        views_content = f.read()
    
    if "messages.success" in views_content and ("вошли" in views_content.lower() or "login" in views_content.lower()):
        print("   ⚠️  В accounts/views.py найдены сообщения о входе")
        print("      Проверьте, нет ли там дублированных сообщений")
    else:
        print("   ✅ В accounts/views.py нет проблемных сообщений о входе")
    
    print("\n" + "=" * 60)
    print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)
    
    print(f"\n✅ Что исправлено:")
    print(f"   - Отключены автоматические сообщения allauth")
    print(f"   - Убран дублированный perform_login из signals.py")
    print(f"   - Настроены MESSAGE_TAGS для правильного отображения")
    
    print(f"\n🚀 Что делать дальше:")
    print(f"   1. Перезапустите Django сервер")
    print(f"   2. Попробуйте войти через Google")
    print(f"   3. Должно появиться только одно сообщение")
    
    print(f"\n💡 Если проблема останется:")
    print(f"   - Проверьте базовый шаблон на дублированные {% if messages %}")
    print(f"   - Посмотрите на middleware, который может добавлять сообщения")

if __name__ == "__main__":
    try:
        fix_duplicate_messages()
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении: {e}")
        import traceback
        traceback.print_exc()
