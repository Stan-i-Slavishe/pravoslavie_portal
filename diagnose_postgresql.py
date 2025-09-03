#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Диагностика подключения к PostgreSQL
"""

import psycopg2
import sys
import os

def test_postgresql_connection():
    """Прямая проверка подключения к PostgreSQL"""
    
    connection_params = {
        'host': 'localhost',
        'port': '5432', 
        'database': 'pravoslavie_local_db',
        'user': 'pravoslavie_user',
        'password': 'local_strong_password_2024'
    }
    
    print("Диагностика подключения к PostgreSQL")
    print("="*50)
    print(f"Host: {connection_params['host']}")
    print(f"Port: {connection_params['port']}")
    print(f"Database: {connection_params['database']}")
    print(f"User: {connection_params['user']}")
    print()
    
    # Тест 1: Подключение к серверу PostgreSQL
    print("Тест 1: Подключение к серверу PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host=connection_params['host'],
            port=connection_params['port'],
            user='postgres',  # Подключаемся под суперпользователем
            password='',  # Попробуем без пароля
            database='postgres'  # К системной БД
        )
        conn.close()
        print("✅ PostgreSQL сервер доступен (без пароля)")
    except Exception as e1:
        print(f"❌ Подключение без пароля не удалось: {e1}")
        
        # Попробуем с паролем
        try:
            password = input("Введите пароль для пользователя postgres: ")
            conn = psycopg2.connect(
                host=connection_params['host'],
                port=connection_params['port'],
                user='postgres',
                password=password,
                database='postgres'
            )
            conn.close()
            print("✅ PostgreSQL сервер доступен (с паролем)")
        except Exception as e2:
            print(f"❌ PostgreSQL сервер недоступен: {e2}")
            print("\nВозможные причины:")
            print("- PostgreSQL не запущен")
            print("- Неверные настройки подключения") 
            print("- Проблемы с firewall")
            return False
    
    # Тест 2: Проверка существования БД
    print("\nТест 2: Проверка существования БД pravoslavie_local_db...")
    try:
        conn = psycopg2.connect(
            host=connection_params['host'],
            port=connection_params['port'],
            user='postgres',
            database='postgres'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'pravoslavie_local_db';")
        result = cursor.fetchone()
        
        if result:
            print("✅ База данных pravoslavie_local_db существует")
        else:
            print("❌ База данных pravoslavie_local_db не найдена")
            
            # Показываем существующие БД
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print("Существующие базы данных:")
            for db in databases:
                print(f"  - {db[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка проверки БД: {e}")
        return False
    
    # Тест 3: Проверка пользователя
    print("\nТест 3: Проверка пользователя pravoslavie_user...")
    try:
        conn = psycopg2.connect(
            host=connection_params['host'],
            port=connection_params['port'],
            user='postgres',
            database='postgres'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = 'pravoslavie_user';")
        result = cursor.fetchone()
        
        if result:
            print("✅ Пользователь pravoslavie_user существует")
        else:
            print("❌ Пользователь pravoslavie_user не найден")
            
            # Показываем существующих пользователей
            cursor.execute("SELECT usename FROM pg_user;")
            users = cursor.fetchall()
            print("Существующие пользователи:")
            for user in users:
                print(f"  - {user[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка проверки пользователя: {e}")
        return False
    
    # Тест 4: Прямое подключение к целевой БД
    print("\nТест 4: Подключение к pravoslavie_local_db под pravoslavie_user...")
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Успешное подключение! PostgreSQL: {version[:50]}...")
        
        # Проверяем таблицы
        cursor.execute("""
            SELECT count(*) FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"✅ Таблиц в БД: {table_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Подключение к целевой БД не удалось: {e}")
        print("\nВозможные причины:")
        print("- Неверный пароль для pravoslavie_user")
        print("- Пользователь не имеет прав на БД") 
        print("- БД не существует")
        return False

if __name__ == "__main__":
    success = test_postgresql_connection()
    if success:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("PostgreSQL готов к работе с Django")
    else:
        print("\n❌ ЕСТЬ ПРОБЛЕМЫ С POSTGRESQL")
        print("Необходимо устранить ошибки подключения")
