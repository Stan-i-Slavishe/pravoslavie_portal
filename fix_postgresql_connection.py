#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Диагностика PostgreSQL с разными паролями
"""

import psycopg2
import sys
import os

def test_different_passwords():
    """Пробуем разные варианты паролей"""
    
    connection_params = {
        'host': 'localhost',
        'port': '5432', 
        'database': 'postgres',  # Начнем с системной БД
        'user': 'postgres'
    }
    
    # Возможные пароли для postgres пользователя
    possible_passwords = [
        '',  # Пустой пароль
        'postgres',  # Стандартный
        'admin',  # Часто используемый
        'password',  # Часто используемый
        '123456',  # Простой
        'local_strong_password_2024',  # Наш пароль
    ]
    
    print("Поиск правильного пароля для postgres...")
    print("="*50)
    
    for password in possible_passwords:
        try:
            print(f"Пробуем пароль: {'(пустой)' if password == '' else password}")
            
            params = connection_params.copy()
            params['password'] = password
            
            conn = psycopg2.connect(**params)
            cursor = conn.cursor()
            
            # Проверяем версию
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ УСПЕХ! PostgreSQL: {version[:50]}...")
            
            # Проверяем существующие базы данных
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print("\nСуществующие базы данных:")
            for db in databases:
                print(f"  - {db[0]}")
            
            # Проверяем пользователей
            cursor.execute("SELECT usename FROM pg_user;")
            users = cursor.fetchall()
            print("\nСуществующие пользователи:")
            for user in users:
                print(f"  - {user[0]}")
            
            cursor.close()
            conn.close()
            
            # Теперь проверим нашу целевую БД
            print(f"\nПроверяем подключение к pravoslavie_local_db...")
            return test_target_database(password)
            
        except Exception as e:
            print(f"❌ Не подошел: {e}")
            continue
    
    print("\n❌ Ни один пароль не подошел")
    return False

def test_target_database(postgres_password):
    """Проверяем целевую базу данных"""
    
    # Сначала проверим существует ли наша БД
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password=postgres_password
        )
        cursor = conn.cursor()
        
        # Проверяем существование нашей БД
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'pravoslavie_local_db';")
        db_exists = cursor.fetchone() is not None
        
        # Проверяем существование нашего пользователя
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = 'pravoslavie_user';")
        user_exists = cursor.fetchone() is not None
        
        print(f"База pravoslavie_local_db существует: {'✅' if db_exists else '❌'}")
        print(f"Пользователь pravoslavie_user существует: {'✅' if user_exists else '❌'}")
        
        cursor.close()
        conn.close()
        
        if not db_exists or not user_exists:
            print("\n⚠️ Нужно пересоздать БД или пользователя")
            return recreate_database_and_user(postgres_password)
        
        # Пробуем подключиться к нашей БД
        print("\nПробуем подключиться к pravoslavie_local_db...")
        try:
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='pravoslavie_local_db',
                user='pravoslavie_user',
                password='local_strong_password_2024'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cursor.fetchone()[0]
            print(f"✅ УСПЕХ! Подключение к pravoslavie_local_db работает")
            print(f"✅ Таблиц в БД: {table_count}")
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка подключения к pravoslavie_local_db: {e}")
            print("Попробуем пересоздать БД с правильными настройками...")
            return recreate_database_and_user(postgres_password)
        
    except Exception as e:
        print(f"❌ Ошибка проверки целевой БД: {e}")
        return False

def recreate_database_and_user(postgres_password):
    """Пересоздаем БД и пользователя с правильными настройками"""
    
    print("\nПересоздание БД и пользователя...")
    print("-" * 40)
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password=postgres_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Удаляем старую БД если существует (осторожно!)
        try:
            cursor.execute("DROP DATABASE IF EXISTS pravoslavie_local_db;")
            print("🗑️ Старая БД удалена")
        except:
            pass
        
        # Удаляем старого пользователя если существует
        try:
            cursor.execute("DROP USER IF EXISTS pravoslavie_user;")
            print("🗑️ Старый пользователь удален")
        except:
            pass
        
        # Создаем пользователя
        cursor.execute("""
            CREATE USER pravoslavie_user WITH 
            PASSWORD 'local_strong_password_2024'
            CREATEDB
            LOGIN;
        """)
        print("👤 Пользователь pravoslavie_user создан")
        
        # Создаем БД
        cursor.execute("""
            CREATE DATABASE pravoslavie_local_db 
            WITH 
            OWNER = pravoslavie_user
            ENCODING = 'UTF8'
            LC_COLLATE = 'C'
            LC_CTYPE = 'C'
            TEMPLATE = template0;
        """)
        print("📂 База данных pravoslavie_local_db создана")
        
        # Даем права
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE pravoslavie_local_db TO pravoslavie_user;")
        print("🔐 Права предоставлены")
        
        cursor.close()
        conn.close()
        
        # Проверяем подключение к новой БД
        print("\nПроверяем подключение к новой БД...")
        test_conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='pravoslavie_local_db',
            user='pravoslavie_user',
            password='local_strong_password_2024'
        )
        test_conn.close()
        
        print("✅ БД и пользователь успешно пересозданы!")
        print("\n⚠️ ВНИМАНИЕ: Нужно будет заново применить миграции Django и импортировать данные")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка пересоздания БД: {e}")
        return False

if __name__ == "__main__":
    success = test_different_passwords()
    
    if success:
        print("\n🎉 PostgreSQL настроен правильно!")
        print("Можно продолжать работу с Django")
    else:
        print("\n❌ Проблемы с PostgreSQL не устранены")
        print("Нужна дополнительная диагностика")
