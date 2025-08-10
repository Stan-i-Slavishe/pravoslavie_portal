#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Закрываем все соединения с базой данных
    from django.db import connections
    
    print("🔧 Закрываем все соединения с базой данных...")
    for conn in connections.all():
        conn.close()
    
    print("✅ Соединения закрыты!")
    print("Теперь можно запустить сервер заново.")
