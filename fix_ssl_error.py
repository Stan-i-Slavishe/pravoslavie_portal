#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка SSL сертификатов и исправление проблем
"""
import os
import subprocess
import sys
from pathlib import Path

def check_ssl_files():
    """Проверяет SSL файлы"""
    print("🔍 Проверяем SSL файлы...")
    
    cert_file = Path('ssl/cert.pem')
    key_file = Path('ssl/key.pem')
    
    if not cert_file.exists():
        print("❌ ssl/cert.pem не найден")
        return False
    
    if not key_file.exists():
        print("❌ ssl/key.pem не найден")
        return False
    
    print("✅ SSL файлы найдены")
    
    # Проверяем размер файлов
    cert_size = cert_file.stat().st_size
    key_size = key_file.stat().st_size
    
    print(f"📄 cert.pem: {cert_size} байт")
    print(f"🔑 key.pem: {key_size} байт")
    
    if cert_size < 100 or key_size < 100:
        print("⚠️ SSL файлы слишком маленькие, возможно повреждены")
        return False
    
    return True

def recreate_ssl_cert():
    """Пересоздает SSL сертификат"""
    print("🔄 Пересоздаем SSL сертификат...")
    
    # Удаляем старые файлы
    for file in ['ssl/cert.pem', 'ssl/key.pem']:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Удален {file}")
    
    # Создаем новый сертификат
    try:
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
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Moscow'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Moscow'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Django Dev Server'),
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
        with open('ssl/cert.pem', 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Сохраняем ключ
        with open('ssl/key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Новый SSL сертификат создан")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания сертификата: {e}")
        return False

def test_https_server():
    """Тестирует HTTPS сервер"""
    print("🧪 Тестируем HTTPS сервер...")
    
    try:
        import requests
        import urllib3
        
        # Отключаем предупреждения о самоподписанном сертификате
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Пробуем подключиться
        response = requests.get('https://127.0.0.1:8000/', verify=False, timeout=5)
        print(f"✅ HTTPS сервер отвечает: {response.status_code}")
        return True
        
    except ImportError:
        print("⚠️ requests не установлен, пропускаем тест")
        return True
    except Exception as e:
        print(f"❌ HTTPS сервер не отвечает: {e}")
        return False

def main():
    print("🔧 ДИАГНОСТИКА И ИСПРАВЛЕНИЕ SSL ПРОБЛЕМ")
    print("=" * 50)
    
    if not os.path.exists('manage.py'):
        print("❌ Запустите из корня Django проекта")
        return
    
    # Проверяем SSL файлы
    if not check_ssl_files():
        print("\n🔄 Пересоздаем SSL сертификат...")
        if not recreate_ssl_cert():
            print("❌ Не удалось создать SSL сертификат")
            return
    
    print("\n✅ SSL ПРОБЛЕМЫ ИСПРАВЛЕНЫ!")
    print("\n📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Перезапустите HTTPS сервер:")
    print("   start_https.bat")
    print("   ИЛИ")
    print("   python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")
    print()
    print("2. Откройте браузер и перейдите на:")
    print("   https://127.0.0.1:8000/")
    print()
    print("3. При предупреждении нажмите 'Дополнительно' -> 'Перейти на сайт'")
    
    choice = input("\nПерезапустить HTTPS сервер сейчас? (y/n): ")
    if choice.lower() == 'y':
        print("\n🔒 Запускаем HTTPS сервер...")
        os.system("python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem")

if __name__ == '__main__':
    main()
