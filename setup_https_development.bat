@echo off
echo 🔒 НАСТРОЙКА HTTPS ДЛЯ DJANGO РАЗРАБОТКИ
echo =======================================
echo.

echo 🔹 Настраиваем HTTPS для тестирования платежей YooKassa/Stripe
echo 🔹 Создаем самоподписанный SSL сертификат
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

call .venv\Scripts\activate

echo 1️⃣  Устанавливаем необходимые пакеты...
pip install django-extensions[werkzeug] --quiet
pip install pyopenssl --quiet

echo.
echo 2️⃣  Создаем директорию для SSL сертификатов...
if not exist ssl mkdir ssl

echo.
echo 3️⃣  Генерируем самоподписанный SSL сертификат...

python -c "
import os
import subprocess
from pathlib import Path

ssl_dir = Path('ssl')
cert_file = ssl_dir / 'cert.pem'
key_file = ssl_dir / 'key.pem'

try:
    # Пробуем использовать OpenSSL
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', str(key_file), '-out', str(cert_file),
        '-days', '365', '-nodes', '-batch',
        '-subj', '/C=RU/ST=Moscow/L=Moscow/O=DevServer/CN=localhost'
    ], check=True, capture_output=True)
    print('✅ SSL сертификат создан через OpenSSL')
    
