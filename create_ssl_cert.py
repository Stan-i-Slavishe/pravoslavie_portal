#!/usr/bin/env python
"""
Создание SSL сертификата для Django разработки
"""
import os
import subprocess
from pathlib import Path

def create_ssl_certificate():
    """Создает самоподписанный SSL сертификат"""
    
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'
    
    try:
        # Способ 1: OpenSSL (если доступен)
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', str(key_file), '-out', str(cert_file),
            '-days', '365', '-nodes', '-batch',
            '-subj', '/C=RU/ST=Local/L=Local/O=Dev/CN=localhost'
        ], check=True, capture_output=True)
        print('✅ SSL сертификат создан через OpenSSL')
        return True
        
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    try:
        # Способ 2: Python cryptography
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
        
        # Сохраняем
        with open(cert_file, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(key_file, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print('✅ SSL сертификат создан через Python cryptography')
        return True
        
    except ImportError:
        print('📦 Устанавливаем cryptography...')
        subprocess.run(['pip', 'install', 'cryptography'])
        print('🔄 Перезапустите создание сертификата')
        return False
        
    except Exception as e:
        print(f'❌ Ошибка создания сертификата: {e}')
        return False

if __name__ == '__main__':
    create_ssl_certificate()
