#!/usr/bin/env python3
"""
Удаление конкретного пользователя по email
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

def remove_user_by_email(email):
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

if __name__ == '__main__':
    # Используем правильный email
    email = "stassilin1984@gmail.com"  # Найденный в базе
    remove_user_by_email(email)
