#!/bin/bash

# 🚀 Деплой с проверкой Google reCAPTCHA v3

echo "🚀 ДЕПЛОЙ ПРАВОСЛАВНОГО ПОРТАЛА С reCAPTCHA"
echo "=============================================="

# Проверяем что мы в правильной директории
if [ ! -f "manage.py" ]; then
    echo "❌ Файл manage.py не найден!"
    echo "   Убедитесь что вы находитесь в корневой директории проекта"
    exit 1
fi

echo "📂 Рабочая директория: $(pwd)"
echo ""

# Проверяем готовность к деплою
echo "🔍 Проверка готовности к продакшен деплою..."
echo "----------------------------------------------"

# Запускаем проверку настроек продакшена
echo "🧪 Запуск проверки reCAPTCHA настроек..."
python check_production_recaptcha.py

# Проверяем результат проверки
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️ ПРОВЕРКА ПРОВАЛИЛАСЬ!"
    echo "========================"
    echo ""
    echo "❌ Обнаружены проблемы с настройками reCAPTCHA"
    echo "   Исправьте проблемы перед деплоем"
    echo ""
    exit 1
fi

echo ""
echo "✅ ПРОВЕРКА ПРОЙДЕНА! Начинаем деплой..."
echo "========================================"

# Проверяем что все изменения закоммичены
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "⚠️ У вас есть незакоммиченные изменения!"
    echo "   Хотите закоммитить их автоматически? (y/n)"
    read -p "Введите y для автокоммита или n для отмены: " choice
    
    case "$choice" in 
        y|Y ) 
            echo "📝 Автоматический коммит изменений..."
            git add .
            git commit -m "🔒 Настроена Google reCAPTCHA v3 для продакшена

✅ Изменения:
- Условная reCAPTCHA (отключена в DEBUG режиме) 
- Продакшен: полная защита с реальными ключами
- Разработка: упрощенное тестирование без капчи
- Настройки домена dobrist.com проверены
- Готово к коммерческому использованию

🛡️ Защита от ботов активирована на продакшене!"
            ;;
        n|N ) 
            echo "❌ Деплой отменен. Закоммитьте изменения вручную"
            exit 1
            ;;
        * ) 
            echo "❌ Неверный ввод. Деплой отменен"
            exit 1
            ;;
    esac
fi

# Пушим изменения
echo ""
echo "📤 Отправка изменений на сервер..."
git push origin main

if [ $? -ne 0 ]; then
    echo "❌ Ошибка при отправке на сервер!"
    exit 1
fi

# Деплой на сервер
echo ""
echo "🚀 Запуск деплоя на продакшен сервер..."
echo "======================================"

# Проверяем есть ли ./deploy.sh
if [ -f "./deploy.sh" ]; then
    chmod +x ./deploy.sh
    ./deploy.sh
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 ДЕПЛОЙ УСПЕШНО ЗАВЕРШЕН!"
        echo "=========================="
        echo ""
        echo "✅ reCAPTCHA активирована на продакшене"
        echo "✅ Форма регистрации защищена от ботов"
        echo "✅ Порог безопасности: 0.85 (высокий)"
        echo ""
        echo "🔗 Полезные ссылки:"
        echo "   • Тест формы: https://dobrist.com/accounts/signup/"
        echo "   • reCAPTCHA Admin: https://www.google.com/recaptcha/admin"
        echo "   • Мониторинг: https://dobrist.com/admin/"
        echo ""
        echo "📊 Рекомендации после деплоя:"
        echo "   1. Протестируйте регистрацию новых пользователей"
        echo "   2. Проверьте статистику в Google reCAPTCHA Admin"
        echo "   3. Мониторьте логи на предмет ошибок капчи"
        echo "   4. При необходимости скорректируйте RECAPTCHA_REQUIRED_SCORE"
        
    else
        echo "❌ Ошибка при деплое на сервер!"
        exit 1
    fi
else
    echo "⚠️ Файл deploy.sh не найден!"
    echo "   Выполните деплой вручную на сервере:"
    echo ""
    echo "   ssh your-server"
    echo "   cd /path/to/pravoslavie_portal"
    echo "   git pull origin main"
    echo "   pip install -r requirements.txt"
    echo "   python manage.py migrate"
    echo "   python manage.py collectstatic --noinput"
    echo "   sudo systemctl restart gunicorn"
    echo "   sudo systemctl restart nginx"
fi

echo ""
echo "🔒 reCAPTCHA деплой завершен!"
