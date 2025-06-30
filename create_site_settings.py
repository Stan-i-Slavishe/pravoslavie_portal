#!/usr/bin/env python
"""
Скрипт для создания начальных настроек сайта
Запустить: python create_site_settings.py
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SiteSettings

def create_site_settings():
    """Создать начальные настройки сайта"""
    
    # Проверяем, есть ли уже настройки
    if SiteSettings.objects.exists():
        print("⚠️  Настройки сайта уже существуют!")
        settings = SiteSettings.objects.first()
        print(f"Название сайта: {settings.site_name}")
        return settings
    
    # Создаем новые настройки
    settings = SiteSettings.objects.create(
        site_name='Добрые истории',
        site_description='Духовные рассказы, книги и аудио для современного человека',
        contact_email='info@dobrye-istorii.ru',
        contact_phone='+7 (800) 123-45-67',
        social_telegram='https://t.me/dobrye_istorii',
        social_youtube='https://www.youtube.com/@dobrye_istorii',
        social_vk='https://vk.com/dobrye_istorii',
        maintenance_mode=False,
        maintenance_message='',
        analytics_yandex='',
        analytics_google=''
    )
    
    print("✅ Настройки сайта успешно созданы!")
    print(f"ID: {settings.id}")
    print(f"Название: {settings.site_name}")
    print(f"Описание: {settings.site_description}")
    print(f"Email: {settings.contact_email}")
    print(f"Telegram: {settings.social_telegram}")
    print(f"YouTube: {settings.social_youtube}")
    print(f"ВКонтакте: {settings.social_vk}")
    
    return settings

if __name__ == '__main__':
    create_site_settings()
