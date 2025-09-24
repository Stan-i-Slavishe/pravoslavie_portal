#!/bin/bash

# 🧪 Быстрый тест настройки reCAPTCHA для регистрации

echo "🛡️ ТЕСТ GOOGLE reCAPTCHA v3 - ФОРМА РЕГИСТРАЦИИ"
echo "=================================================="

# Проверяем, что мы в правильной директории
if [ ! -f "manage.py" ]; then
    echo "❌ Файл manage.py не найден!"
    echo "   Убедитесь что вы находитесь в корневой директории проекта"
    exit 1
fi

echo "📂 Рабочая директория: $(pwd)"
echo ""

# Проверяем Python зависимости
echo "🔍 Проверка зависимостей..."
echo "--------------------------------"

# Проверяем django-recaptcha
if python -c "import django_recaptcha" 2>/dev/null; then
    echo "✅ django-recaptcha установлен"
else
    echo "❌ django-recaptcha НЕ установлен!"
    echo "   Установите: pip install django-recaptcha==4.0.0"
    exit 1
fi

# Проверяем django-allauth
if python -c "import allauth" 2>/dev/null; then
    echo "✅ django-allauth установлен"
else
    echo "❌ django-allauth НЕ установлен!"
    exit 1
fi

echo ""

# Запускаем Python тест
echo "🧪 Запуск детального теста настроек..."
echo "--------------------------------------"
python test_recaptcha_setup.py

# Проверяем результат
if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 ТЕСТ ЗАВЕРШЕН УСПЕШНО!"
    echo "========================="
    echo ""
    echo "📋 Следующие шаги:"
    echo "   1. Запуск сервера разработки:"
    echo "      python manage.py runserver"
    echo ""
    echo "   2. Тестирование в браузере:"
    echo "      http://127.0.0.1:8000/accounts/signup/"
    echo ""
    echo "   3. Деплой на продакшен:"
    echo "      git add ."
    echo "      git commit -m 'Добавлена reCAPTCHA в форму регистрации'"
    echo "      git push origin main"
    echo "      ./deploy.sh"
    echo ""
    echo "🔗 Мониторинг reCAPTCHA:"
    echo "   https://www.google.com/recaptcha/admin"
else
    echo ""
    echo "⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!"
    echo "======================="
    echo ""
    echo "📋 Возможные решения:"
    echo "   • Установите зависимости: pip install -r requirements.txt"
    echo "   • Проверьте настройки в config/settings*.py"
    echo "   • Убедитесь что ключи reCAPTCHA корректны"
    echo ""
    exit 1
fi
