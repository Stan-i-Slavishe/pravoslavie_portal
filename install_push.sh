#!/bin/bash
# Установка pywebpush для push-уведомлений

echo "🔔 Устанавливаем pywebpush для push-уведомлений..."

pip install pywebpush

echo "✅ pywebpush установлен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Выполните: python generate_vapid_keys.py"
echo "2. Скопируйте ключи в .env файл"
echo "3. Перезапустите сервер"
echo "4. Откройте /push/test/ для тестирования"
