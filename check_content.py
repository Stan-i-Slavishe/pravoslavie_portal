#!/usr/bin/env python
"""
Скрипт для проверки доступного контента в базе данных
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_content():
    """Проверяем какой контент доступен для создания товаров"""
    
    print("🔍 ПРОВЕРКА ДОСТУПНОГО КОНТЕНТА")
    print("=" * 50)
    
    # Проверяем книги
    try:
        from books.models import Book
        books = Book.objects.all()
        print(f"📚 КНИГИ: {books.count()} шт.")
        for book in books[:5]:  # Показываем первые 5
            print(f"   - {book.title} (ID: {book.id})")
        if books.count() > 5:
            print(f"   ... и еще {books.count() - 5} книг")
    except Exception as e:
        print(f"📚 КНИГИ: Ошибка - {e}")
    
    print()
    
    # Проверяем сказки
    try:
        from fairy_tales.models import FairyTale
        tales = FairyTale.objects.all()
        print(f"🧚‍♀️ СКАЗКИ: {tales.count()} шт.")
        for tale in tales[:5]:
            age_group = getattr(tale, 'age_group', 'Не указан')
            print(f"   - {tale.title} ({age_group}) (ID: {tale.id})")
        if tales.count() > 5:
            print(f"   ... и еще {tales.count() - 5} сказок")
    except Exception as e:
        print(f"🧚‍♀️ СКАЗКИ: Ошибка - {e}")
    
    print()
    
    # Проверяем аудио
    try:
        from audio.models import AudioTrack
        audio_tracks = AudioTrack.objects.all()
        print(f"🎧 АУДИО: {audio_tracks.count()} шт.")
        for track in audio_tracks[:5]:
            print(f"   - {track.title} (ID: {track.id})")
        if audio_tracks.count() > 5:
            print(f"   ... и еще {audio_tracks.count() - 5} треков")
    except Exception as e:
        print(f"🎧 АУДИО: Ошибка - {e}")
    
    print()
    
    # Проверяем подписки
    try:
        from subscriptions.models import Subscription
        subscriptions = Subscription.objects.all()
        print(f"📅 ПОДПИСКИ: {subscriptions.count()} шт.")
        for sub in subscriptions[:5]:
            print(f"   - {sub.name} (ID: {sub.id})")
        if subscriptions.count() > 5:
            print(f"   ... и еще {subscriptions.count() - 5} подписок")
    except Exception as e:
        print(f"📅 ПОДПИСКИ: Ошибка - {e}")
    
    print()
    
    # Проверяем уже созданные товары
    try:
        from shop.models import Product
        products = Product.objects.all()
        print(f"🛒 ТОВАРЫ: {products.count()} шт.")
        for product in products:
            content_info = ""
            if product.product_type == 'book' and product.book_id:
                content_info = f" → Книга ID: {product.book_id}"
            elif product.product_type == 'fairy_tale' and product.fairy_tale_template_id:
                content_info = f" → Сказка ID: {product.fairy_tale_template_id}"
            elif product.product_type == 'audio' and product.audio_id:
                content_info = f" → Аудио ID: {product.audio_id}"
            elif product.product_type == 'subscription' and product.subscription_id:
                content_info = f" → Подписка ID: {product.subscription_id}"
            
            print(f"   - {product.title} ({product.get_product_type_display()}){content_info}")
    except Exception as e:
        print(f"🛒 ТОВАРЫ: Ошибка - {e}")
    
    print()
    print("=" * 50)
    print("✅ Проверка завершена!")
    print()
    
    # Рекомендации
    print("💡 РЕКОМЕНДАЦИИ:")
    print("1. Если контента мало - создайте его в соответствующих разделах админки")
    print("2. Потом создавайте товары с новой улучшенной формой")
    print("3. Товары будут автоматически связываться с контентом")

if __name__ == "__main__":
    check_content()
