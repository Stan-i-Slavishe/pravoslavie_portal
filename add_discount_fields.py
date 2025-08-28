#!/usr/bin/env python
"""
Скрипт для добавления полей discount_amount и discount_code в таблицу shop_order
"""
import os
import django
import sqlite3

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def add_discount_fields():
    """Добавляет поля discount_amount и discount_code в таблицу shop_order"""
    
    with connection.cursor() as cursor:
        try:
            # Проверяем, есть ли уже поле discount_amount
            cursor.execute("PRAGMA table_info(shop_order)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'discount_amount' not in columns:
                print("Добавляем поле discount_amount...")
                cursor.execute("""
                    ALTER TABLE shop_order 
                    ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0.00
                """)
                print("✅ Поле discount_amount добавлено")
            else:
                print("ℹ️ Поле discount_amount уже существует")
            
            if 'discount_code' not in columns:
                print("Добавляем поле discount_code...")
                cursor.execute("""
                    ALTER TABLE shop_order 
                    ADD COLUMN discount_code VARCHAR(50) DEFAULT ''
                """)
                print("✅ Поле discount_code добавлено")
            else:
                print("ℹ️ Поле discount_code уже существует")
                
            # Проверяем структуру таблицы
            cursor.execute("PRAGMA table_info(shop_order)")
            columns_info = cursor.fetchall()
            print("\nТекущая структура таблицы shop_order:")
            for col in columns_info:
                print(f"  {col[1]} - {col[2]}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    add_discount_fields()
    print("\n🎉 Готово! Теперь можно запускать сервер.")
