#!/usr/bin/env python3
"""
Удаление существующего пользователя для тестирования Google OAuth
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

def remove_existing_user():
    email = "atasalin1984@gmail.com"
    
    print(f"🔍 Поиск пользователя с email: {email}")
    
    try:
        user = User.objects.get(email=email)
        print(f"✅ Найден пользователь: {user.email} (ID: {user.id})")
        
        # Проверяем связанные Google аккаунты
        social_accounts = SocialAccount.objects.filter(user=user, provider='google')
        if social_accounts.exists():
            print(f"📱 Найдено {social_accounts.count()} связанных Google аккаунтов")
            for account in social_accounts:
                print(f"   - Google ID: {account.uid}")
        else:
            print("📱 Google аккаунты не связаны")
        
        # Удаляем пользователя
        user.delete()
        print("🗑️  Пользователь удален")
        
        print("\n✅ Теперь можете попробовать Google OAuth снова!")
        print("http://127.0.0.1:8000/accounts/google/login/")
        
    except User.DoesNotExist:
        print(f"❌ Пользователь с email {email} не найден")
        
        # Попробуем найти всех пользователей
        all_users = User.objects.all()
        print(f"\n📊 Всего пользователей в базе: {all_users.count()}")
        
        if all_users.exists():
            print("📝 Список всех пользователей:")
            for user in all_users:
                print(f"   - {user.email} (ID: {user.id})")

if __name__ == '__main__':
    remove_existing_user()
