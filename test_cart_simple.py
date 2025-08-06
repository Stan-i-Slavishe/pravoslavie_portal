#!/usr/bin/env python
"""
Быстрая проверка функций корзины
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

def test_cart_delete_button():
    """Проверяем что есть товары в системе для тестирования"""
    print("🧪 Проверка системы корзины...")
    
    # Проверяем наличие продуктов
    products_count = Product.objects.filter(is_active=True).count()
    print(f"📦 Активных товаров в системе: {products_count}")
    
    if products_count == 0:
        print("❌ Нет товаров для тестирования")
        return False
    
    # Проверяем наличие пользователей
    users_count = User.objects.count()
    print(f"👥 Пользователей в системе: {users_count}")
    
    # Проверяем корзины
    carts_count = Cart.objects.count()
    print(f"🛒 Корзин в системе: {carts_count}")
    
    # Проверяем элементы корзин
    cart_items_count = CartItem.objects.count()
    print(f"📱 Элементов в корзинах: {cart_items_count}")
    
    if cart_items_count > 0:
        print("✅ В системе есть товары в корзинах - можно тестировать удаление")
        
        # Показываем примеры корзин
        for cart_item in CartItem.objects.all()[:3]:
            print(f"   - {cart_item.product.title} (x{cart_item.quantity}) у {cart_item.cart.user.username}")
    else:
        print("ℹ️ Корзины пустые - добавьте товары для тестирования")
    
    print("\n🔍 Проверьте сами:")
    print("1. Авторизуйтесь на сайте")
    print("2. Добавьте товары в корзину")
    print("3. Перейдите в корзину: http://127.0.0.1:8000/shop/cart/")
    print("4. Найдите красную кнопку с иконкой корзины")
    print("5. Попробуйте удалить товар")
    
    return True

if __name__ == '__main__':
    test_cart_delete_button()
