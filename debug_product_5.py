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

from shop.models import Product
from analytics.models import PurchaseIntent
from fairy_tales.models import FairyTaleTemplate

print("🛍️ ВСЕ ТОВАРЫ В МАГАЗИНЕ:")
print("=" * 50)
products = Product.objects.all()
for product in products:
    print(f"ID: {product.id} | Название: {product.name} | Тип: {product.product_type}")

print(f"\nВсего товаров: {products.count()}")

print("\n🔍 ПРОВЕРЯЕМ ТОВАР С ID=5:")
print("=" * 50)
try:
    product_5 = Product.objects.get(id=5)
    print(f"✅ Товар найден: {product_5.name}")
    print(f"   Тип: {product_5.product_type}")
    print(f"   Описание: {product_5.description[:100] if product_5.description else 'Нет описания'}...")
    print(f"   Цена: {product_5.price}")
    print(f"   Создан: {product_5.created_at}")
except Product.DoesNotExist:
    print("❌ Товар с ID=5 НЕ СУЩЕСТВУЕТ в базе данных")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n📊 АНАЛИТИКА ПО PRODUCT #5:")
print("=" * 50)
try:
    product_5_analytics = PurchaseIntent.objects.filter(content_type='product', object_id=5)
    print(f"Кликов по Product #5: {product_5_analytics.count()}")

    for intent in product_5_analytics:
        print(f"  - Клик: {intent.clicked_at}")
        print(f"    Тип кнопки: {intent.button_type}")
        print(f"    URL: {intent.page_url}")
        print(f"    User Agent: {intent.user_agent[:50]}...")
        print()
except Exception as e:
    print(f"❌ Ошибка в аналитике: {e}")

print("\n🧚‍♀️ ПРОВЕРЯЕМ СКАЗКИ (ваша гипотеза про аудио):")
print("=" * 50)
try:
    fairy_tales = FairyTaleTemplate.objects.all()
    print(f"Всего сказок: {fairy_tales.count()}")
    
    for tale in fairy_tales:
        print(f"ID: {tale.id} | Название: {tale.title}")
        print(f"   Аудио опции: {tale.has_audio_option if hasattr(tale, 'has_audio_option') else 'Неизвестно'}")
        print(f"   Связанный товар: {tale.shop_product.id if hasattr(tale, 'shop_product') and tale.shop_product else 'Нет'}")
        print()
        
    # Проверяем сказку с ID=5
    if fairy_tales.filter(id=5).exists():
        tale_5 = fairy_tales.get(id=5)
        print(f"🎯 СКАЗКА #5: {tale_5.title}")
        if hasattr(tale_5, 'shop_product') and tale_5.shop_product:
            print(f"   Связана с товаром ID: {tale_5.shop_product.id}")
    
except Exception as e:
    print(f"❌ Ошибка с сказками: {e}")

print("\n🔍 ПОИСК ССЫЛОК НА ID=5 В ШАБЛОНАХ:")
print("=" * 50)
print("Нужно проверить шаблоны на наличие data-object-id='5'")
