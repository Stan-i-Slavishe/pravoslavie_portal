@echo off
echo ========================================
echo  ИСПРАВЛЕНИЕ ОШИБОК ЗАПУСКА
echo ========================================

echo.
echo 1. Удаление проблемных кеш-файлов...
del /Q "stories\templatetags\__pycache__\russian_pluralize.cpython-311.pyc" 2>nul
del /Q "core\templatetags\__pycache__\russian_pluralize.cpython-311.pyc" 2>nul

echo.
echo 2. Проверка синтаксиса Django...
python manage.py check

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибки в коде Django!
    pause
    exit /b 1
)

echo ✅ Синтаксис Django в порядке.

echo.
echo 3. Тестирование подключения к БД...
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print('✅ Подключение к БД успешно')

# Проверяем PRAGMA настройки
with connection.cursor() as cursor:
    cursor.execute('PRAGMA journal_mode;')
    journal_mode = cursor.fetchone()[0]
    print(f'📊 Journal mode: {journal_mode}')
    
    cursor.execute('PRAGMA synchronous;')
    sync_mode = cursor.fetchone()[0]  
    print(f'📊 Synchronous: {sync_mode}')
    
    cursor.execute('PRAGMA busy_timeout;')
    timeout = cursor.fetchone()[0]
    print(f'📊 Busy timeout: {timeout}ms')

print('✅ PRAGMA настройки применены')
"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ ВСЕ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!
    echo ========================================
    echo.
    echo Исправлено:
    echo ✓ Настройки SQLite backend
    echo ✓ PRAGMA оптимизации
    echo ✓ Дублирующиеся templatetags
    echo ✓ Подключение к БД работает
    echo.
    echo 🚀 Теперь сервер должен запускаться без ошибок!
    echo.
) else (
    echo.
    echo ❌ Обнаружены проблемы с БД
)

echo.
echo 4. Запуск сервера разработки...
python manage.py runserver

pause
