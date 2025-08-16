#!/usr/bin/env python3
"""
Скрипт для создания тестового промокода
"""

import os
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Discount
from django.utils import timezone

def create_test_promocode():
    """Создаем тестовый промокод"""
    
    # Удаляем старый промокод если есть
    Discount.objects.filter(code='TEST15').delete()
    
    # Создаем новый промокод
    discount = Discount.objects.create(
        code='TEST15',
        description='Тестовая скидка 15%',
        discount_type='percentage',
        discount_value=Decimal('15.00'),
        min_amount=Decimal('100.00'),
        max_uses=100,
        uses_count=0,
        valid_from=timezone.now(),
        valid_until=timezone.now() + timedelta(days=30),
        is_active=True
    )
    
    print("✅ Тестовый промокод создан:")
    print(f"   Код: {discount.code}")
    print(f"   Скидка: {discount.discount_value}%")
    print(f"   Минимальная сумма: {discount.min_amount}₽")
    print(f"   Действует до: {discount.valid_until.strftime('%d.%m.%Y')}")
    
    # Создаем еще несколько примеров
    promocodes_data = [
        {
            'code': 'SAVE200',
            'description': 'Скидка 200 рублей',
            'discount_type': 'fixed',
            'discount_value': Decimal('200.00'),
            'min_amount': Decimal('1000.00'),
        },
        {
            'code': 'WELCOME10',
            'description': 'Приветственная скидка 10%',
            'discount_type': 'percentage', 
            'discount_value': Decimal('10.00'),
            'min_amount': Decimal('500.00'),
        }
    ]
    
    for data in promocodes_data:
        # Удаляем если существует
        Discount.objects.filter(code=data['code']).delete()
        
        # Создаем новый
        promo = Discount.objects.create(
            code=data['code'],
            description=data['description'],
            discount_type=data['discount_type'],
            discount_value=data['discount_value'],
            min_amount=data['min_amount'],
            max_uses=50,
            uses_count=0,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=30),
            is_active=True
        )
        
        suffix = '%' if data['discount_type'] == 'percentage' else '₽'
        print(f"✅ Промокод {promo.code}: {promo.discount_value}{suffix}")

if __name__ == '__main__':
    print("🚀 Создание тестовых промокодов...")
    create_test_promocode()
    print("\n🎯 Для тестирования используйте промокоды:")
    print("   TEST15 - скидка 15% (мин. сумма 100₽)")
    print("   SAVE200 - скидка 200₽ (мин. сумма 1000₽)")
    print("   WELCOME10 - скидка 10% (мин. сумма 500₽)")
