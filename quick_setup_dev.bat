@echo off
echo 🔧 НАСТРОЙКА DJANGO ДЛЯ HTTPS
echo ============================
echo.

echo 🔹 Быстрая настройка как было раньше
echo.

set /p mode="Выберите режим: (1) Только HTTP, (2) Только HTTPS, (3) Оба режима: "

call .venv\Scripts\activate

if "%mode%"=="1" goto :http_only
if "%mode%"=="2" goto :https_only
if "%mode%"=="3" goto :both_modes

:http_only
echo.
echo 🌐 Настраиваем только HTTP режим...
python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('SECURE_SSL_REDIRECT = True', 'SECURE_SSL_REDIRECT = False')
if 'SECURE_SSL_REDIRECT = False' not in content:
    content += '\nSECURE_SSL_REDIRECT = False\n'
with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ HTTP режим настроен')
"
echo.
echo ✅ HTTP сервер готов!
echo 🚀 Запуск: python manage.py runserver
echo 🌐 Адрес: http://127.0.0.1:8000/
goto :end

:https_only
echo.
echo 🔒 Настраиваем только HTTPS режим...
call setup_simple_https.bat
goto :end

:both_modes
echo.
echo 🔄 Настраиваем оба режима...

REM Устанавливаем django-extensions
pip install django-extensions[werkzeug] --quiet

REM Создаем SSL если нужно
if not exist ssl\cert.pem (
    if not exist ssl mkdir ssl
    python create_ssl_cert.py
)

REM Обновляем settings.py
python -c "
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'django_extensions' not in content:
    content = content.replace('THIRD_PARTY_APPS = [', 'THIRD_PARTY_APPS = [\\n    \"django_extensions\",')

# Отключаем принуждение к HTTPS для гибкости
content = content.replace('SECURE_SSL_REDIRECT = True', 'SECURE_SSL_REDIRECT = False')
if 'SECURE_SSL_REDIRECT = False' not in content:
    content += '\nSECURE_SSL_REDIRECT = False\n'

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Настройки обновлены')
"

REM Создаем простые скрипты
echo python manage.py runserver 127.0.0.1:8000 > http.bat
echo python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000 > https.bat

echo.
echo ✅ Оба режима готовы!
echo.
echo 🌐 HTTP:  http.bat  → http://127.0.0.1:8000/
echo 🔒 HTTPS: https.bat → https://127.0.0.1:8000/

:end
echo.
set /p start_now="Запустить сервер сейчас? (h=HTTP, s=HTTPS, n=Нет): "

if /i "%start_now%"=="h" (
    echo.
    echo 🌐 Запускаем HTTP...
    python manage.py runserver 127.0.0.1:8000
) else if /i "%start_now%"=="s" (
    echo.
    echo 🔒 Запускаем HTTPS...
    if exist ssl\cert.pem (
        python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 127.0.0.1:8000
    ) else (
        echo ❌ SSL сертификат не найден. Сначала настройте HTTPS.
    )
)

pause
