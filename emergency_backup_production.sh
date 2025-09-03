#!/bin/bash
# АВАРИЙНЫЙ BACKUP РАБОЧЕЙ КОНФИГУРАЦИИ ПРОДАКШЕНА

echo "🚨 Создаем аварийный backup рабочих настроек продакшена..."

# Создаем папку для backup
mkdir -p backups/working_production_$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/working_production_$(date +%Y%m%d_%H%M%S)"

# Копируем ВСЕ настройки, которые сейчас работают
cp .env.production $BACKUP_DIR/
cp config/settings_production.py $BACKUP_DIR/
cp config/settings.py $BACKUP_DIR/

# Записываем текущие переменные окружения
echo "DJANGO_ENV=$(printenv DJANGO_ENV)" > $BACKUP_DIR/current_env_vars.txt
echo "DEBUG=$(printenv DEBUG)" >> $BACKUP_DIR/current_env_vars.txt

echo "✅ Backup создан в $BACKUP_DIR"
echo "🔒 Эти файлы НИ В КОЕМ СЛУЧАЕ НЕ ТРОГАТЬ - это ваша страховка!"
