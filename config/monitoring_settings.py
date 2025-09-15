# 📊 Расширенные настройки мониторинга для Production
# Добавить в config/settings_production.py

import os
from datetime import timedelta

# 📁 Создание директорий для логов
LOGS_DIR = '/app/logs/'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)

# 👥 Администраторы для уведомлений
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@pravoslavie-portal.ru')),
]
MANAGERS = ADMINS

# 📊 Расширенная конфигурация логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # 🎨 Форматы логов
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {funcName} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[{asctime}] {levelname} - {message}',
            'style': '{',
            'datefmt': '%H:%M:%S'
        },
        'json': {
            'format': '{"timestamp": "{asctime}", "level": "{levelname}", "logger": "{name}", "message": "{message}"}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    
    # 📝 Обработчики логов
    'handlers': {
        # 🗂️ Общий лог приложения
        'file_general': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}django.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        # ❌ Лог ошибок
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}errors.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        # 🔒 Лог безопасности
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}security.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        # 💰 Лог транзакций магазина
        'file_shop': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}shop.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        # 👤 Лог аутентификации
        'file_auth': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}auth.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        # 📧 Email уведомления критических ошибок
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True,
        },
        
        # 🖥️ Консольный вывод
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        
        # 📊 JSON лог для внешнего мониторинга
        'file_json': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOGS_DIR}monitoring.json',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 3,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
    },
    
    # 🎯 Логгеры для разных компонентов
    'loggers': {
        # Django общий
        'django': {
            'handlers': ['file_general', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Django ошибки
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        # Django безопасность
        'django.security': {
            'handlers': ['file_security', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        
        # Магазин
        'shop': {
            'handlers': ['file_shop', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Аутентификация
        'accounts': {
            'handlers': ['file_auth', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Система подписок
        'subscriptions': {
            'handlers': ['file_shop', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Терапевтические сказки
        'fairy_tales': {
            'handlers': ['file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Мониторинг производительности
        'monitoring': {
            'handlers': ['file_json', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Root логгер
        'root': {
            'handlers': ['file_general'],
            'level': 'WARNING',
        },
    },
}

# 📈 Настройки мониторинга производительности
PERFORMANCE_MONITORING = {
    'ENABLED': os.environ.get('ENABLE_PERFORMANCE_MONITORING', 'True').lower() == 'true',
    'SLOW_QUERY_THRESHOLD': float(os.environ.get('SLOW_QUERY_THRESHOLD', '1.0')),  # секунды
    'MEMORY_THRESHOLD': int(os.environ.get('MEMORY_THRESHOLD', '500')),  # MB
    'LOG_LEVEL': os.environ.get('MONITORING_LOG_LEVEL', 'INFO'),
}

# 📊 Метрики для отслеживания
METRICS_CONFIG = {
    'TRACK_USER_ACTIVITY': True,
    'TRACK_PAGE_VIEWS': True,
    'TRACK_PURCHASES': True,
    'TRACK_ERRORS': True,
    'TRACK_PERFORMANCE': True,
    'METRICS_RETENTION_DAYS': 90,
}

# 🚨 Настройки алертов
ALERTS_CONFIG = {
    'ERROR_THRESHOLD': 10,  # ошибок в час
    'RESPONSE_TIME_THRESHOLD': 2.0,  # секунды
    'DISK_SPACE_THRESHOLD': 80,  # процентов
    'MEMORY_THRESHOLD': 85,  # процентов
    'SEND_EMAIL_ALERTS': True,
    'SEND_TELEGRAM_ALERTS': os.environ.get('TELEGRAM_BOT_TOKEN') is not None,
}

# 📱 Telegram уведомления
if os.environ.get('TELEGRAM_BOT_TOKEN'):
    TELEGRAM_CONFIG = {
        'BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN'),
        'CHAT_ID': os.environ.get('TELEGRAM_ADMIN_CHAT_ID'),
        'ALERTS_ENABLED': True,
    }

# ⏰ Настройки rotated логов
LOG_ROTATION_CONFIG = {
    'MAX_LOG_SIZE': 10 * 1024 * 1024,  # 10MB
    'BACKUP_COUNT': 5,
    'CLEANUP_DAYS': 30,  # Удалять логи старше 30 дней
}

# 🔍 Мониторинг базы данных
DB_MONITORING = {
    'LOG_SLOW_QUERIES': True,
    'SLOW_QUERY_THRESHOLD': 1.0,  # секунды
    'LOG_DB_CONNECTIONS': True,
    'MAX_DB_CONNECTIONS': 50,
}

print("📊 Система мониторинга инициализирована")
print(f"   📁 Логи сохраняются в: {LOGS_DIR}")
print(f"   📧 Уведомления отправляются на: {[admin[1] for admin in ADMINS]}")
print(f"   📈 Мониторинг производительности: {'Включен' if PERFORMANCE_MONITORING['ENABLED'] else 'Отключен'}")
