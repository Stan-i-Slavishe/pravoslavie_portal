#!/usr/bin/env python
"""
Скрипт для полной инициализации базы данных
Запустить: python init_database.py
"""

import os
import django
import subprocess
import sys

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def run_command(command, description):
    """Выполнить команду и показать результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - ошибка!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False
    return True

def init_database():
    """Инициализация базы данных"""
    
    print("🚀 Инициализация базы данных...")
    
    # 1. Создание миграций
    if not run_command("python manage.py makemigrations", "Создание миграций"):
        return False
    
    # 2. Применение миграций
    if not run_command("python manage.py migrate", "Применение миграций"):
        return False
    
    # 3. Создание суперпользователя (если нужно)
    print("\n🔄 Проверка суперпользователя...")
    
    # Настройка Django после миграций
    django.setup()
    
    from django.contrib.auth.models import User
    from core.models import SiteSettings
    
    # Проверяем, есть ли суперпользователь
    if not User.objects.filter(is_superuser=True).exists():
        print("⚠️  Суперпользователь не найден.")
        print("Создайте суперпользователя командой: python manage.py createsuperuser")
    else:
        print("✅ Суперпользователь уже существует")
    
    # 4. Создание настроек сайта
    print("\n🔄 Создание настроек сайта...")
    
    if SiteSettings.objects.exists():
        print("✅ Настройки сайта уже существуют")
        settings = SiteSettings.objects.first()
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
        print("✅ Настройки сайта созданы!")
    
    # 5. Сбор статических файлов
    if not run_command("python manage.py collectstatic --noinput", "Сбор статических файлов"):
        print("⚠️  Статические файлы не собраны, но это не критично")
    
    print("\n🎉 Инициализация завершена!")
    print("📝 Следующие шаги:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Откройте админку: http://127.0.0.1:8000/admin/")
    print("3. Настройки сайта будут доступны в разделе 'Настройки сайта'")
    
    return True

if __name__ == '__main__':
    init_database()
