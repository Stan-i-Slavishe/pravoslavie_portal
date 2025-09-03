#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление пользователя и прав PostgreSQL
"""

import psycopg2
import sys

def fix_postgresql_user():
    """Исправляем пользователя pravoslavie_user и его права"""
    
    postgres_password = 'postgres'  # Нашли рабочий пароль
    
    print("Исправление пользователя pravoslavie_user...")
    print("=" * 50)
    
    try:
        # Подключаемся как суперпользователь
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password=postgres_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Подключение к PostgreSQL успешно")
        
        # Изменяем пароль пользователя pravoslavie_user
        print("🔐 Устанавливаем правильный пароль для pravoslavie_user...")
        cursor.execute("""
            ALTER USER pravoslavie_user WITH PASSWORD 'local_strong_password_2024';
        """)
        print("✅ Пароль изменен")
        
        # Даем пользователю права суперпользователя (временно для настройки)
        print("👑 Устанавливаем права суперпользователя...")
        cursor.execute("""
            ALTER USER pravoslavie_user WITH SUPERUSER CREATEDB CREATEROLE LOGIN;
        """)
        print("✅ Права установлены")
        
        # Убеждаемся что пользователь владелец БД
        print("📂 Устанавливаем владельца БД...")
        cursor.execute("""
            ALTER DATABASE pravoslavie_local_db OWNER TO pravoslavie_user;
        """)
        print("✅ Владелец БД установлен")
        
        # Даем все права на БД
        print("🔑 Предоставляем все права на БД...")
        cursor.execute("""
            GRANT ALL PRIVILEGES ON DATABASE pravoslavie_local_db TO pravoslavie_user;
        """)
        print("✅ Права на БД предоставлены")
        
        cursor.close()
        conn.close()
        
        # Теперь проверяем подключение под pravoslavie_user
        print("\n🧪 Тестируем подключение под pravoslavie_user...")
        
        test_conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='pravoslavie_local_db',
            user='pravoslavie_user',
            password='local_strong_password_2024'
        )
        
        test_cursor = test_conn.cursor()
        
        # Проверяем версию PostgreSQL
        test_cursor.execute("SELECT version();")
        version = test_cursor.fetchone()[0]
        print(f"✅ PostgreSQL версия: {version[:50]}...")
        
        # Проверяем текущую БД
        test_cursor.execute("SELECT current_database();")
        current_db = test_cursor.fetchone()[0]
        print(f"✅ Текущая БД: {current_db}")
        
        # Проверяем текущего пользователя  
        test_cursor.execute("SELECT current_user;")
        current_user = test_cursor.fetchone()[0]
        print(f"✅ Текущий пользователь: {current_user}")
        
        # Проверяем количество таблиц
        test_cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = test_cursor.fetchone()[0]
        print(f"✅ Таблиц в БД: {table_count}")
        
        # Если таблиц мало, значит нужно применить миграции
        if table_count < 20:  # Django обычно создает много системных таблиц
            print("⚠️ Таблиц мало - возможно нужно применить миграции Django")
        
        test_cursor.close()
        test_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка исправления пользователя: {e}")
        return False

def test_django_connection():
    """Тестируем подключение Django"""
    
    print("\n" + "=" * 50)
    print("ТЕСТ DJANGO ПОДКЛЮЧЕНИЯ")
    print("=" * 50)
    
    try:
        # Настройка Django окружения
        import os
        import django
        
        os.environ['DJANGO_ENV'] = 'local'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local_postgresql')
        
        # Инициализация Django
        import sys
        sys.path.append('.')
        django.setup()
        
        from django.db import connection
        
        # Тест подключения
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Django подключен к PostgreSQL: {version[:50]}...")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✅ База данных: {db_name}")
            
            cursor.execute("SELECT current_user;")
            user = cursor.fetchone()[0] 
            print(f"✅ Пользователь: {user}")
        
        # Проверяем настройки Django
        from django.conf import settings
        db_config = settings.DATABASES['default']
        print(f"✅ Django Engine: {db_config['ENGINE']}")
        print(f"✅ Django Database: {db_config['NAME']}")
        print(f"✅ Django User: {db_config['USER']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django подключение не удалось: {e}")
        return False

if __name__ == "__main__":
    print("Исправление PostgreSQL подключения...")
    print()
    
    # Шаг 1: Исправляем пользователя PostgreSQL
    postgresql_ok = fix_postgresql_user()
    
    if not postgresql_ok:
        print("\n❌ Не удалось исправить PostgreSQL пользователя")
        sys.exit(1)
    
    # Шаг 2: Тестируем Django подключение
    django_ok = test_django_connection()
    
    if postgresql_ok and django_ok:
        print("\n🎉 ВСЕ ИСПРАВЛЕНО!")
        print("PostgreSQL и Django работают корректно")
        print("\nСледующие шаги:")
        print("1. Применить миграции: python manage.py migrate")
        print("2. Запустить проверку: python verify_postgresql_integration.py")
        print("3. Импортировать данные из бэкапа при необходимости")
    else:
        print("\n❌ ЕСТЬ ПРОБЛЕМЫ")
        print("Требуется дополнительная диагностика")
