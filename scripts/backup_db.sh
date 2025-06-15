#!/bin/bash

# Создаем папку для скриптов
mkdir -p scripts

# Создаем скрипт бэкапа
cat > scripts/backup_db.sh << 'EOF'
#!/bin/bash

# Настройки
DB_NAME="pravoslavie_portal_db"
DB_USER="pravoslavie_user"
BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Создаем папку для бэкапов
mkdir -p $BACKUP_DIR

# Создаем бэкап
pg_dump -h localhost -U $DB_USER -d $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Удаляем старые бэкапы (старше 7 дней)
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Backup created: $BACKUP_DIR/backup_$DATE.sql"
EOF

# Делаем скрипт исполняемым
chmod +x scripts/backup_db.sh