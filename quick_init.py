#!/usr/bin/env python
"""
Максимально простой скрипт инициализации
"""

import os
import subprocess
import sys

def run_cmd(command):
    """Выполнить команду и показать результат"""
    print(f"Выполняется: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    if result.returncode == 0:
        print("OK")
        if result.stdout.strip():
            print(result.stdout)
    else:
        print("ОШИБКА:")
        print(result.stderr)
        return False
    return True

def main():
    print("=== Инициализация базы данных ===")
    
    # Используем настройки без Redis
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_minimal'
    
    commands = [
        "python manage.py makemigrations",
        "python manage.py migrate",
        "python manage.py collectstatic --noinput"
    ]
    
    for cmd in commands:
        if not run_cmd(cmd):
            print(f"Остановлено на команде: {cmd}")
            break
    
    # Создаем настройки через Django shell
    shell_commands = '''
from core.models import SiteSettings

if not SiteSettings.objects.exists():
    settings = SiteSettings.objects.create(
        site_name="Добрые истории",
        site_description="Духовные рассказы, книги и аудио для современного человека",
        contact_email="info@dobrye-istorii.ru",
        social_telegram="https://t.me/dobrye_istorii",
        social_youtube="https://www.youtube.com/@dobrye_istorii",
        social_vk="https://vk.com/dobrye_istorii"
    )
    print("Настройки созданы!")
else:
    print("Настройки уже существуют")
'''
    
    # Сохраняем команды в файл
    with open('temp_shell.py', 'w', encoding='utf-8') as f:
        f.write(shell_commands)
    
    print("Создание настроек сайта...")
    run_cmd("python manage.py shell < temp_shell.py")
    
    # Удаляем временный файл
    try:
        os.remove('temp_shell.py')
    except:
        pass
    
    print("\n=== ГОТОВО ===")
    print("Теперь можно запустить: python manage.py runserver")

if __name__ == '__main__':
    main()