except (FileNotFoundError, subprocess.CalledProcessError):
    # Если OpenSSL недоступен, создаем через Python
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        # Генерируем приватный ключ
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Создаем сертификат
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'RU'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Moscow'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, 'Moscow'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Django Dev Server'),
            x509.NameAttribute(NameOID.COMMON_NAME, 'localhost'),
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
                x509.DNSName('localhost'),
                x509.DNSName('127.0.0.1'),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Сохраняем сертификат
        with open(cert_file, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Сохраняем приватный ключ
        with open(key_file, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print('✅ SSL сертификат создан через Python cryptography')
        
    except ImportError:
        print('⚠️ Устанавливаем cryptography...')
        subprocess.run(['pip', 'install', 'cryptography'], check=True)
        print('🔄 Перезапустите скрипт после установки cryptography')
        exit(1)
        
    except Exception as e:
        print(f'❌ Ошибка создания сертификата: {e}')
        exit(1)
"

if %ERRORLEVEL% neq 0 (
    echo ❌ Ошибка при создании сертификата
    pause
    exit /b 1
)

echo.
echo 4️⃣  Добавляем django-extensions в настройки...

python -c "
import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Добавляем django_extensions в THIRD_PARTY_APPS если его еще нет
if 'django_extensions' not in content:
    content = re.sub(
        r'(THIRD_PARTY_APPS\s*=\s*\[)',
        r'\1\n    \"django_extensions\",  # Для HTTPS в разработке',
        content
    )

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ django-extensions добавлен в настройки')
"

echo.
echo 5️⃣  Настраиваем HTTPS настройки для разработки...

python -c "
import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем старые настройки безопасности если есть
content = re.sub(r'# Отключаем HTTPS для разработки.*?\n', '', content, flags=re.DOTALL)
content = re.sub(r'SECURE_SSL_REDIRECT\s*=\s*False.*?\n', '', content)
content = re.sub(r'SESSION_COOKIE_SECURE\s*=\s*False.*?\n', '', content)
content = re.sub(r'CSRF_COOKIE_SECURE\s*=\s*False.*?\n', '', content)

# Добавляем правильные HTTPS настройки для разработки
https_settings = '''

# HTTPS настройки для разработки с платежами
if DEBUG:
    # В разработке не принуждаем к HTTPS (для гибкости)
    SECURE_SSL_REDIRECT = False
    # Но настраиваем secure cookies для HTTPS запросов
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Отключаем HSTS для разработки
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Продакшен настройки
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Настройки для работы с платежными системами
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
'''

content += https_settings

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ HTTPS настройки добавлены')
"

echo.
echo 6️⃣  Создаем скрипт запуска HTTPS сервера...

echo @echo off > start_https_server.bat
echo echo 🔒 ЗАПУСК DJANGO HTTPS СЕРВЕРА >> start_https_server.bat
echo echo ============================== >> start_https_server.bat
echo echo. >> start_https_server.bat
echo call .venv\Scripts\activate >> start_https_server.bat
echo echo ✅ Запускаем Django с HTTPS... >> start_https_server.bat
echo echo. >> start_https_server.bat
echo echo 🌐 Сервер будет доступен по адресу: >> start_https_server.bat
echo echo    https://127.0.0.1:8000/ >> start_https_server.bat
echo echo. >> start_https_server.bat
echo echo ⚠️  ВАЖНО: Браузер покажет предупреждение о сертификате >> start_https_server.bat
echo echo    Нажмите "Дополнительно" ^-^> "Перейти на 127.0.0.1" >> start_https_server.bat
echo echo. >> start_https_server.bat
echo python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000 >> start_https_server.bat
echo pause >> start_https_server.bat

echo ✅ Скрипт start_https_server.bat создан

echo.
echo 7️⃣  Создаем скрипт запуска обычного HTTP сервера...

echo @echo off > start_http_server.bat
echo echo 🌐 ЗАПУСК DJANGO HTTP СЕРВЕРА >> start_http_server.bat
echo echo ============================= >> start_http_server.bat
echo echo. >> start_http_server.bat
echo call .venv\Scripts\activate >> start_http_server.bat
echo echo ✅ Запускаем Django с HTTP... >> start_http_server.bat
echo echo. >> start_http_server.bat
echo echo 🌐 Сервер будет доступен по адресу: >> start_http_server.bat
echo echo    http://127.0.0.1:8000/ >> start_http_server.bat
echo echo. >> start_http_server.bat
echo python manage.py runserver 127.0.0.1:8000 >> start_http_server.bat
echo pause >> start_http_server.bat

echo ✅ Скрипт start_http_server.bat создан

echo.
echo 8️⃣  Очищаем кеш и сессии...
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
try:
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
    print('✅ Сессии очищены')
except:
    pass
try:
    from django.core.cache import cache
    cache.clear()
    print('✅ Кеш очищен')
except:
    pass
"

echo.
echo 🎉 HTTPS НАСТРОЙКА ЗАВЕРШЕНА!
echo =============================
echo.
echo 📋 ЧТО БЫЛО НАСТРОЕНО:
echo   ✅ Установлен django-extensions
echo   ✅ Создан самоподписанный SSL сертификат
echo   ✅ Настроены HTTPS параметры Django
echo   ✅ Созданы скрипты запуска
echo.
echo 🚀 ВАРИАНТЫ ЗАПУСКА:
echo.
echo   🔒 HTTPS (для платежей): start_https_server.bat
echo      Адрес: https://127.0.0.1:8000/
echo.
echo   🌐 HTTP (обычная разработка): start_http_server.bat
echo      Адрес: http://127.0.0.1:8000/
echo.
echo 💡 РЕКОМЕНДАЦИИ:
echo   • Для тестирования YooKassa/Stripe - используйте HTTPS
echo   • Для обычной разработки - используйте HTTP
echo   • Оба режима настроены и готовы к работе
echo.
echo ⚠️  ПРИ ПЕРВОМ ЗАПУСКЕ HTTPS:
echo   1. Браузер покажет предупреждение о сертификате
echo   2. Нажмите "Дополнительно"
echo   3. Выберите "Перейти на 127.0.0.1 (небезопасно)"
echo   4. Это нормально для разработки!
echo.

set /p launch_choice="Запустить сервер сейчас? (1=HTTPS, 2=HTTP, 3=Нет): "

if "%launch_choice%"=="1" (
    echo.
    echo 🔒 Запускаем HTTPS сервер...
    call start_https_server.bat
) else if "%launch_choice%"=="2" (
    echo.
    echo 🌐 Запускаем HTTP сервер...
    call start_http_server.bat
) else (
    echo.
    echo ✅ Настройка завершена! Используйте скрипты запуска когда будете готовы.
)

pause
