@echo off
echo 🔒 ПРОСТАЯ НАСТРОЙКА HTTPS ДЛЯ РАЗРАБОТКИ
echo ========================================
echo.

echo 🔹 Настраиваем HTTPS как было раньше
echo 🔹 Без лишних платежных настроек
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

call .venv\Scripts\activate

echo 1️⃣  Устанавливаем django-extensions...
pip install django-extensions[werkzeug] --quiet

echo.
echo 2️⃣  Создаем SSL сертификат...
if not exist ssl mkdir ssl

python -c "
import subprocess
import os

try:
    # Простой способ создания сертификата
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', 'ssl/key.pem', '-out', 'ssl/cert.pem',
        '-days', '365', '-nodes', '-batch',
        '-subj', '/C=RU/ST=Local/L=Local/O=Dev/CN=localhost'
    ], check=True, capture_output=True)
    print('✅ SSL сертификат создан')
except:
    # Если OpenSSL недоступен, используем другой способ
    try:
        import ssl
        import socket
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
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
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).sign(key, hashes.SHA256())
        
        with open('ssl/cert.pem', 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open('ssl/key.pem', 'wb') as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print('✅ SSL сертификат создан через Python')
    except ImportError:
        print('⚠️ Устанавливаем cryptography...')
        subprocess.run(['pip', 'install', 'cryptography'])
        print('🔄 Запустите скрипт повторно')
        exit(1)
"

echo.
echo 3️⃣  Добавляем django-extensions в настройки...

python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем django_extensions если его нет
if 'django_extensions' not in content:
    content = content.replace(
        'THIRD_PARTY_APPS = [',
        'THIRD_PARTY_APPS = [\n    \"django_extensions\",  # Для HTTPS в разработке'
    )

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ django-extensions добавлен')
"

echo.
echo 4️⃣  Создаем простые скрипты запуска...

REM HTTPS сервер
echo @echo off > run_https.bat
echo echo 🔒 Django HTTPS Server >> run_https.bat
echo echo ==================== >> run_https.bat
echo call .venv\Scripts\activate >> run_https.bat
echo echo Starting HTTPS server at https://127.0.0.1:8000/ >> run_https.bat
echo python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000 >> run_https.bat

REM HTTP сервер
echo @echo off > run_http.bat
echo echo 🌐 Django HTTP Server >> run_http.bat
echo echo =================== >> run_http.bat
echo call .venv\Scripts\activate >> run_http.bat
echo echo Starting HTTP server at http://127.0.0.1:8000/ >> run_http.bat
echo python manage.py runserver 127.0.0.1:8000 >> run_http.bat

echo ✅ Скрипты запуска созданы

echo.
echo 5️⃣  Минимальная настройка HTTPS в Django...

python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Убираем принуждение к HTTPS для гибкости разработки
if 'SECURE_SSL_REDIRECT = True' in content:
    content = content.replace('SECURE_SSL_REDIRECT = True', 'SECURE_SSL_REDIRECT = False')

# Добавляем минимальные настройки если их нет
if 'SECURE_SSL_REDIRECT' not in content:
    content += '''
# Простые HTTPS настройки для разработки
SECURE_SSL_REDIRECT = False  # Не принуждаем к HTTPS
'''

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Базовые HTTPS настройки добавлены')
"

echo.
echo 🎉 ГОТОВО!
echo ========
echo.
echo 📋 ТЕПЕРЬ У ВАС ЕСТЬ ДВА РЕЖИМА:
echo.
echo   🔒 HTTPS: run_https.bat
echo      → https://127.0.0.1:8000/
echo.
echo   🌐 HTTP:  run_http.bat  
echo      → http://127.0.0.1:8000/
echo.
echo 💡 ПРИ ПЕРВОМ ЗАПУСКЕ HTTPS:
echo   • Браузер покажет предупреждение
echo   • Нажмите "Дополнительно" → "Перейти на 127.0.0.1"
echo   • Это нормально для разработки!
echo.

set /p launch="Запустить сейчас? (1=HTTPS, 2=HTTP, 3=Не сейчас): "

if "%launch%"=="1" (
    echo.
    echo 🔒 Запускаем HTTPS...
    call run_https.bat
) else if "%launch%"=="2" (
    echo.
    echo 🌐 Запускаем HTTP...
    call run_http.bat
) else (
    echo.
    echo ✅ Готово! Используйте run_https.bat или run_http.bat
)

pause
