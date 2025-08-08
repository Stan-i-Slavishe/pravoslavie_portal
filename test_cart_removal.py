import os
import sys
import django

# Добавляем путь проекта
sys.path.append(r'E:\pravoslavie_portal')

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Cart, CartItem, Product
from django.contrib.auth.models import User

def test_cart_removal():
    """Тестирует функцию удаления из корзины"""
    
    print("🗑️ ТЕСТИРОВАНИЕ ФУНКЦИИ УДАЛЕНИЯ ИЗ КОРЗИНЫ")
    print("=" * 60)
    
    # 1. Проверяем существующие корзины
    carts = Cart.objects.all()
    print(f"📊 Найдено корзин: {carts.count()}")
    
    for cart in carts:
        items = cart.items.all()
        print(f"\n👤 Пользователь: {cart.user.username}")
        print(f"   🛒 Товаров в корзине: {items.count()}")
        
        for item in items:
            print(f"      📦 {item.product.title} x{item.quantity} = {item.total_price}₽")
            print(f"         ID элемента: {item.id}")
    
    # 2. Проверяем URL удаления
    print("\n🔗 ПРОВЕРКА URL:")
    from django.urls import reverse
    try:
        remove_url = reverse('shop:remove_from_cart')
        print(f"   ✅ URL удаления: {remove_url}")
    except Exception as e:
        print(f"   ❌ Ошибка URL: {e}")
    
    # 3. Проверяем функцию в views
    print("\n🔧 ПРОВЕРКА ФУНКЦИИ remove_from_cart:")
    try:
        from shop.views import remove_from_cart
        print("   ✅ Функция remove_from_cart найдена")
    except ImportError as e:
        print(f"   ❌ Функция не найдена: {e}")
    
    print("\n📋 ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ:")
    print("1. Откройте корзину: http://127.0.0.1:8000/shop/cart/")
    print("2. Нажмите кнопку удаления (иконка корзины)")
    print("3. Подтвердите удаление")
    print("4. Проверьте:")
    print("   - Появилось ли подтверждение?")
    print("   - Удалился ли товар?")
    print("   - Обновился ли счетчик корзины?")
    
    print("\n🔍 ОТЛАДКА (если не работает):")
    print("- Откройте консоль браузера (F12)")
    print("- Проверьте ошибки JavaScript")
    print("- Убедитесь, что CSRF токен передается")
    print("- Проверьте, что запрос идет на /shop/remove-from-cart/")
    
    return carts.count()

def create_test_cart():
    """Создает тестовую корзину для проверки"""
    
    print(f"\n🧪 СОЗДАНИЕ ТЕСТОВОЙ КОРЗИНЫ")
    print("=" * 40)
    
    # Найдем тестового пользователя
    try:
        user = User.objects.get(username='test_cart_user')
    except User.DoesNotExist:
        print("❌ Тестовый пользователь не найден. Создайте его:")
        print("   python fix_book_pricing.py")
        return
    
    # Найдем активные товары
    products = Product.objects.filter(is_active=True)[:2]
    if products.count() == 0:
        print("❌ Нет активных товаров")
        return
    
    # Создаем корзину
    cart, created = Cart.objects.get_or_create(user=user)
    
    if created:
        print(f"✅ Создана новая корзина для {user.username}")
    else:
        print(f"📝 Используем существующую корзину {user.username}")
    
    # Добавляем товары
    for product in products:
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if item_created:
            print(f"✅ Добавлен товар: {product.title}")
        else:
            print(f"📝 Товар уже в корзине: {product.title}")
    
    print(f"\n📊 Итого в корзине: {cart.total_items} товаров на {cart.total_price}₽")

if __name__ == "__main__":
    print("🚀 ДИАГНОСТИКА УДАЛЕНИЯ ИЗ КОРЗИНЫ")
    
    try:
        cart_count = test_cart_removal()
        
        if cart_count == 0:
            create_test_cart()
        
        print("\n🎯 ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ:")
        print("✅ Исправлен JavaScript код удаления")
        print("✅ Добавлена правильная обработка CSRF токена")
        print("✅ Добавлены функции showToast и getCookie")
        print("✅ Улучшена обработка ошибок")
        
        print("\n🔄 ДЛЯ ПРИМЕНЕНИЯ ИЗМЕНЕНИЙ:")
        print("1. Обновите страницу корзины")
        print("2. Попробуйте удалить товар")
        print("3. Удаление должно работать без ошибок 500")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
