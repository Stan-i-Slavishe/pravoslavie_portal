# fix_existing_purchases.py
# Скрипт для исправления существующих покупок без заказов

import os
import django
from collections import defaultdict

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Product, Order, OrderItem, Purchase
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def fix_purchases_without_orders():
    """Исправить покупки без связанных заказов"""
    
    print("🔧 ИСПРАВЛЕНИЕ ПОКУПОК БЕЗ ЗАКАЗОВ")
    print("=" * 50)
    
    # Находим покупки без заказов
    purchases_without_orders = Purchase.objects.filter(order__isnull=True)
    
    if not purchases_without_orders.exists():
        print("✅ Все покупки имеют связанные заказы")
        return
    
    print(f"⚠️  Найдено покупок без заказов: {purchases_without_orders.count()}")
    
    # Группируем покупки по пользователям
    purchases_by_user = defaultdict(list)
    
    for purchase in purchases_without_orders:
        purchases_by_user[purchase.user].append(purchase)
    
    print(f"👥 Пользователей с проблемными покупками: {len(purchases_by_user)}")
    
    fixed_count = 0
    
    # Создаем заказы для каждого пользователя
    for user, user_purchases in purchases_by_user.items():
        try:
            print(f"\n🔧 Исправляем покупки для пользователя: {user.username}")
            print(f"   Покупок: {len(user_purchases)}")
            
            # Создаем заказ
            total_amount = sum(p.product.price for p in user_purchases)
            
            order = Order.objects.create(
                user=user,
                email=user.email,
                first_name=user.first_name or 'Пользователь',
                last_name=user.last_name or 'Сайта',
                phone='',
                total_amount=total_amount,
                status='completed',
                paid_at=user_purchases[0].purchased_at,
                completed_at=user_purchases[0].purchased_at,
                payment_method='legacy_fix',
                payment_id=f'legacy_{user.id}_{timezone.now().timestamp()}',
            )
            
            print(f"   ✅ Создан заказ #{order.short_id}")
            
            # Создаем элементы заказа и связываем покупки
            for purchase in user_purchases:
                OrderItem.objects.create(
                    order=order,
                    product=purchase.product,
                    product_title=purchase.product.title,
                    product_price=purchase.product.price,
                    quantity=1,
                )
                
                # Обновляем покупку
                purchase.order = order
                purchase.save()
                
                fixed_count += 1
                print(f"   📦 Исправлена покупка: {purchase.product.title}")
            
        except Exception as e:
            print(f"   ❌ Ошибка для пользователя {user.username}: {e}")
            continue
    
    print(f"\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print(f"Исправлено покупок: {fixed_count}")
    print("=" * 50)

def verify_fix():
    """Проверить результат исправления"""
    
    print("\n🔍 ПРОВЕРКА РЕЗУЛЬТАТА ИСПРАВЛЕНИЯ")
    print("=" * 30)
    
    # Проверяем покупки без заказов
    purchases_without_orders = Purchase.objects.filter(order__isnull=True)
    print(f"Покупок без заказов: {purchases_without_orders.count()}")
    
    # Проверяем общую статистику
    total_purchases = Purchase.objects.count()
    total_orders = Order.objects.count()
    
    print(f"Всего покупок: {total_purchases}")
    print(f"Всего заказов: {total_orders}")
    
    # Проверяем статусы заказов
    for status, name in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status).count()
        if count > 0:
            print(f"Заказов со статусом '{name}': {count}")

if __name__ == '__main__':
    fix_purchases_without_orders()
    verify_fix()
