# diagnose_orders_issue.py
# Быстрая диагностика проблемы с заказами и покупками

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from shop.models import Order, Purchase, Product
from books.models import Book

def diagnose_current_state():
    """Диагностировать текущее состояние системы"""
    
    print("🔍 ДИАГНОСТИКА СИСТЕМЫ ЗАКАЗОВ И ПОКУПОК")
    print("=" * 50)
    
    # Проверяем пользователей
    users_count = User.objects.count()
    print(f"👥 Пользователей в системе: {users_count}")
    
    if users_count > 0:
        # Берем первого пользователя (вероятно, администратор)
        user = User.objects.first()
        print(f"🔍 Проверяем пользователя: {user.username}")
        
        # Проверяем заказы этого пользователя
        orders = Order.objects.filter(user=user)
        print(f"📋 Заказов у пользователя: {orders.count()}")
        
        if orders.exists():
            for order in orders:
                print(f"  🧾 Заказ #{order.short_id}")
                print(f"      Статус: {order.get_status_display()}")
                print(f"      Дата: {order.created_at}")
                print(f"      Товаров: {order.items.count()}")
        else:
            print("  ❌ Заказов не найдено")
        
        # Проверяем покупки этого пользователя
        purchases = Purchase.objects.filter(user=user)
        print(f"📦 Покупок у пользователя: {purchases.count()}")
        
        if purchases.exists():
            for purchase in purchases:
                print(f"  📚 Покупка: {purchase.product.title}")
                print(f"      Заказ: #{purchase.order.short_id}")
                print(f"      Дата: {purchase.purchased_at}")
        else:
            print("  ❌ Покупок не найдено")
    
    # Общая статистика
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"  Всего заказов: {Order.objects.count()}")
    print(f"  Оплаченных заказов: {Order.objects.filter(status__in=['paid', 'completed']).count()}")
    print(f"  Всего покупок: {Purchase.objects.count()}")
    print(f"  Товаров в магазине: {Product.objects.filter(is_active=True).count()}")
    print(f"  Книг в системе: {Book.objects.count()}")
    
    # Проверяем связь между заказами и покупками
    print(f"\n🔗 ПРОВЕРКА СВЯЗЕЙ:")
    
    paid_orders = Order.objects.filter(status__in=['paid', 'completed'])
    print(f"  Оплаченных заказов: {paid_orders.count()}")
    
    for order in paid_orders[:5]:  # Проверяем первые 5
        purchases_for_order = Purchase.objects.filter(order=order)
        print(f"    Заказ #{order.short_id} -> покупок: {purchases_for_order.count()}")
        
        if purchases_for_order.count() == 0:
            print(f"      ⚠️ ПРОБЛЕМА: Заказ оплачен, но покупки не созданы!")
            
            # Пробуем исправить
            print(f"      🔧 Попытка исправления...")
            from shop.views import complete_order
            try:
                complete_order(order)
                print(f"      ✅ Исправлено! Создано покупок: {Purchase.objects.filter(order=order).count()}")
            except Exception as e:
                print(f"      ❌ Ошибка исправления: {e}")

if __name__ == '__main__':
    diagnose_current_state()
