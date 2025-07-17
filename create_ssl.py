#!/usr/bin/env python
"""
Создание SSL сертификата для Django HTTPS
"""
import subprocess
import os
from pathlib import Path

def create_ssl_cert():
    """Создает SSL сертификат"""
    try:
        # Создаем папку ssl если нет
        Path('ssl').mkdir(exist_ok=True)
        
        # Пробуем создать через OpenSSL
        result = subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', 'ssl/key.pem', '-out', 'ssl/cert.pem',
            '-days', '365', '-nodes', '-batch',
            '-subj', '/C=RU/ST=Local/L=Local/O=Django Dev/CN=localhost'
        ], capture_output=True, check=True)
        
        print('✅ SSL сертификат создан через OpenSSL')
        print('   Файлы: ssl/cert.pem и ssl/key.pem')
        return True
        
    except (FileNotFoundError, subprocess.CalledProcessError):
        print('⚠️ OpenSSL не найден, пробуем Python способ...')
        
        try:
            # Устанавливаем cryptography если нет
            try:
                from cryptography import x509
                from cryptography.x509.oid import NameOID
                from cryptography.hazmat.primitives import hashes, serialization
                from cryptography.hazmat.primitives.asymmetric import rsa
                import datetime
            except ImportError:
                print('📦 Устанавливаем cryptography...')
                subprocess.run(['pip', 'install', 'cryptography'], check=True)
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
            with open('ssl/cert.pem', 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            # Сохраняем ключ
            with open('ssl/key.pem', 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            print('✅ SSL сертификат создан через Python cryptography')
            print('   Файлы: ssl/cert.pem и ssl/key.pem')
            return True
            
        except Exception as e:
            print(f'❌ Ошибка создания сертификата: {e}')
            return False

if __name__ == '__main__':
    print('🔒 СОЗДАНИЕ SSL СЕРТИФИКАТА')
    print('=' * 30)
    
    if os.path.exists('ssl/cert.pem') and os.path.exists('ssl/key.pem'):
        response = input('SSL сертификат уже существует. Пересоздать? (y/n): ')
        if response.lower() != 'y':
            print('✅ Используем существующий сертификат')
            exit(0)
    
    if create_ssl_cert():
        print('\n🎉 SSL сертификат готов!')
        print('\n🚀 Теперь можете запустить HTTPS сервер:')
        print('   python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem')
        print('\n🌐 Адрес: https://127.0.0.1:8000/')
        print('⚠️  Браузер покажет предупреждение - это нормально для разработки')
    else:
        print('\n❌ Не удалось создать SSL сертификат')
