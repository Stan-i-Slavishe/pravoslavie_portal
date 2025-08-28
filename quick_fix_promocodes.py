#!/usr/bin/env python3
"""
Быстрое исправление промокодов - создаем DEBUG15 и тестируем
"""

import os
import django
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Discount, Cart
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def create_debug_promocode():
    """Создаем отладочный промокод DEBUG15"""
    
    # Удаляем старый если есть
    Discount.objects.filter(code='DEBUG15').delete()
    
    # Создаем новый
    discount = Discount.objects.create(
        code='DEBUG15',
        description='Отладочная скидка 15%',
        discount_type='percentage',
        discount_value=Decimal('15.00'),
        min_amount=Decimal('0.00'),  # Без минимальной суммы
        max_uses=1000,
        uses_count=0,
        valid_from=timezone.now() - timedelta(days=1),
        valid_until=timezone.now() + timedelta(days=365),
        is_active=True
    )
    
    print(f"✅ Создан промокод: {discount.code}")
    print(f"   Скидка: {discount.discount_value}%")
    print(f"   Минимальная сумма: {discount.min_amount}₽")
    print(f"   Активен: {discount.is_active}")
    
    # Проверяем валидность
    is_valid, message = discount.is_valid()
    print(f"   Статус: {'✅ Валиден' if is_valid else '❌ Невалиден'} - {message}")
    
    return discount

def test_cart_discount():
    """Тестируем применение скидки к корзине"""
    
    print("\n🧪 Тестирование корзины...")
    
    # Находим первого пользователя
    user = User.objects.first()
    if not user:
        print("❌ Пользователи не найдены")
        return
    
    print(f"👤 Пользователь: {user.username}")
    
    # Получаем корзину
    cart, created = Cart.objects.get_or_create(user=user)
    print(f"🛒 Корзина: {cart.total_items} товаров, {cart.total_price}₽")
    
    if cart.total_items == 0:
        print("⚠️  Корзина пуста")
        return
    
    # Применяем скидку
    discount = Discount.objects.get(code='DEBUG15')
    discount_amount = discount.calculate_discount(cart.total_price)
    
    cart.apply_discount('DEBUG15', discount_amount)
    cart.refresh_from_db()
    
    print(f"💰 Применена скидка: {discount_amount}₽")
    print(f"💳 Итоговая цена: {cart.total_price_with_discount}₽")
    print(f"🎯 has_discount: {cart.has_discount}")

if __name__ == '__main__':
    print("🚀 Быстрое исправление промокодов\n")
    
    # Создаем промокод
    discount = create_debug_promocode()
    
    # Тестируем корзину
    test_cart_discount()
    
    print("\n✅ Готово! Теперь промокод DEBUG15 должен работать на /shop/checkout/")
