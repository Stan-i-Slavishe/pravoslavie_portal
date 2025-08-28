"""
Настройки SQLite для избежания блокировок
Добавить в settings.py
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # Увеличиваем timeout до 30 секунд
            'init_command': '''
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA temp_store=memory;
                PRAGMA mmap_size=268435456;
                PRAGMA cache_size=10000;
                PRAGMA busy_timeout=30000;
            '''
        }
    }
}

# Альтернативный вариант для продакшена - PostgreSQL
# Раскомментировать для использования:

# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default='postgresql://user:password@localhost:5432/pravoslavie_portal'
#     )
# }
