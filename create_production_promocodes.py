#!/usr/bin/env python3
"""
Создание промокодов для продакшена
"""

import os
import django
from decimal import Decimal
from datetime import timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Discount
from django.utils import timezone

def create_production_promocodes():
    """Создаем промокоды для продакшена"""
    
    print("🎫 Создание промокодов для продакшена...")
    
    promocodes_data = [
        {
            'code': 'WELCOME10',
            'description': 'Приветственная скидка 10%',
            'discount_type': 'percentage',
            'discount_value': Decimal('10.00'),
            'min_amount': Decimal('500.00'),
        },
        {
            'code': 'SAVE15',
            'description': 'Скидка 15% на заказы от 1000₽',
            'discount_type': 'percentage',
            'discount_value': Decimal('15.00'),
            'min_amount': Decimal('1000.00'),
        },
        {
            'code': 'BOOK200',
            'description': 'Скидка 200₽ на книги',
            'discount_type': 'fixed',
            'discount_value': Decimal('200.00'),
            'min_amount': Decimal('800.00'),
        }
    ]
    
    for data in promocodes_data:
        # Удаляем если существует
        Discount.objects.filter(code=data['code']).delete()
        
        # Создаем новый
        discount = Discount.objects.create(
            code=data['code'],
            description=data['description'],
            discount_type=data['discount_type'],
            discount_value=data['discount_value'],
            min_amount=data['min_amount'],
            max_uses=100,
            uses_count=0,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=90),
            is_active=True
        )
        
        suffix = '%' if data['discount_type'] == 'percentage' else '₽'
        print(f"✅ {discount.code}: {discount.discount_value}{suffix} (мин. {discount.min_amount}₽)")

    # Удаляем отладочный промокод если он есть
    debug_count = Discount.objects.filter(code='DEBUG15').count()
    if debug_count > 0:
        Discount.objects.filter(code='DEBUG15').delete()
        print(f"🗑️  Удален отладочный промокод DEBUG15")

if __name__ == '__main__':
    print("🚀 Настройка промокодов для продакшена\n")
    create_production_promocodes()
    print("\n✅ Готово! Промокоды созданы для продакшена.")
