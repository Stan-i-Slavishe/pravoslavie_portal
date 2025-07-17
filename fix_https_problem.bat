@echo off
echo 🚨 БЫСТРОЕ ИСПРАВЛЕНИЕ HTTPS/HTTP ПРОБЛЕМЫ
echo ========================================
echo.

echo Django запускается, но браузер не может подключиться из-за HTTPS/HTTP конфликта
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

echo 1️⃣  Останавливаем Django...
taskkill /f /im python.exe 2>nul

echo.
echo 2️⃣  Исправляем настройки HTTPS/HTTP...
call .venv\Scripts\activate

REM Быстрое исправление settings.py
python -c "
import re
with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Отключаем все HTTPS принуждения
fixes = [
    ('SECURE_SSL_REDIRECT = True', 'SECURE_SSL_REDIRECT = False'),
    ('SESSION_COOKIE_SECURE = True', 'SESSION_COOKIE_SECURE = False'),
    ('CSRF_COOKIE_SECURE = True', 'CSRF_COOKIE_SECURE = False'),
    ('SECURE_HSTS_SECONDS = ', '# SECURE_HSTS_SECONDS = '),
]

for old, new in fixes:
    content = content.replace(old, new)

# Добавляем настройки если их нет
if 'SECURE_SSL_REDIRECT' not in content:
    content += '\n# Отключаем HTTPS для разработки\nSECURE_SSL_REDIRECT = False\n'
if 'SESSION_COOKIE_SECURE' not in content:
    content += 'SESSION_COOKIE_SECURE = False\n'
if 'CSRF_COOKIE_SECURE' not in content:
    content += 'CSRF_COOKIE_SECURE = False\n'

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ HTTPS настройки отключены')
"

echo.
echo 3️⃣  Очищаем Django сессии и кеш...
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
    print('⚠️ Не удалось очистить сессии')

try:
    from django.core.cache import cache
    cache.clear()
    print('✅ Кеш очищен')
except:
    print('⚠️ Не удалось очистить кеш')
"

echo.
echo 4️⃣  Создаем HTML файл для перенаправления...
echo ^<!DOCTYPE html^> > open_django.html
echo ^<html^> >> open_django.html
echo ^<head^> >> open_django.html
echo     ^<title^>Django Portal^</title^> >> open_django.html
echo     ^<meta http-equiv="refresh" content="1;url=http://127.0.0.1:8000/"^> >> open_django.html
echo ^</head^> >> open_django.html
echo ^<body^> >> open_django.html
echo     ^<h1^>Перенаправление на Django...^</h1^> >> open_django.html
echo     ^<p^>Если автоматическое перенаправление не работает:^</p^> >> open_django.html
echo     ^<h2^>^<a href="http://127.0.0.1:8000/"^>НАЖМИТЕ СЮДА^</a^>^</h2^> >> open_django.html
echo     ^<p^>Адрес: ^<code^>http://127.0.0.1:8000/^</code^>^</p^> >> open_django.html
echo ^</body^> >> open_django.html
echo ^</html^> >> open_django.html

echo ✅ Создан файл open_django.html

echo.
echo 5️⃣  Запускаем Django сервер...
echo.
echo 🎯 ВАЖНО! После запуска сервера:
echo.
echo    ✅ ПРАВИЛЬНО: http://127.0.0.1:8000/
echo    ❌ НЕПРАВИЛЬНО: https://127.0.0.1:8000/
echo.
echo    💡 Если браузер не открывается:
echo       1. Откройте файл open_django.html
echo       2. Или скопируйте: http://127.0.0.1:8000/
echo       3. Или используйте режим инкогнито
echo.

REM Ждем нажатия клавиши
set /p ready="Нажмите Enter для запуска сервера..."

echo.
echo 🚀 Запускаем Django...
python manage.py runserver 127.0.0.1:8000

pause
