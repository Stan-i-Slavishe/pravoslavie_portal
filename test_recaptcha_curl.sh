#!/bin/bash

# Тест блокировки Google reCAPTCHA v3 через curl с CSRF токеном

echo "🤖 ТЕСТ БЛОКИРОВКИ GOOGLE reCAPTCHA v3"
echo "======================================"
echo ""

URL="https://dobrist.com/accounts/signup/"

# Шаг 1: Получаем страницу с формой и извлекаем CSRF токен
echo "📥 Получаем CSRF токен..."
RESPONSE=$(curl -s -c cookies.txt "$URL")
CSRF_TOKEN=$(echo "$RESPONSE" | grep -oP 'csrfmiddlewaretoken.*?value="\K[^"]+' | head -1)

if [ -z "$CSRF_TOKEN" ]; then
    echo "❌ Не удалось получить CSRF токен"
    exit 1
fi

echo "✅ CSRF токен получен: ${CSRF_TOKEN:0:20}..."
echo ""

# Шаг 2: Отправляем 10 запросов подряд
echo "🔄 Отправляем множественные запросы регистрации..."
echo ""

for i in {1..10}; do
    echo "Попытка $i/10..."
    
    RESPONSE=$(curl -s -b cookies.txt -c cookies.txt \
        -X POST "$URL" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Referer: $URL" \
        -d "csrfmiddlewaretoken=$CSRF_TOKEN" \
        -d "email=bot-test-$i@example.com" \
        -d "password1=BotPassword123!" \
        -d "password2=BotPassword123!")
    
    # Проверяем наличие ошибок reCAPTCHA
    if echo "$RESPONSE" | grep -qi "recaptcha\|captcha"; then
        echo "❌ ЗАБЛОКИРОВАНО reCAPTCHA!"
        echo ""
        echo "📊 Фрагмент ответа:"
        echo "$RESPONSE" | grep -i "captcha" | head -5
        exit 0
    fi
    
    # Проверяем успешную регистрацию
    if echo "$RESPONSE" | grep -qi "success\|успешно"; then
        echo "⚠️ Запрос прошёл (пока не заблокирован)"
    else
        echo "🔍 Проверяем код ответа..."
    fi
    
    # Небольшая задержка (бот-поведение)
    sleep 0.05
done

echo ""
echo "⚠️ reCAPTCHA не сработала после 10 попыток"
echo "Возможные причины:"
echo "  • Google ещё не собрал достаточно данных о сайте"
echo "  • Порог 0.85 недостаточно строгий для curl запросов"
echo "  • Нужно больше запросов для триггера"

# Очистка
rm -f cookies.txt
