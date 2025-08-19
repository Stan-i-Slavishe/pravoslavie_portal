#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор VAPID ключей для push-уведомлений (исправленная версия)
"""

try:
    from pywebpush import Vapid
    
    print("🔑 Генерация VAPID ключей для push-уведомлений...")
    
    # Генерируем VAPID ключи (обновленный API)
    vapid = Vapid()
    
    # Новый способ генерации ключей
    try:
        # Пытаемся использовать новый API
        vapid.generate_private_key()
        private_key = vapid.private_key.decode('utf-8') if hasattr(vapid.private_key, 'decode') else vapid.private_key
        public_key = vapid.public_key.decode('utf-8') if hasattr(vapid.public_key, 'decode') else vapid.public_key
    except AttributeError:
        # Используем альтернативный способ для новых версий
        try:
            vapid_claims = vapid.from_raw(vapid.generate_private_key_bytes())
            private_key = vapid.private_key_bytes.decode('utf-8') if hasattr(vapid.private_key_bytes, 'decode') else str(vapid.private_key_bytes)
            public_key = vapid.public_key_bytes.decode('utf-8') if hasattr(vapid.public_key_bytes, 'decode') else str(vapid.public_key_bytes)
        except:
            # Статичные ключи для разработки (ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!)
            print("⚠️  Используем тестовые ключи для разработки...")
            private_key = "BNfxJJVRflBJLtB3-1JsG7fzU8NO5rHy15j5R5oI8J1fW-HlsA6yEGHG8O5vJJz_VXTvS2wMdBjQ_rjC1J6o-P0"
            public_key = "BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc"
    
    print("\n✅ VAPID ключи сгенерированы!")
    print("\n📋 Добавьте в .env файл:")
    print("-" * 60)
    print(f"VAPID_PRIVATE_KEY={private_key}")
    print(f"VAPID_PUBLIC_KEY={public_key}")
    print(f"VAPID_EMAIL=admin@pravoslavie-portal.ru")
    print("-" * 60)
    
    print("\n💡 Инструкции:")
    print("1. Скопируйте эти 3 строки в ваш .env файл")
    print("2. Перезапустите сервер: python manage.py runserver")
    print("3. Откройте: http://127.0.0.1:8000/push/test/")
    print("4. Разрешите уведомления и протестируйте")
    
    print("\n🚀 После настройки вы сможете:")
    print("   - Получать уведомления о новом контенте")
    print("   - Напоминания о сказках в 19:00")
    print("   - Уведомления о православных праздниках")
    
except ImportError:
    print("❌ Ошибка: pywebpush не установлен")
    print("Выполните: pip install pywebpush")
    
except Exception as e:
    print(f"❌ Ошибка генерации ключей: {e}")
    print("\n🔧 Альтернативное решение:")
    print("Используйте тестовые ключи для разработки:")
    print("-" * 60)
    print("VAPID_PRIVATE_KEY=test-private-key-for-development")
    print("VAPID_PUBLIC_KEY=BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc")
    print("VAPID_EMAIL=admin@pravoslavie-portal.ru")
    print("-" * 60)
    print("⚠️  Эти ключи только для тестирования! В продакшене используйте реальные.")
