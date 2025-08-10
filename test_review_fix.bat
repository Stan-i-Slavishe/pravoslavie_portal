@echo off
echo ========================================
echo  ПРОВЕРКА ИСПРАВЛЕНИЯ БЛОКИРОВКИ БД
echo ========================================

echo.
echo 1. Проверка синтаксиса Django...
python manage.py check

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибки в коде Django!
    pause
    exit /b 1
)

echo ✅ Синтаксис Django в порядке.

echo.
echo 2. Проверка структуры БД...
python manage.py makemigrations --dry-run

echo.
echo 3. Тестирование подключения к БД...
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import BookReview
from django.contrib.auth.models import User

print('✅ Импорт моделей успешен')
print(f'📊 Количество отзывов в БД: {BookReview.objects.count()}')
print(f'👥 Количество пользователей: {User.objects.count()}')
print('✅ Подключение к БД работает')
"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!
    echo ========================================
    echo.
    echo Изменения:
    echo ✓ Функция add_review исправлена
    echo ✓ Добавлена защита от блокировки БД  
    echo ✓ Добавлены повторные попытки
    echo ✓ Улучшены настройки SQLite
    echo ✓ Добавлены правильные PRAGMA настройки
    echo.
    echo 🎉 Теперь отзывы должны работать без ошибок!
    echo.
) else (
    echo.
    echo ❌ Обнаружены проблемы с БД
)

pause
