#!/bin/bash
# 🔧 Запуск локального сервера разработки
# Файл: run_local.sh

echo "🔧 Запуск локального сервера разработки..."

# Копируем локальные настройки в основной .env файл
cp .env.local .env

# Активируем виртуальное окружение (если есть)
if [ -d ".venv" ]; then
    echo "📦 Активация виртуального окружения..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "📦 Активация виртуального окружения..."
    source venv/bin/activate
fi

# Устанавливаем зависимости если нужно
if [ ! -f "requirements_installed.flag" ]; then
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
    touch requirements_installed.flag
fi

# Создаем папки если нужно
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Миграции
echo "🗄️ Применение миграций..."
python manage.py migrate

# Сбор статики
echo "📁 Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя если нужно
echo "👤 Проверка суперпользователя..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('✅ Создан суперпользователь: admin / admin123')
else:
    print('👤 Суперпользователь уже существует')
"

echo ""
echo "🎉 Локальный сервер готов к запуску!"
echo ""
echo "📋 Полезные команды:"
echo "   🌐 Запуск сервера:     python manage.py runserver"
echo "   🌐 На всех интерфейсах: python manage.py runserver 0.0.0.0:8000"
echo "   👤 Админка:            http://localhost:8000/admin/"
echo "   📧 Почта:              http://localhost:8000/admin/"
echo ""
echo "🚀 Запуск сервера..."
python manage.py runserver
