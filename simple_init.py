#!/usr/bin/env python
"""
Упрощенный скрипт для инициализации без Redis
Запустить: python simple_init.py
"""

import os
import sys

# Настройка переменных окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')

# Создадим простые настройки без Redis
settings_content = '''
from .settings import *

# Отключаем Redis для начальной инициализации
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Отключаем Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'

# Простое логирование без emoji
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
'''

# Создаем файл настроек
with open('config/settings_simple.py', 'w', encoding='utf-8') as f:
    f.write(settings_content)

print("Создан упрощенный файл настроек")

# Импортируем Django
import django
django.setup()

from django.core.management import execute_from_command_line

def run_command(args, description):
    """Выполнить Django команду"""
    print(f"[INFO] {description}...")
    try:
        execute_from_command_line(['manage.py'] + args)
        print(f"[OK] {description} - успешно!")
        return True
    except Exception as e:
        print(f"[ERROR] {description} - ошибка: {e}")
        return False

def init_simple():
    """Простая инициализация"""
    
    print("=== Инициализация базы данных ===")
    
    # 1. Создание миграций
    if not run_command(['makemigrations'], "Создание миграций"):
        return False
    
    # 2. Применение миграций
    if not run_command(['migrate'], "Применение миграций"):
        return False
    
    # 3. Создание настроек сайта
    print("[INFO] Создание настроек сайта...")
    
    try:
        from core.models import SiteSettings
        
        if SiteSettings.objects.exists():
            print("[OK] Настройки уже существуют")
        else:
            settings = SiteSettings.objects.create(
                site_name='Добрые истории',
                site_description='Духовные рассказы, книги и аудио для современного человека',
                contact_email='info@dobrye-istorii.ru',
                contact_phone='+7 (800) 123-45-67',
                social_telegram='https://t.me/dobrye_istorii',
                social_youtube='https://www.youtube.com/@dobrye_istorii',
                social_vk='https://vk.com/dobrye_istorii'
            )
            print("[OK] Настройки сайта созданы!")
            
    except Exception as e:
        print(f"[ERROR] Ошибка создания настроек: {e}")
        return False
    
    # 4. Сбор статических файлов
    run_command(['collectstatic', '--noinput'], "Сбор статических файлов")
    
    print("=== Инициализация завершена ===")
    print("Следующие шаги:")
    print("1. python manage.py runserver")
    print("2. Откройте http://127.0.0.1:8000/admin/")
    print("3. Настройки сайта будут доступны")
    
    return True

if __name__ == '__main__':
    init_simple()
