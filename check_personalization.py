#!/usr/bin/env python
"""
Скрипт для проверки и исправления персонализированных товаров
"""

import os
import django
import sys

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

def check_and_fix_personalization():
    """Проверяем и исправляем персонализированные товары"""
    
    print("🔍 Проверяем персонализированные товары...")
    
    # Получаем все активные товары
    products = Product.objects.filter(is_active=True)
    
    print(f"📊 Всего активных товаров: {products.count()}")
    
    # Проверяем каждый товар
    for product in products:
        print(f"\n📦 Товар: {product.title}")
        print(f"   Тип: {product.product_type}")
        print(f"   Цена: {product.price}₽")
        print(f"   Требует персонализации: {product.requires_personalization}")
        
        # Проверяем логику для сказок
        if product.product_type == 'fairy_tale':
            if not product.requires_personalization:
                print("   ⚠️  ПРОБЛЕМА: Сказка должна требовать персонализации!")
                
                # Исправляем
                product.requires_personalization = True
                product.save()
                print("   ✅ ИСПРАВЛЕНО: Установлено requires_personalization=True")
            else:
                print("   ✅ Все в порядке: Сказка требует персонализации")
        
        elif product.product_type in ['book', 'audio']:
            if product.requires_personalization:
                print("   ⚠️  ПРЕДУПРЕЖДЕНИЕ: Книга/аудио не должна требовать персонализации")
                
                # Можно исправить автоматически
                response = input("     Исправить? (y/n): ")
                if response.lower() == 'y':
                    product.requires_personalization = False
                    product.save()
                    print("   ✅ ИСПРАВЛЕНО: Убрана требование персонализации")
            else:
                print("   ✅ Все в порядке: Не требует персонализации")
    
    print("\n🎉 Проверка завершена!")

if __name__ == "__main__":
    check_and_fix_personalization()
