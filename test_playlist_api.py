#!/usr/bin/env python
"""
Тест API плейлистов
Запуск: python test_playlist_api.py
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_playlist_api():
    print("🧪 Тестирование API плейлистов...")
    
    client = Client()
    
    # 1. Тест без авторизации
    print("\n1. Тест без авторизации:")
    response = client.get('/stories/api/playlists/')
    print(f"   Статус: {response.status_code}")
    if response.status_code == 302:
        print("   ✅ Перенаправление на login (правильно)")
    
    # 2. Создаем тестового пользователя
    print("\n2. Создание тестового пользователя:")
    try:
        user = User.objects.get(username='test_playlist_user')
        print("   ✅ Пользователь существует")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_playlist_user',
            password='testpass123'
        )
        print("   ✅ Пользователь создан")
    
    # 3. Авторизация
    print("\n3. Авторизация:")
    login_success = client.login(username='test_playlist_user', password='testpass123')
    print(f"   Авторизация: {'✅ Успешно' if login_success else '❌ Ошибка'}")
    
    # 4. Тест API плейлистов
    print("\n4. Тест API плейлистов:")
    response = client.get('/stories/api/playlists/?story_slug=test-story')
    print(f"   Статус: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✅ JSON ответ получен: {data}")
        except:
            print("   ❌ Ошибка парсинга JSON")
    else:
        print(f"   ❌ Ошибка: {response.content}")
    
    # 5. Тест создания плейлиста
    print("\n5. Тест создания плейлиста:")
    response = client.post('/stories/api/create-playlist/', {
        'name': 'Тестовый плейлист',
        'story_slug': 'test-story'
    })
    print(f"   Статус: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✅ Плейлист создан: {data}")
        except:
            print("   ❌ Ошибка парсинга JSON")
    else:
        print(f"   ❌ Ошибка: {response.content}")
    
    print("\n🎉 Тестирование завершено!")

if __name__ == "__main__":
    test_playlist_api()
