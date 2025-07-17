#!/usr/bin/env python
"""
Быстрое добавление HTTPS поддержки в Django
"""

# Читаем текущие настройки
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем django-extensions в THIRD_PARTY_APPS если его еще нет
if 'django_extensions' not in content:
    content = content.replace(
        'THIRD_PARTY_APPS = [',
        'THIRD_PARTY_APPS = [\n    "django_extensions",  # Для HTTPS в разработке'
    )
    print('✅ django-extensions добавлен в THIRD_PARTY_APPS')

# Добавляем HTTPS настройки для разработки в конец файла
https_settings = '''

# =====================================
# HTTPS НАСТРОЙКИ ДЛЯ РАЗРАБОТКИ
# =====================================

# Разрешаем как HTTP так и HTTPS в разработке
SECURE_SSL_REDIRECT = False  # Не принуждаем к HTTPS

# Настройки для работы с HTTPS в разработке
if DEBUG:
    # В разработке поддерживаем и HTTP и HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Для HTTPS запросов используем secure cookies
    SESSION_COOKIE_SECURE = False  # Работает и с HTTP и с HTTPS
    CSRF_COOKIE_SECURE = False     # Работает и с HTTP и с HTTPS
    
    # Отключаем HSTS для разработки
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
    # Доверенные источники для CSRF (для HTTPS)
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'https://127.0.0.1:8000',
        'https://localhost:8000',
    ]
else:
    # Продакшен - строгие настройки
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
'''

# Удаляем старые настройки безопасности если есть
import re
content = re.sub(r'# =====================================\s*# HTTPS НАСТРОЙКИ ДЛЯ РАЗРАБОТКИ.*?SECURE_HSTS_PRELOAD = True', '', content, flags=re.DOTALL)

# Добавляем новые настройки
content += https_settings

# Записываем обновленный файл
with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ HTTPS настройки добавлены в settings.py')
print('✅ Django теперь поддерживает и HTTP и HTTPS')
print('')
print('🚀 Теперь установите django-extensions:')
print('   pip install django-extensions[werkzeug]')
print('')
print('🔒 Для HTTPS запуска используйте:')
print('   python manage.py runserver_plus --cert-file cert.pem --key-file key.pem')
print('')
print('🌐 Для HTTP запуска используйте:')
print('   python manage.py runserver')
