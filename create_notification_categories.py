#!/usr/bin/env python
"""
Скрипт для создания базовых категорий уведомлений
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import NotificationCategory

def create_notification_categories():
    """Создание базовых категорий уведомлений"""
    
    categories_data = [
        {
            'name': 'bedtime_stories',
            'title': 'Сказки на ночь',
            'description': 'Напоминания о чтении сказок перед сном для детей',
            'icon': '🌙',
            'default_enabled': True
        },
        {
            'name': 'orthodox_calendar',
            'title': 'Православный календарь',
            'description': 'Уведомления о православных праздниках, постах и важных датах',
            'icon': '⛪',
            'default_enabled': True
        },
        {
            'name': 'new_content',
            'title': 'Новый контент',
            'description': 'Уведомления о новых рассказах, статьях и материалах на портале',
            'icon': '📚',
            'default_enabled': True
        },
        {
            'name': 'fairy_tales',
            'title': 'Терапевтические сказки',
            'description': 'Рекомендации терапевтических сказок для решения детских проблем',
            'icon': '🧚',
            'default_enabled': True
        },
        {
            'name': 'audio_content',
            'title': 'Аудио-контент',
            'description': 'Новые аудио-рассказы, подкасты и аудиокниги',
            'icon': '🎵',
            'default_enabled': False
        },
        {
            'name': 'book_releases',
            'title': 'Новые книги',
            'description': 'Уведомления о поступлении новых книг в магазин',
            'icon': '📖',
            'default_enabled': True
        },
        {
            'name': 'special_events',
            'title': 'Особые события',
            'description': 'Важные события и мероприятия портала',
            'icon': '🎉',
            'default_enabled': False
        },
        {
            'name': 'daily_wisdom',
            'title': 'Мудрость дня',
            'description': 'Ежедневные духовные размышления и цитаты',
            'icon': '💭',
            'default_enabled': False
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for category_data in categories_data:
        category, created = NotificationCategory.objects.get_or_create(
            name=category_data['name'],
            defaults=category_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Создана категория: {category.icon} {category.title}")
        else:
            # Обновляем существующую категорию
            for key, value in category_data.items():
                if key != 'name':
                    setattr(category, key, value)
            category.save()
            updated_count += 1
            print(f"🔄 Обновлена категория: {category.icon} {category.title}")
    
    print(f"\n📊 Результат:")
    print(f"Создано новых категорий: {created_count}")
    print(f"Обновлено категорий: {updated_count}")
    print(f"Всего категорий: {NotificationCategory.objects.count()}")

if __name__ == '__main__':
    print("🚀 Создание категорий уведомлений...")
    create_notification_categories()
    print("✨ Готово!")
