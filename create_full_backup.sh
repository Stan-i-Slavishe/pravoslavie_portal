#!/bin/bash
# 🚨 АВАРИЙНЫЙ BACKUP ВСЕХ РАБОЧИХ НАСТРОЕК ПРОДАКШЕНА
# Дата создания: $(date)
# ВАЖНО: Эти файлы - ваша страховка! НЕ УДАЛЯЙТЕ!

echo "🚨 Создаем ПОЛНЫЙ backup рабочих настроек..."

# Получаем текущую дату и время
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/WORKING_PRODUCTION_BACKUP_$TIMESTAMP"

# Создаем папку для backup
mkdir -p $BACKUP_DIR

echo "📁 Backup папка: $BACKUP_DIR"

# === КОПИРУЕМ ВСЕ КОНФИГУРАЦИОННЫЕ ФАЙЛЫ ===
echo "🔧 Копируем конфигурационные файлы..."

# Все .env файлы
cp .env $BACKUP_DIR/dot_env_current 2>/dev/null || echo "⚠️ .env не найден"
cp .env.production $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.production не найден"
cp .env.local $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.local не найден"
cp .env.lightweight $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.lightweight не найден"
cp .env.postgres_local $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.postgres_local не найден"
cp .env.push_test $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.push_test не найден"
cp .env.temp $BACKUP_DIR/ 2>/dev/null || echo "⚠️ .env.temp не найден"

# Django settings
cp -r config/ $BACKUP_DIR/config_backup/

# Requirements
cp requirements.txt $BACKUP_DIR/

# === ЗАПИСЫВАЕМ СИСТЕМНУЮ ИНФОРМАЦИЮ ===
echo "📝 Записываем системную информацию..."

# Текущие переменные окружения
echo "=== ТЕКУЩИЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===" > $BACKUP_DIR/system_info.txt
echo "DJANGO_ENV: $DJANGO_ENV" >> $BACKUP_DIR/system_info.txt
echo "DEBUG: $DEBUG" >> $BACKUP_DIR/system_info.txt
echo "PATH: $PATH" >> $BACKUP_DIR/system_info.txt
echo "" >> $BACKUP_DIR/system_info.txt

# Информация о Python
echo "=== PYTHON ИНФОРМАЦИЯ ===" >> $BACKUP_DIR/system_info.txt
python --version >> $BACKUP_DIR/system_info.txt
which python >> $BACKUP_DIR/system_info.txt
echo "" >> $BACKUP_DIR/system_info.txt

# Установленные пакеты
echo "=== УСТАНОВЛЕННЫЕ PYTHON ПАКЕТЫ ===" >> $BACKUP_DIR/system_info.txt
pip list >> $BACKUP_DIR/system_info.txt 2>/dev/null || pip3 list >> $BACKUP_DIR/system_info.txt 2>/dev/null

# Git информация
echo "=== GIT ИНФОРМАЦИЯ ===" >> $BACKUP_DIR/system_info.txt
git branch >> $BACKUP_DIR/system_info.txt 2>/dev/null || echo "Git не настроен" >> $BACKUP_DIR/system_info.txt
git log --oneline -5 >> $BACKUP_DIR/system_info.txt 2>/dev/null || echo "Git история недоступна" >> $BACKUP_DIR/system_info.txt

# === СОЗДАЕМ ИНСТРУКЦИЮ ПО ВОССТАНОВЛЕНИЮ ===
cat > $BACKUP_DIR/RESTORE_INSTRUCTIONS.md << 'EOF'
# 🚨 ИНСТРУКЦИЯ ПО ВОССТАНОВЛЕНИЮ РАБОЧЕЙ КОНФИГУРАЦИИ

## ЧТО ЗДЕСЬ НАХОДИТСЯ
Этот backup содержит ВСЕ рабочие настройки продакшена на момент создания.

## ФАЙЛЫ В BACKUP:
- `.env.production` - настройки продакшена (ГЛАВНЫЙ ФАЙЛ)
- `dot_env_current` - текущий .env файл
- `config_backup/` - все файлы Django настроек
- `requirements.txt` - список пакетов Python
- `system_info.txt` - информация о системе

## ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ:

### 1. Если продакшен сломался:
```bash
# Восстанавливаем рабочие настройки
cp backups/WORKING_PRODUCTION_BACKUP_*/env.production .env.production
cp -r backups/WORKING_PRODUCTION_BACKUP_*/config_backup/* config/

# Устанавливаем переменную окружения
export DJANGO_ENV=production

# Перезапускаем сервер
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### 2. Если нужно откатить изменения:
```bash
# Откатываемся к рабочей версии
git stash  # сохраняем текущие изменения
# копируем файлы из backup (как в п.1)
```

## ⚠️ ВАЖНО:
- НЕ УДАЛЯЙТЕ этот backup!
- Перед любыми изменениями на продакшене создавайте новый backup
- Всегда тестируйте изменения на staging перед продакшеном

EOF

# === СОЗДАЕМ КРАТКУЮ СПРАВКУ ===
cat > $BACKUP_DIR/QUICK_REFERENCE.txt << 'EOF'
🚨 БЫСТРАЯ СПРАВКА - АВАРИЙНОЕ ВОССТАНОВЛЕНИЕ

ЕСЛИ САЙТ НЕ РАБОТАЕТ:
1. cd /path/to/project
2. cp этот_backup/.env.production .env.production
3. export DJANGO_ENV=production
4. sudo systemctl restart gunicorn
5. sudo systemctl restart nginx

ЕСЛИ НЕ ПОМОГЛО:
1. Проверить логи: sudo journalctl -u gunicorn
2. Проверить nginx: sudo nginx -t
3. Проверить БД: python manage.py dbshell

ПОМОЩЬ: найти последний working backup в папке backups/
EOF

echo "✅ Backup создан успешно!"
echo "📁 Местоположение: $BACKUP_DIR"
echo ""
echo "🔒 ВАЖНО: Этот backup содержит рабочие настройки продакшена!"
echo "📋 Инструкции по восстановлению: $BACKUP_DIR/RESTORE_INSTRUCTIONS.md"
echo ""
echo "🎯 Следующий шаг: очистка лишних .env файлов"
