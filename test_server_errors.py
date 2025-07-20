#!/usr/bin/env python3
"""
Скрипт для тестирования доступности основных URLs проекта
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

def test_urls():
    """Тестируем основные URL"""
    client = Client()
    User = get_user_model()
    
    print("🧪 Тестирование основных URLs...")
    
    # Тест 1: Главная страница
    print("\n1️⃣ Тестируем главную страницу...")
    try:
        response = client.get('/')
        print(f"✅ Главная страница: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка главной страницы: {e}")
    
    # Тест 2: Корзина (без авторизации)
    print("\n2️⃣ Тестируем корзину без авторизации...")
    try:
        response = client.get('/shop/cart/count/')
        print(f"✅ Корзина (неавторизованный): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Данные корзины: {data}")
    except Exception as e:
        print(f"❌ Ошибка корзины: {e}")
    
    # Тест 3: Создаем тестового пользователя
    print("\n3️⃣ Создаем тестового пользователя...")
    try:
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        print(f"✅ Пользователь: {user.username} ({'создан' if created else 'существует'})")
    except Exception as e:
        print(f"❌ Ошибка создания пользователя: {e}")
        return
    
    # Тест 4: Авторизуемся
    print("\n4️⃣ Авторизуемся...")
    try:
        client.force_login(user)
        print("✅ Авторизация успешна")
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        return
    
    # Тест 5: Корзина (с авторизацией)
    print("\n5️⃣ Тестируем корзину с авторизацией...")
    try:
        response = client.get('/shop/cart/count/')
        print(f"✅ Корзина (авторизованный): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Данные корзины: {data}")
    except Exception as e:
        print(f"❌ Ошибка корзины: {e}")
    
    # Тест 6: Плейлисты
    print("\n6️⃣ Тестируем плейлисты...")
    try:
        response = client.post(
            '/stories/playlists/for-save/',
            data=json.dumps({'story_id': 1}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        print(f"✅ Плейлисты: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Данные плейлистов: {data}")
        elif response.status_code == 404:
            print("📝 Рассказ с ID=1 не найден (это нормально)")
        elif response.status_code >= 500:
            print(f"🔧 Ошибка сервера: {response.content.decode()[:200]}")
    except Exception as e:
        print(f"❌ Ошибка плейлистов: {e}")
    
    # Тест 7: Проверка моделей
    print("\n7️⃣ Проверяем модели...")
    try:
        from stories.models import Story, Playlist
        stories_count = Story.objects.count()
        print(f"📚 Рассказов в БД: {stories_count}")
        
        if Playlist:
            playlists_count = Playlist.objects.count()
            print(f"🎵 Плейлистов в БД: {playlists_count}")
        else:
            print("⚠️ Модель Playlist недоступна")
    except Exception as e:
        print(f"❌ Ошибка проверки моделей: {e}")
    
    print("\n🎯 Тестирование завершено!")

if __name__ == '__main__':
    test_urls()
