@echo off
chcp 65001 >nul
echo FIXING HTTPS/HTTP BROWSER PROBLEM
echo =================================
echo.

call .venv\Scripts\activate

echo 1. Installing django-extensions...
pip install django-extensions[werkzeug] --quiet

echo.
echo 2. Creating SSL certificate...
if not exist ssl mkdir ssl

python -c "
import subprocess
import os
try:
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', 'ssl/key.pem', '-out', 'ssl/cert.pem', '-days', '365', '-nodes', '-subj', '/CN=localhost'], check=True, capture_output=True)
    print('SSL certificate created via OpenSSL')
except:
    try:
        import ssl
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
        ])
        
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(key, hashes.SHA256())
        
        with open('ssl/cert.pem', 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open('ssl/key.pem', 'wb') as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
        
        print('SSL certificate created via Python')
    except ImportError:
        subprocess.run(['pip', 'install', 'cryptography'])
        print('Cryptography installed. Run script again.')
    except Exception as e:
        print(f'Error: {e}')
"

echo.
echo 3. Adding django-extensions to settings...
python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()
if 'django_extensions' not in content:
    content = content.replace('THIRD_PARTY_APPS = [', 'THIRD_PARTY_APPS = [\n    \"django_extensions\",')
    with open('config/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('django-extensions added')
"

echo.
echo 4. Creating startup scripts...
echo python manage.py runserver 127.0.0.1:8000 > http.bat
echo python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000 > https.bat

echo.
echo 5. Clearing browser cache instructions...
echo.
echo IMPORTANT: Clear your browser cache first!
echo.
echo Chrome/Edge: Press Ctrl+Shift+Delete, select "All time", clear all
echo Firefox: Press Ctrl+Shift+Delete, select "Everything", clear all
echo.
echo Also clear HSTS in Chrome: chrome://net-internals/#hsts
echo Delete domain: localhost and 127.0.0.1
echo.

set /p cleared="Did you clear browser cache? (y/n): "
if /i "%cleared%" neq "y" (
    echo Please clear browser cache first, then run this script again.
    pause
    exit /b 1
)

echo.
echo 6. Choose server type:
echo.
echo 1. HTTP server (http://127.0.0.1:8000/)
echo 2. HTTPS server (https://127.0.0.1:8000/)
echo.

set /p choice="Choose (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting HTTP server...
    echo Open: http://127.0.0.1:8000/
    echo.
    python manage.py runserver 127.0.0.1:8000
) else if "%choice%"=="2" (
    echo.
    echo Starting HTTPS server...
    echo Open: https://127.0.0.1:8000/
    echo Browser will show security warning - click "Advanced" then "Proceed"
    echo.
    python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000
) else (
    echo Invalid choice
)

pause
