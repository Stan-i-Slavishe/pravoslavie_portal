@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 ИСПРАВЛЕНИЕ ПЕТРОВА ПОСТА
echo ========================================
echo.

cd /d E:\pravoslavie_portal

echo 📦 Шаг 1: Создание миграций...
python manage.py makemigrations pwa
if %errorlevel% neq 0 (
    echo ❌ Ошибка создания миграций
    pause
    exit /b 1
)

echo.
echo 🔧 Шаг 2: Применение миграций...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Ошибка применения миграций
    pause
    exit /b 1
)

echo.
echo ⛪ Шаг 3: Добавление Петрова поста...
python -c "
import os, sys, django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import FastingPeriod

# Удаляем старый (если есть)
FastingPeriod.objects.filter(name='peter_paul_fast').delete()

# Создаем Петров пост
petrov = FastingPeriod.objects.create(
    name='peter_paul_fast',
    title='Петров пост (Апостольский пост)',
    description='Пост в честь святых апостолов Петра и Павла',
    easter_start_offset=57,
    easter_end_offset=None,
    end_month=7,
    end_day=12,
    fasting_rules={
        'monday': 'strict_fast',
        'tuesday': 'with_fish', 
        'wednesday': 'strict_fast',
        'thursday': 'with_fish',
        'friday': 'strict_fast',
        'saturday': 'with_fish',
        'sunday': 'with_fish'
    },
    priority=8,
    is_active=True
)

print(f'✅ Петров пост создан: {petrov.title}')
print(f'   ID: {petrov.id}')
print(f'   Приоритет: {petrov.priority}')

# Тестируем
from datetime import date
test_date = date(2026, 6, 15)
is_active = petrov.is_active_for_date(test_date)
print(f'   Тест 15.06.2026: {\"✅ Активен\" if is_active else \"❌ Не активен\"}')
"

if %errorlevel% neq 0 (
    echo ❌ Ошибка добавления Петрова поста
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 УСПЕШНО ЗАВЕРШЕНО!
echo ========================================
echo.
echo ✅ Светлая седмица исправлена (13-19 апреля 2026)
echo ✅ Петров пост добавлен (8 июня - 12 июля 2026)
echo.
echo 🎯 РЕЗУЛЬТАТ В КАЛЕНДАРЕ:
echo    📅 Июнь 2026:
echo       🟢 1-7 июня  = Троицкая седмица (зеленый)
echo       🟣 8-30 июня = Петров пост (фиолетовый)
echo    📅 Июль 2026:
echo       🟣 1-12 июля = Петров пост (фиолетовый)
echo.
echo 🔄 Запускаю сервер...
echo.
python manage.py runserver
