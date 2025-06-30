#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Настройка Django
PROJECT_PATH = r'E:\pravoslavie_portal'
sys.path.insert(0, PROJECT_PATH)
os.chdir(PROJECT_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from analytics.models import PurchaseIntent, PopularContent
from shop.models import Product
from fairy_tales.models import FairyTaleTemplate

def clean_incorrect_analytics():
    """Очищаем неправильные записи аналитики"""
    
    print("🧹 Очистка неправильных записей аналитики...")
    print("=" * 60)
    
    # Находим все записи с content_type='product'
    product_intents = PurchaseIntent.objects.filter(content_type='product')
    print(f"📊 Найдено записей с content_type='product': {product_intents.count()}")
    
    for intent in product_intents:
        print(f"\n🔍 Проверяем: Product #{intent.object_id}")
        
        # Проверяем, существует ли товар с таким ID
        try:
            product = Product.objects.get(id=intent.object_id)
            print(f"  ✅ Товар найден: {product.title}")
            print(f"     Запись КОРРЕКТНА - оставляем")
        except Product.DoesNotExist:
            print(f"  ❌ Товар НЕ найден")
            
            # Проверяем, есть ли сказка с таким ID
            try:
                fairy_tale = FairyTaleTemplate.objects.get(id=intent.object_id)
                print(f"  🧚‍♀️ Найдена сказка: {fairy_tale.title}")
                print(f"     Это ОШИБОЧНАЯ запись - нужно исправить или удалить")
                
                # Предлагаем варианты
                print(f"     Варианты:")
                print(f"     1. Удалить запись (recommended)")
                print(f"     2. Исправить content_type на 'fairy_tale'")
                
                # Автоматически удаляем неправильные записи
                intent.delete()
                print(f"     ✅ УДАЛЕНО!")
                
            except FairyTaleTemplate.DoesNotExist:
                print(f"  ❓ Объект с ID {intent.object_id} не найден нигде")
                print(f"     Удаляем мертвую ссылку")
                intent.delete()
                print(f"     ✅ УДАЛЕНО!")
    
    # Также очищаем PopularContent
    print(f"\n📈 Проверяем PopularContent...")
    popular_products = PopularContent.objects.filter(content_type='product')
    print(f"Найдено записей: {popular_products.count()}")
    
    for popular in popular_products:
        print(f"\n🔍 Проверяем PopularContent: Product #{popular.object_id}")
        
        try:
            product = Product.objects.get(id=popular.object_id)
            print(f"  ✅ Товар найден: {product.title}")
        except Product.DoesNotExist:
            print(f"  ❌ Товар НЕ найден - удаляем запись")
            popular.delete()
            print(f"     ✅ УДАЛЕНО!")
    
    print(f"\n🎉 Очистка завершена!")
    
    # Показываем статистику после очистки
    print(f"\n📊 СТАТИСТИКА ПОСЛЕ ОЧИСТКИ:")
    print(f"PurchaseIntent записей:")
    for content_type in ['book', 'fairy_tale', 'product', 'audio']:
        count = PurchaseIntent.objects.filter(content_type=content_type).count()
        print(f"  {content_type}: {count}")
    
    print(f"\nPopularContent записей:")
    for content_type in ['book', 'fairy_tale', 'product', 'audio']:
        count = PopularContent.objects.filter(content_type=content_type).count()
        print(f"  {content_type}: {count}")

if __name__ == '__main__':
    clean_incorrect_analytics()
