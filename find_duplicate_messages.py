#!/usr/bin/env python
"""
Поиск дублированных сообщений об успешном входе
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def search_login_messages():
    """Ищет места, где добавляются сообщения о входе"""
    
    print("🔍 Поиск дублированных сообщений об успешном входе")
    print("=" * 60)
    
    # Директории для поиска
    search_dirs = [
        "accounts",
        "core", 
        "config",
        "templates"
    ]
    
    # Ключевые слова для поиска
    search_patterns = [
        "messages.success",
        "messages.add_message", 
        "Вы вошли как",
        "успешно вошли",
        "вошли как",
        "login success",
        "logged in"
    ]
    
    found_files = []
    
    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
            
        print(f"\n📁 Поиск в директории: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.html')):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        for pattern in search_patterns:
                            if pattern.lower() in content.lower():
                                print(f"   🎯 Найдено в {file_path}")
                                print(f"      Паттерн: {pattern}")
                                
                                # Показываем строки с найденным паттерном
                                lines = content.split('\n')
                                for i, line in enumerate(lines, 1):
                                    if pattern.lower() in line.lower():
                                        print(f"      Строка {i}: {line.strip()}")
                                
                                if file_path not in found_files:
                                    found_files.append(file_path)
                                break
                                
                    except Exception as e:
                        continue
    
    print(f"\n📋 Итого найдено файлов с сообщениями о входе: {len(found_files)}")
    
    if len(found_files) > 1:
        print("⚠️  Возможные причины дублирования:")
        print("   1. Несколько views добавляют сообщения")
        print("   2. Allauth + кастомные сообщения")
        print("   3. Middleware добавляет дополнительные сообщения")
    
    return found_files

def check_allauth_messages_settings():
    """Проверяет настройки сообщений allauth"""
    
    print(f"\n🔧 Проверка настроек сообщений allauth")
    print("=" * 40)
    
    from django.conf import settings
    
    # Проверяем настройки, которые могут влиять на сообщения
    message_settings = [
        'ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION',
        'ACCOUNT_EMAIL_VERIFICATION',
        'SOCIALACCOUNT_AUTO_SIGNUP',
        'SOCIALACCOUNT_LOGIN_ON_GET',
    ]
    
    for setting_name in message_settings:
        value = getattr(settings, setting_name, 'НЕ УСТАНОВЛЕН')
        print(f"   {setting_name}: {value}")
    
    # Проверяем MESSAGE_TAGS
    if hasattr(settings, 'MESSAGE_TAGS'):
        print(f"\n📨 MESSAGE_TAGS: {settings.MESSAGE_TAGS}")
    
    print(f"\n💡 Рекомендация:")
    print(f"   Отключить автоматические сообщения allauth и использовать свои")

if __name__ == "__main__":
    try:
        files = search_login_messages()
        check_allauth_messages_settings()
        
        print(f"\n🎯 Для исправления:")
        print(f"   1. Найдите дублированные сообщения в файлах выше")
        print(f"   2. Оставьте только одно место для добавления сообщения")
        print(f"   3. Или отключите автоматические сообщения allauth")
        
    except Exception as e:
        print(f"❌ Ошибка при поиске: {e}")
        import traceback
        traceback.print_exc()
