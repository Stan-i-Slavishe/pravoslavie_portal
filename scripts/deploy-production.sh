#!/bin/bash
# 🚀 Православный портал - Production Deploy Script

set -e  # Exit on any error

echo "🐳 Deploying Pravoslavie Portal to Production..."

# 🔧 Configuration
REPO_URL="https://github.com/yourusername/pravoslavie-portal.git"
DEPLOY_DIR="/opt/pravoslavie-portal"
BACKUP_DIR="/opt/backups/pravoslavie-portal"
DATE=$(date +"%Y%m%d_%H%M%S")

# 🔍 Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    echo "❌ This script must be run as root or with sudo"
    exit 1
fi

# 🛑 Function to rollback on error
rollback() {
    echo "❌ Deployment failed. Rolling back..."
    if [ -d "$BACKUP_DIR/latest" ]; then
        cd "$DEPLOY_DIR"
        docker-compose down
        rm -rf current
        mv "$BACKUP_DIR/latest" current
        docker-compose up -d
        echo "✅ Rollback completed"
    fi
    exit 1
}

trap rollback ERR

# 📁 Create directories
mkdir -p "$DEPLOY_DIR"
mkdir -p "$BACKUP_DIR"

# 💾 Backup current deployment
if [ -d "$DEPLOY_DIR/current" ]; then
    echo "💾 Creating backup of current deployment..."
    cp -r "$DEPLOY_DIR/current" "$BACKUP_DIR/backup_$DATE"
    cp -r "$DEPLOY_DIR/current" "$BACKUP_DIR/latest"
fi

# 📥 Clone or update repository
if [ -d "$DEPLOY_DIR/current" ]; then
    echo "🔄 Updating existing repository..."
    cd "$DEPLOY_DIR/current"
    git pull origin main
else
    echo "📥 Cloning repository..."
    cd "$DEPLOY_DIR"
    git clone "$REPO_URL" current
    cd current
fi

# 📋 Setup environment
if [ ! -f .env ]; then
    echo "📋 Creating production environment file..."
    cp .env.production .env
    echo "⚠️  Please update .env with production values before continuing"
    read -p "Press Enter when ready..."
fi

# 🏗️ Build production images
echo "🏗️ Building production containers..."
docker-compose build --no-cache

# 🛑 Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# 🗄️ Database backup
if docker ps -a | grep -q pravoslavie_postgres; then
    echo "💾 Creating database backup..."
    docker-compose exec -T postgres pg_dump -U pravoslavie_user pravoslavie_portal_db > "$BACKUP_DIR/db_backup_$DATE.sql"
fi

# 🚀 Start new containers
echo "🚀 Starting production containers..."
docker-compose up -d

# ⏳ Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# 🗄️ Run migrations
echo "🗄️ Running database migrations..."
docker-compose exec web python manage.py migrate --noinput

# 🎨 Collect static files
echo "🎨 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

# 🧹 Cleanup old backups (keep last 7)
echo "🧹 Cleaning up old backups..."
find "$BACKUP_DIR" -name "backup_*" -mtime +7 -delete
find "$BACKUP_DIR" -name "db_backup_*" -mtime +7 -delete

# 🔍 Health check
echo "🔍 Performing health check..."
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    rollback
fi

# 🎉 Success
echo "🎉 Deployment completed successfully!"
echo ""
echo "📊 Deployment info:"
echo "   - Date: $DATE"
echo "   - Directory: $DEPLOY_DIR/current"
echo "   - Backup: $BACKUP_DIR/backup_$DATE"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: cd $DEPLOY_DIR/current && docker-compose logs -f"
echo "   - Restart: cd $DEPLOY_DIR/current && docker-compose restart"
echo "   - Shell: cd $DEPLOY_DIR/current && docker-compose exec web bash"

# 📧 Send notification (optional)
# curl -X POST "https://hooks.slack.com/..." -d "{'text':'Pravoslavie Portal deployed successfully'}"
