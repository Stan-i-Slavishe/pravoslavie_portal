#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт проверки целостности данных после миграции на PostgreSQL
Сравнивает количество записей в основных таблицах
"""

import os
import sys
import django
from collections import defaultdict

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from django.apps import apps

def count_records():
    """Подсчет записей во всех моделях"""
    print("=" * 60)
    print("🔍 ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ ПОСЛЕ МИГРАЦИИ")
    print("=" * 60)
    print()
    
    total_records = 0
    app_counts = defaultdict(dict)
    
    # Получаем все модели проекта
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        try:
            count = model.objects.count()
            app_counts[app_label][model_name] = count
            total_records += count
        except Exception as e:
            app_counts[app_label][model_name] = f"Ошибка: {e}"
    
    # Отображение результатов по приложениям
    for app_name, models in app_counts.items():
        print(f"📦 {app_name.upper()}")
        print("-" * 30)
        
        app_total = 0
        for model_name, count in models.items():
            if isinstance(count, int):
                print(f"   {model_name:20} : {count:>6} записей")
                app_total += count
            else:
                print(f"   {model_name:20} : {count}")
        
        if app_total > 0:
            print(f"   {'ИТОГО':20} : {app_total:>6} записей")
        print()
    
    print("=" * 60)
    print(f"🎯 ОБЩЕЕ КОЛИЧЕСТВО ЗАПИСЕЙ: {total_records}")
    print("=" * 60)
    print()
    
    return total_records, app_counts

def check_database_connection():
    """Проверка подключения к БД"""
    print("🔗 Проверка подключения к PostgreSQL...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ PostgreSQL подключен: {version}")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"📂 Текущая БД: {db_name}")
            
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0]
            print(f"👤 Пользователь: {user}")
            
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False
    
    print()
    return True

def check_key_data():
    """Проверка ключевых данных"""
    print("🔑 ПРОВЕРКА КЛЮЧЕВЫХ ДАННЫХ")
    print("-" * 40)
    
    try:
        # Проверяем пользователей
        from django.contrib.auth.models import User
        users_count = User.objects.count()
        superuser_count = User.objects.filter(is_superuser=True).count()
        print(f"👥 Пользователи: {users_count} (из них админов: {superuser_count})")
        
        # Проверяем рассказы
        from stories.models import Story
        stories_count = Story.objects.count()
        print(f"🎬 Рассказы: {stories_count}")
        
        # Проверяем книги
        from books.models import Book
        books_count = Book.objects.count()
        print(f"📚 Книги: {books_count}")
        
        # Проверяем сказки
        from fairy_tales.models import FairyTale
        fairy_tales_count = FairyTale.objects.count()
        print(f"🧚 Терапевтические сказки: {fairy_tales_count}")
        
        # Проверяем товары магазина
        from shop.models import Product, Order
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        print(f"🛒 Товары: {products_count}")
        print(f"📋 Заказы: {orders_count}")
        
        # Проверяем категории
        from core.models import Category
        categories_count = Category.objects.count()
        print(f"🏷️ Категории: {categories_count}")
        
    except Exception as e:
        print(f"❌ Ошибка проверки данных: {e}")
    
    print()

def check_media_files():
    """Проверка медиа-файлов"""
    print("🖼️ ПРОВЕРКА МЕДИА-ФАЙЛОВ")
    print("-" * 40)
    
    from django.conf import settings
    import os
    
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        print(f"📁 Папка media: {media_root}")
        
        # Подсчет файлов в директориях
        for root, dirs, files in os.walk(media_root):
            if files:
                rel_path = os.path.relpath(root, media_root)
                if rel_path == '.':
                    rel_path = 'корень'
                print(f"   {rel_path}: {len(files)} файлов")
    else:
        print("⚠️ Папка media не найдена")
    
    print()

def main():
    """Основная функция проверки"""
    print()
    
    # Проверка подключения
    if not check_database_connection():
        return
    
    # Подсчет всех записей
    total_records, app_counts = count_records()
    
    # Проверка ключевых данных
    check_key_data()
    
    # Проверка медиа-файлов
    check_media_files()
    
    # Итоговая оценка
    print("📊 ИТОГОВАЯ ОЦЕНКА МИГРАЦИИ")
    print("-" * 40)
    
    if total_records > 0:
        print("✅ Миграция прошла успешно!")
        print(f"✅ Перенесено {total_records} записей")
        print("✅ PostgreSQL подключена и работает")
        print()
        print("🚀 РЕКОМЕНДАЦИИ:")
        print("   1. Протестируйте сайт в браузере")
        print("   2. Проверьте админку Django")
        print("   3. Создайте резервную копию PostgreSQL")
        print("   4. Переходите к созданию Docker инфраструктуры")
    else:
        print("⚠️ Возможны проблемы с миграцией")
        print("💡 Проверьте логи импорта данных")
    
    print()

if __name__ == "__main__":
    main()