import os
import sys
import django
import sqlite3
from django.db import connection

# Настройка Django
sys.path.append('E:\\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_database_lock():
    try:
        # Закрываем все соединения с БД
        connection.close()
        
        # Путь к базе данных
        db_path = 'E:\\pravoslavie_portal\\db.sqlite3'
        
        print(f"Проверяем базу данных: {db_path}")
        
        # Проверяем блокировку
        try:
            conn = sqlite3.connect(db_path, timeout=10)
            cursor = conn.cursor()
            
            # Проверяем целостность базы
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()
            print(f"Целостность БД: {result[0]}")
            
            # Принудительно закрываем все соединения
            cursor.execute("PRAGMA wal_checkpoint(TRUNCATE);")
            
            # Оптимизируем базу
            cursor.execute("VACUUM;")
            print("База данных оптимизирована")
            
            conn.close()
            
        except sqlite3.OperationalError as e:
            print(f"Ошибка SQLite: {e}")
            return False
            
        print("✅ База данных исправлена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    fix_database_lock()
