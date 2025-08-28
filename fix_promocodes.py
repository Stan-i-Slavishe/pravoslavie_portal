#!/usr/bin/env python3
"""
Скрипт для исправления промокодов и отладки
"""

import os
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Discount, Cart
from django.utils import timezone
from django.contrib.auth.models import User

def check_and_create_promocodes():
    """Проверяем и создаем промокоды"""
    
    print("🔍 Проверка существующих промокодов...")
    existing_discounts = Discount.objects.all()
    print(f"Найдено промокодов: {existing_discounts.count()}")
    
    for discount in existing_discounts:
        print(f"  - {discount.code}: {discount.discount_value}{'%' if discount.discount_type == 'percentage' else '₽'} (активен: {discount.is_active})")
    
    # Создаем DEBUG15 если его нет
    debug15, created = Discount.objects.get_or_create(
        code='DEBUG15',
        defaults={
            'description': 'Отладочная скидка 15%',
            'discount_type': 'percentage',
            'discount_value': Decimal('15.00'),
            'min_amount': Decimal('0.00'),  # Без минимальной суммы для тестов
            'max_uses': 1000,
            'uses_count': 0,
            'valid_from': timezone.now() - timedelta(days=1),
            'valid_until': timezone.now() + timedelta(days=365),
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Создан промокод DEBUG15")
    else:
        print(f"ℹ️  Промокод DEBUG15 уже существует")
        # Обновляем его на всякий случай
        debug15.is_active = True
        debug15.min_amount = Decimal('0.00')
        debug15.valid_until = timezone.now() + timedelta(days=365)
        debug15.save()
        print(f"🔄 Промокод DEBUG15 обновлен")
    
    # Проверяем валидность DEBUG15
    is_valid, message = debug15.is_valid()
    print(f"Статус DEBUG15: {'✅ Валиден' if is_valid else '❌ Невалиден'} - {message}")
    
    return debug15

def test_discount_application():
    """Тестируем применение скидки"""
    
    print("\n🧪 Тестирование применения скидки...")
    
    # Находим первого пользователя или создаем тестового
    user = User.objects.first()
    if not user:
        print("❌ Пользователи не найдены")
        return
    
    print(f"👤 Тестируем для пользователя: {user.username}")
    
    # Получаем корзину
    cart, created = Cart.objects.get_or_create(user=user)
    print(f"🛒 Корзина: {cart.total_items} товаров, {cart.total_price}₽")
    
    if cart.total_items == 0:
        print("⚠️  Корзина пуста - добавьте товары для тестирования")
        return
    
    # Получаем промокод
    try:
        discount = Discount.objects.get(code='DEBUG15')
        print(f"🎫 Промокод найден: {discount.code}")
        
        # Проверяем валидность
        is_valid, error_message = discount.is_valid()
        print(f"Валидность: {'✅' if is_valid else '❌'} {error_message}")
        
        if is_valid:
            # Проверяем минимальную сумму
            if cart.total_price >= discount.min_amount:
                # Рассчитываем скидку
                discount_amount = discount.calculate_discount(cart.total_price)
                print(f"💰 Рассчитанная скидка: {discount_amount}₽")
                
                # Применяем скидку
                cart.apply_discount('DEBUG15', discount_amount)
                cart.refresh_from_db()
                
                print(f"✅ Скидка применена!")
                print(f"   Промокод в корзине: '{cart.applied_discount_code}'")
                print(f"   Размер скидки: {cart.discount_amount}₽")
                print(f"   Итоговая цена: {cart.total_price_with_discount}₽")
                print(f"   has_discount: {cart.has_discount}")
                
            else:
                print(f"❌ Сумма корзины {cart.total_price}₽ меньше минимальной {discount.min_amount}₽")
        
    except Discount.DoesNotExist:
        print("❌ Промокод DEBUG15 не найден")

def debug_cart_discount_fields():
    """Отладка полей скидки в корзине"""
    
    print("\n🔧 Отладка полей корзины...")
    
    user = User.objects.first()
    if not user:
        return
    
    cart, created = Cart.objects.get_or_create(user=user)
    
    print(f"Корзина ID: {cart.id}")
    print(f"applied_discount_code: '{cart.applied_discount_code}' (тип: {type(cart.applied_discount_code)})")
    print(f"discount_amount: {cart.discount_amount} (тип: {type(cart.discount_amount)})")
    print(f"total_price: {cart.total_price}")
    print(f"total_price_with_discount: {cart.total_price_with_discount}")
    print(f"has_discount: {cart.has_discount}")

if __name__ == '__main__':
    print("🚀 Исправление и отладка промокодов\n")
    
    # 1. Проверяем и создаем промокоды
    debug15 = check_and_create_promocodes()
    
    # 2. Тестируем применение скидки
    test_discount_application()
    
    # 3. Отладка полей корзины
    debug_cart_discount_fields()
    
    print("\n✅ Отладка завершена!")
    print("\n💡 Для проверки зайдите на /shop/checkout/ и примените промокод DEBUG15")
