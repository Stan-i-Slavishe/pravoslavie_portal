@echo off
echo 🚀 БЫСТРЫЙ ЗАПУСК HTTPS
echo =====================
echo.

call .venv\Scripts\activate

REM Проверяем есть ли django-extensions
python -c "import django_extensions" 2>nul
if %ERRORLEVEL% neq 0 (
    echo 📦 Устанавливаем django-extensions...
    pip install django-extensions[werkzeug] --quiet
)

REM Проверяем есть ли SSL сертификат
if not exist ssl\cert.pem (
    echo 🔒 Создаем SSL сертификат...
    if not exist ssl mkdir ssl
    
    REM Простой способ создания сертификата
    python -c "
import subprocess
try:
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', 'ssl/key.pem', '-out', 'ssl/cert.pem', '-days', '365', '-nodes', '-subj', '/CN=localhost'], check=True, capture_output=True)
    print('✅ Сертификат создан')
except:
    # Fallback метод
    exec(open('create_ssl_cert.py').read() if __import__('os').path.exists('create_ssl_cert.py') else 'print(\"⚠️ Нужен OpenSSL\")')
    "
)

REM Добавляем django-extensions в настройки если его нет
python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()
if 'django_extensions' not in content:
    content = content.replace('THIRD_PARTY_APPS = [', 'THIRD_PARTY_APPS = [\\n    \"django_extensions\",')
    with open('config/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ django-extensions добавлен')
"

echo.
echo 🔒 Запускаем HTTPS сервер...
echo.
echo    💡 Адрес: https://127.0.0.1:8000/
echo    ⚠️  При предупреждении о сертификате выберите "Перейти на сайт"
echo.

python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000
