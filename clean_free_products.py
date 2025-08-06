#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления бесплатных товаров из магазина
"""

import os
import sys
import django

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

def clean_free_products():
    """Удаляет все бесплатные товары из магазина"""
    
    print("🧹 Начинаем очистку бесплатных товаров из магазина...")
    
    # Найдем все бесплатные товары
    free_products = Product.objects.filter(price=0)
    
    print(f"📊 Найдено бесплатных товаров: {free_products.count()}")
    
    if free_products.exists():
        for product in free_products:
            print(f"   - {product.title} (ID: {product.id}, цена: {product.price}₽)")
        
        # Деактивируем бесплатные товары
        updated_count = free_products.update(is_active=False)
        print(f"✅ Деактивировано товаров: {updated_count}")
        
        # Опционально - полностью удалить
        delete_choice = input("\n❓ Полностью удалить бесплатные товары? (y/N): ").lower()
        if delete_choice == 'y':
            deleted_count = free_products.delete()[0]
            print(f"🗑️ Удалено товаров: {deleted_count}")
        else:
            print("💼 Товары деактивированы, но оставлены в базе")
    else:
        print("✅ Бесплатных товаров не найдено")
    
    # Покажем итоговую статистику
    print("\n📈 Итоговая статистика:")
    active_products = Product.objects.filter(is_active=True)
    paid_products = active_products.filter(price__gt=0)
    
    print(f"   Всего активных товаров: {active_products.count()}")
    print(f"   Платных товаров: {paid_products.count()}")
    print(f"   Бесплатных активных: {active_products.filter(price=0).count()}")
    
    if paid_products.exists():
        print("\n💰 Активные платные товары:")
        for product in paid_products:
            print(f"   - {product.title}: {product.price}₽")
    
    print("\n🎉 Очистка завершена!")

if __name__ == "__main__":
    clean_free_products()
