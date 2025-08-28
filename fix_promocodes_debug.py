#!/usr/bin/env python3
"""
ИСПРАВЛЕНИЕ ПРОМОКОДОВ
Запустите этот скрипт для создания промокода DEBUG15 и тестирования
"""

import os
import sys

# Добавляем путь к проекту
project_path = r'E:\pravoslavie_portal'
sys.path.append(project_path)
os.chdir(project_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

from shop.models import Discount, Cart, Product, CartItem

def create_debug_promocode():
    """Создаем отладочный промокод DEBUG15"""
    
    print("🎫 Создание промокода DEBUG15...")
    
    # Удаляем старый если есть
    old_count = Discount.objects.filter(code='DEBUG15').count()
    if old_count > 0:
        Discount.objects.filter(code='DEBUG15').delete()
        print(f"   Удален старый промокод (было {old_count})")
    
    # Создаем новый
    discount = Discount.objects.create(
        code='DEBUG15',
        description='Отладочная скидка 15%',
        discount_type='percentage',
        discount_value=Decimal('15.00'),
        min_amount=Decimal('0.00'),  # Без минимальной суммы для тестов
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
    print(f"   Действует до: {discount.valid_until.strftime('%d.%m.%Y')}")
    
    # Проверяем валидность
    is_valid, message = discount.is_valid()
    print(f"   Статус: {'✅ Валиден' if is_valid else '❌ Невалиден'} - {message}")
    
    return discount

def test_cart_with_promocode():
    """Тестируем корзину с промокодом"""
    
    print("\n🛒 Тестирование корзины...")
    
    # Находим первого пользователя
    user = User.objects.first()
    if not user:
        print("❌ Пользователи не найдены. Создайте пользователя через админку.")
        return None
    
    print(f"👤 Пользователь: {user.username}")
    
    # Получаем или создаем корзину
    cart, created = Cart.objects.get_or_create(user=user)
    print(f"🛒 Корзина: {cart.total_items} товаров на сумму {cart.total_price}₽")
    
    # Если корзина пуста, добавляем тестовый товар
    if cart.total_items == 0:
        print("   Корзина пуста, добавляем тестовый товар...")
        
        # Находим любой товар
        product = Product.objects.filter(is_active=True, price__gt=0).first()
        if product:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )
            cart.refresh_from_db()
            print(f"   Добавлен товар: {product.title} ({product.price}₽)")
            print(f"   Новая сумма корзины: {cart.total_price}₽")
        else:
            print("   ❌ Нет доступных товаров для добавления")
            return None
    
    # Применяем промокод
    discount = Discount.objects.get(code='DEBUG15')
    
    # Рассчитываем скидку
    discount_amount = discount.calculate_discount(cart.total_price)
    
    # Применяем к корзине
    cart.apply_discount('DEBUG15', discount_amount)
    cart.refresh_from_db()
    
    print(f"\n💰 Результат применения промокода:")
    print(f"   Исходная сумма: {cart.total_price}₽")
    print(f"   Размер скидки: {cart.discount_amount}₽")
    print(f"   Итоговая сумма: {cart.total_price_with_discount}₽")
    print(f"   Промокод в корзине: '{cart.applied_discount_code}'")
    print(f"   has_discount: {cart.has_discount}")
    
    return cart

def check_system_status():
    """Проверяем состояние системы"""
    
    print("\n🔍 Проверка системы...")
    
    # Проверяем пользователей
    users_count = User.objects.count()
    print(f"👥 Пользователей в системе: {users_count}")
    
    # Проверяем товары
    products_count = Product.objects.filter(is_active=True, price__gt=0).count()
    print(f"📦 Активных платных товаров: {products_count}")
    
    # Проверяем промокоды
    discounts_count = Discount.objects.filter(is_active=True).count()
    print(f"🎫 Активных промокодов: {discounts_count}")
    
    # Проверяем корзины
    carts_count = Cart.objects.count()
    print(f"🛒 Корзин в системе: {carts_count}")
    
    return users_count > 0 and products_count > 0

def main():
    """Основная функция"""
    
    print("🚀 ИСПРАВЛЕНИЕ ПРОМОКОДОВ DEBUG15")
    print("=" * 50)
    
    # Проверяем систему
    if not check_system_status():
        print("\n❌ Система не готова:")
        print("   - Убедитесь, что есть зарегистрированные пользователи")
        print("   - Убедитесь, что есть активные товары в магазине")
        return
    
    # Создаем промокод
    discount = create_debug_promocode()
    
    # Тестируем корзину
    cart = test_cart_with_promocode()
    
    if cart:
        print("\n✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("\n📋 Инструкции для тестирования:")
        print("1. Откройте http://127.0.0.1:8000/shop/checkout/")
        print("2. Введите промокод: DEBUG15")
        print("3. Нажмите 'Применить'")
        print("4. Проверьте, что скидка применилась")
        print("\n💡 Если возникают проблемы:")
        print("   - Убедитесь, что вы авторизованы")
        print("   - Убедитесь, что в корзине есть товары")
        print("   - Проверьте консоль браузера на ошибки")
    else:
        print("\n❌ Не удалось протестировать корзину")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Убедитесь, что:")
        print("   - Django сервер не запущен (python manage.py runserver)")
        print("   - Путь к проекту правильный")
        print("   - База данных доступна")
