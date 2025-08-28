# Дополнительные настройки для стабильности SQLite
# Добавьте в settings.py для улучшения работы с SQLite

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # Увеличенный таймаут
            'check_same_thread': False,  # Для многопоточности
        },
    }
}

# Дополнительные настройки для production
if not DEBUG:
    DATABASES['default']['OPTIONS'].update({
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    })
