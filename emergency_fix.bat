@echo off
echo 🛑 ОСТАНОВКА СЕРВЕРА И БЫСТРОЕ ИСПРАВЛЕНИЕ
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Редактирование MIDDLEWARE в settings.py...

REM Создаем временный Python скрипт для удаления middleware безопасности
echo import re > temp_fix.py
echo. >> temp_fix.py
echo with open('config/settings.py', 'r', encoding='utf-8') as f: >> temp_fix.py
echo     content = f.read() >> temp_fix.py
echo. >> temp_fix.py
echo # Удаляем middleware безопасности из MIDDLEWARE списка >> temp_fix.py
echo content = re.sub(r"'core\.middleware\.security\.\w+',?\s*\n", '', content) >> temp_fix.py
echo. >> temp_fix.py
echo # Убираем пустые строки в MIDDLEWARE >> temp_fix.py
echo content = re.sub(r'MIDDLEWARE = \[\s*\n(\s*#[^\n]*\n)*', 'MIDDLEWARE = [\n', content) >> temp_fix.py
echo. >> temp_fix.py
echo # Принудительно устанавливаем локальное кеширование >> temp_fix.py
echo if 'REDIS_URL' in content: >> temp_fix.py
echo     content = re.sub(r"CACHES = \{[^}]+\}", "CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'unique-snowflake'}}", content, flags=re.DOTALL) >> temp_fix.py
echo. >> temp_fix.py
echo with open('config/settings.py', 'w', encoding='utf-8') as f: >> temp_fix.py
echo     f.write(content) >> temp_fix.py
echo. >> temp_fix.py
echo print('✅ Middleware безопасности удален из settings.py') >> temp_fix.py

python temp_fix.py
del temp_fix.py

echo.
echo ✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!
echo 🚀 Запуск исправленного сервера...
python manage.py runserver

pause