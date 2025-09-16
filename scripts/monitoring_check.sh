#!/bin/bash
# 🤖 Основной скрипт мониторинга
# Создан автоматически для интеграции системы мониторинга

# Настройки
PROJECT_DIR="E:/pravoslavie_portal"
PYTHON_PATH="python"
MANAGE_PY="$PROJECT_DIR/manage.py"
LOG_FILE="$PROJECT_DIR/logs/monitoring_cron.log"

# Функция логирования
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Проверка системных ресурсов
check_system() {
    log_message "🔍 Запуск проверки системы..."
    
    cd "$PROJECT_DIR"
    export DJANGO_ENV=production
    
    $PYTHON_PATH $MANAGE_PY monitor_system --check-all --send-alerts >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "✅ Проверка системы завершена успешно"
    else
        log_message "❌ Ошибка при проверке системы"
    fi
}

# Очистка старых логов
cleanup_logs() {
    log_message "🧹 Запуск очистки логов..."
    
    cd "$PROJECT_DIR"
    export DJANGO_ENV=production
    
    $PYTHON_PATH $MANAGE_PY cleanup_logs --days=7 >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "✅ Очистка логов завершена"
    else
        log_message "❌ Ошибка при очистке логов"
    fi
}

# Создание отчета
generate_report() {
    log_message "📊 Создание отчета мониторинга..."
    
    cd "$PROJECT_DIR"
    export DJANGO_ENV=production
    
    REPORT_FILE="$PROJECT_DIR/logs/monitoring_report_$(date +%Y%m%d_%H%M).txt"
    
    $PYTHON_PATH $MANAGE_PY monitoring_report --hours=24 --save="$REPORT_FILE" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "✅ Отчет создан: $REPORT_FILE"
    else
        log_message "❌ Ошибка создания отчета"
    fi
}

# Проверка здоровья сервисов
health_check() {
    log_message "❤️ Проверка здоровья сервисов..."
    
    # Проверка Django (для локальной разработки)
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health/simple/ | grep -q "200"; then
        log_message "✅ Django приложение: OK"
    else
        log_message "❌ Django приложение: FAILED"
        send_critical_alert "Django приложение недоступно"
    fi
}

# Отправка критического алерта
send_critical_alert() {
    local message="$1"
    log_message "🚨 КРИТИЧЕСКИЙ АЛЕРТ: $message"
    
    # Здесь можно добавить отправку email или Telegram уведомлений
    echo "КРИТИЧЕСКИЙ АЛЕРТ: $message" >> "$PROJECT_DIR/logs/critical_alerts.log"
}

# Основная логика
case "$1" in
    "system")
        check_system
        ;;
    "cleanup")
        cleanup_logs
        ;;
    "report")
        generate_report
        ;;
    "health")
        health_check
        ;;
    "all")
        health_check
        check_system
        ;;
    *)
        echo "Использование: $0 {system|cleanup|report|health|all}"
        echo "  system  - Проверка системных ресурсов"
        echo "  cleanup - Очистка старых логов"
        echo "  report  - Создание отчета"
        echo "  health  - Проверка здоровья сервисов"
        echo "  all     - Полная проверка"
        exit 1
        ;;
esac
