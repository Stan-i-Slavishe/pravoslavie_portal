# create_mobile_feedback_migration.py
"""
Скрипт для создания миграции модели MobileFeedback
"""
import os
import sys
import django

# Добавляем корневую директорию проекта в sys.path
sys.path.append(r'E:\pravoslavie_portal')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def create_migration():
    """Создаем миграцию для новой модели MobileFeedback"""
    print("🔄 Создание миграции для модели MobileFeedback...")
    
    try:
        # Создаем миграцию
        execute_from_command_line(['manage.py', 'makemigrations', 'core'])
        print("✅ Миграция создана успешно!")
        
        # Применяем миграцию
        print("🔄 Применение миграции...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Миграция применена успешно!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании/применении миграции: {e}")
        return False

if __name__ == "__main__":
    create_migration()