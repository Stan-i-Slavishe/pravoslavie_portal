#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Полная настройка HTTPS для Django - все в одном файле
"""
import subprocess
import sys
import os
from pathlib import Path

def install_django_extensions():
    """Устанавливает django-extensions"""
    print("📦 Устанавливаем django-extensions...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'django-extensions', 'werkzeug'], 
                      check=True, capture_output=True)
        print("✅ django-extensions установлен")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def update_settings():
    """Обновляет settings.py для поддержки HTTPS"""
    print("⚙️ Обновляем settings.py...")
    
    try:
        # Читаем settings.py
        with open('config/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Добавляем django-extensions если его нет
        if 'django_extensions' not in content:
            content = content.replace(
                'THIRD_PARTY_APPS = [',
                'THIRD_PARTY_APPS = [\n    "django_extensions",  # Для HTTPS в разработке'
            )
            print("✅ django-extensions добавлен в THIRD_PARTY_APPS")
        
        # Проверяем есть ли уже HTTPS настройки
        if 'HTTPS НАСТРОЙКИ ДЛЯ РАЗРАБОТКИ' not in content:
            # Добавляем HTTPS настройки
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
            content += https_settings
            print("✅ HTTPS настройки добавлены")
        else:
            print("✅ HTTPS настройки уже есть")
        
        # Записываем обновленный файл
        with open('config/settings.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления settings.py: {e}")
        return False

def create_ssl_certificate():
    """Создает SSL сертификат"""
    print("🔒 Создаем SSL сертификат...")
    
    # Создаем папку ssl
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'
    
    # Проверяем существуют ли файлы
    if cert_file.exists() and key_file.exists():
        print("✅ SSL сертификат уже существует")
        return True
    
    # Способ 1: OpenSSL
    try:
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', str(key_file), '-out', str(cert_file),
            '-days', '365', '-nodes', '-batch',
            '-subj', '/C=RU/ST=Local/L=Local/O=Django/CN=localhost'
        ], check=True, capture_output=True)
        
        print("✅ SSL сертификат создан через OpenSSL")
        return True
        
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️ OpenSSL не найден, пробуем Python способ...")
    
    # Способ 2: Python cryptography
    try:
        # Устанавливаем cryptography если нужно
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime
        except ImportError:
            print("📦 Устанавливаем cryptography...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'cryptography'], check=True)
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime
        
        # Генерируем ключ
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Создаем сертификат
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'RU'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Local'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Local'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Django Dev'),
            x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u'localhost'),
                x509.DNSName(u'127.0.0.1'),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Сохраняем сертификат
        with open(cert_file, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Сохраняем ключ
        with open(key_file, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ SSL сертификат создан через Python")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания сертификата: {e}")
        return False

def create_startup_scripts():
    """Создает простые скрипты для запуска"""
    print("📝 Создаем скрипты запуска...")
    
    # HTTP скрипт
    with open('start_http.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('call .venv\\Scripts\\activate\n')
        f.write('echo Starting HTTP server at http://127.0.0.1:8000/\n')
        f.write('python manage.py runserver\n')
    
    # HTTPS скрипт
    with open('start_https.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('call .venv\\Scripts\\activate\n')
        f.write('echo Starting HTTPS server at https://127.0.0.1:8000/\n')
        f.write('echo Browser will show security warning - click Advanced then Proceed\n')
        f.write('python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem\n')
    
    print("✅ Скрипты start_http.bat и start_https.bat созданы")

def main():
    print("🔧 НАСТРОЙКА DJANGO ДЛЯ HTTPS")
    print("=" * 40)
    
    if not os.path.exists('manage.py'):
        print("❌ Запустите скрипт из корня Django проекта")
        return
    
    print("\n1️⃣ Устанавливаем django-extensions...")
    if not install_django_extensions():
        print("❌ Не удалось установить django-extensions")
        return
    
    print("\n2️⃣ Обновляем settings.py...")
    if not update_settings():
        print("❌ Не удалось обновить settings.py")
        return
    
    print("\n3️⃣ Создаем SSL сертификат...")
    if not create_ssl_certificate():
        print("❌ Не удалось создать SSL сертификат")
        return
    
    print("\n4️⃣ Создаем скрипты запуска...")
    create_startup_scripts()
    
    print("\n🎉 НАСТРОЙКА ЗАВЕРШЕНА!")
    print("=" * 50)
    
    print("\n📋 ВАРИАНТЫ ЗАПУСКА:")
    print("🌐 HTTP сервер:")
    print("   start_http.bat")
    print("   ИЛИ: python manage.py runserver")
    print("   Адрес: http://127.0.0.1:8000/")
    print()
    print("🔒 HTTPS сервер:")
    print("   start_https.bat")
    print("   ИЛИ: python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
    print("   Адрес: https://127.0.0.1:8000/")
    print("   ⚠️ Браузер покажет предупреждение - нажмите 'Дополнительно' -> 'Перейти на сайт'")
    
    choice = input("\nЗапустить сервер сейчас? (1=HTTP, 2=HTTPS, n=Нет): ")
    
    if choice == "1":
        print("\n🌐 Запускаем HTTP сервер...")
        os.system("python manage.py runserver")
    elif choice == "2":
        print("\n🔒 Запускаем HTTPS сервер...")
        if os.path.exists('ssl/cert.pem'):
            os.system("python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
        else:
            print("❌ SSL сертификат не найден")
    else:
        print("\n✅ Готово! Используйте start_http.bat или start_https.bat")

if __name__ == '__main__':
    main()
