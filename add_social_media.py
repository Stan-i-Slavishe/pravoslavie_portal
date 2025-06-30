#!/usr/bin/env python
"""
Скрипт для добавления социальных сетей в настройки сайта
Запустить: python add_social_media.py
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SiteSettings

def add_social_media():
    """Добавить ссылки на социальные сети"""
    
    # Получаем или создаем настройки
    settings = SiteSettings.get_settings()
    
    # Обновляем социальные сети
    settings.social_telegram = 'https://t.me/dobrye_istorii'
    settings.social_youtube = 'https://www.youtube.com/@dobrye_istorii'
    settings.social_vk = 'https://vk.com/dobrye_istorii'
    
    # Сохраняем
    settings.save()
    
    print("✅ Социальные сети успешно добавлены!")
    print(f"Telegram: {settings.social_telegram}")
    print(f"YouTube: {settings.social_youtube}")
    print(f"ВКонтакте: {settings.social_vk}")

if __name__ == '__main__':
    add_social_media()
