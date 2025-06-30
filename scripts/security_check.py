#!/usr/bin/env python
"""
🔐 Скрипт проверки безопасности Django

Запуск: python security_check.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def run_security_checks():
    """Запускает проверки безопасности Django"""
    
    print("🔐 Запуск проверки безопасности Django...")
    print("=" * 50)
    
    # Устанавливаем настройки Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Запускаем check с флагами безопасности
    try:
        print("\n1️⃣ Базовые проверки Django:")
        execute_from_command_line(['manage.py', 'check'])
        
        print("\n2️⃣ Проверки безопасности Django:")
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        
        print("\n✅ Проверки завершены!")
        print("\n📝 Рекомендации:")
        print("- Установите DEBUG=False в продакшене")
        print("- Используйте HTTPS в продакшене")
        print("- Регулярно обновляйте зависимости")
        print("- Настройте мониторинг безопасности")
        
    except SystemExit as e:
        if e.code != 0:
            print(f"\n❌ Найдены проблемы безопасности (код: {e.code})")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Ошибка при проверке: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_security_checks()