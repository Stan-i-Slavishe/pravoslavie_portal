"""
Кастомный SQLite backend с оптимизированными PRAGMA настройками
"""

from django.db.backends.sqlite3 import base


class DatabaseWrapper(base.DatabaseWrapper):
    """Кастомный SQLite wrapper с оптимизированными настройками"""
    
    def get_new_connection(self, conn_params):
        """Создает новое соединение с оптимизированными PRAGMA настройками"""
        conn = super().get_new_connection(conn_params)
        
        # Применяем оптимизированные PRAGMA настройки
        with conn.cursor() as cursor:
            # WAL режим для лучшей производительности
            cursor.execute("PRAGMA journal_mode=WAL;")
            
            # Сбалансированная синхронизация
            cursor.execute("PRAGMA synchronous=NORMAL;")
            
            # Временные файлы в памяти
            cursor.execute("PRAGMA temp_store=memory;")
            
            # Memory-mapped I/O (256MB)
            cursor.execute("PRAGMA mmap_size=268435456;")
            
            # Размер кеша (10000 страниц)
            cursor.execute("PRAGMA cache_size=10000;")
            
            # Таймаут при блокировке (30 секунд)
            cursor.execute("PRAGMA busy_timeout=30000;")
            
            # Отключаем проверку foreign keys во время bulk операций
            # (можно включить в production если нужно)
            # cursor.execute("PRAGMA foreign_keys=ON;")
        
        return conn
