#!/usr/bin/env python
"""Очистка сессий просмотров для тестирования"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🧹 Очистка сессий...")
    
    try:
        # Очищаем все сессии
        call_command('clearsessions')
        print("✅ Сессии очищены!")
        print("🔄 Теперь счетчик просмотров будет увеличиваться только один раз за сессию")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
