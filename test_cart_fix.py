#!/usr/bin/env python
"""
Тестовый скрипт для проверки исправлений корзины
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from shop.models import Product, Cart, CartItem
from books.models import Book

User = get_user_model()

def test_cart_operations():
    """Тест операций с корзиной"""
    print("🧪 Запуск тестов корзины...")
    
    # Создаем тестового пользователя
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print("✅ Тестовый пользователь создан")
    
    # Создаем тестовую книгу и продукт
    book = Book.objects.first()
    if not book:
        print("❌ Нет книг в системе для тестирования")
        return
    
    product = Product.objects.filter(content_object=book).first()
    if not product:
        print("❌ Нет продуктов в системе для тестирования")
        return
    
    print(f"📚 Используем продукт: {product.title}")
    
    # Создаем клиента и логинимся
    client = Client()
    client.login(username='testuser', password='testpass123')
    print("✅ Пользователь авторизован")
    
    # Создаем корзину и добавляем товар
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2
    )
    print(f"✅ Товар добавлен в корзину: {cart_item.quantity} шт.")
    
    # Тестируем страницу корзины
    response = client.get(reverse('shop:cart'))
    print(f"📄 Страница корзины: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Страница корзины загружается")
        
        # Проверяем наличие кнопки удаления в HTML
        if 'remove-btn' in response.content.decode():
            print("✅ Кнопка удаления найдена в HTML")
        else:
            print("❌ Кнопка удаления НЕ найдена в HTML")
            
        # Проверяем наличие элементов корзины
        if f'{product.title}' in response.content.decode():
            print("✅ Товар отображается в корзине")
        else:
            print("❌ Товар НЕ отображается в корзине")
    else:
        print("❌ Ошибка загрузки страницы корзины")
    
    # Тестируем удаление товара
    response = client.post(
        reverse('shop:update_cart_item', kwargs={'item_id': cart_item.id}),
        {'action': 'remove'}
    )
    print(f"🗑️ Удаление товара: {response.status_code}")
    
    if response.status_code == 302:  # Редирект обратно в корзину
        print("✅ Удаление товара работает")
        
        # Проверяем, что товар действительно удален
        if not CartItem.objects.filter(id=cart_item.id).exists():
            print("✅ Товар действительно удален из корзины")
        else:
            print("❌ Товар НЕ удален из корзины")
    else:
        print("❌ Ошибка при удалении товара")
    
    # Очистка
    user.delete()
    print("🧹 Тестовые данные очищены")
    print("\n🎉 Тестирование завершено!")

if __name__ == '__main__':
    test_cart_operations()
