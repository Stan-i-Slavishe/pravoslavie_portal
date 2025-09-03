# 🐳 Православный портал - Makefile для Docker

.PHONY: help build dev prod logs shell backup restore clean

# 🎯 Default target
help:
	@echo "🐳 Православный портал - Docker Commands"
	@echo ""
	@echo "📋 Available commands:"
	@echo "  make dev          - Start development environment"
	@echo "  make prod         - Start production environment"
	@echo "  make build        - Build all Docker images"
	@echo "  make logs         - Show container logs"
	@echo "  make shell        - Access Django shell"
	@echo "  make migrate      - Run database migrations"
	@echo "  make superuser    - Create Django superuser"
	@echo "  make collectstatic - Collect static files"
	@echo "  make backup       - Create database backup"
	@echo "  make restore      - Restore database from backup"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean up containers and volumes"
	@echo "  make stop         - Stop all containers"
	@echo ""

# 🏗️ Build images
build:
	@echo "🏗️ Building Docker images..."
	docker-compose build --no-cache

# 🛠️ Development environment
dev:
	@echo "🛠️ Starting development environment..."
	cp .env.development .env
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started!"
	@echo "🌐 Services available at:"
	@echo "   - Django App: http://localhost:8000"
	@echo "   - pgAdmin: http://localhost:5050"
	@echo "   - MailHog: http://localhost:8025"

# 🚀 Production environment
prod:
	@echo "🚀 Starting production environment..."
	cp .env.production .env
	docker-compose up -d
	@echo "✅ Production environment started!"

# 📊 Show logs
logs:
	@echo "📊 Showing container logs..."
	docker-compose logs -f

# 🖥️ Access Django shell
shell:
	@echo "🖥️ Accessing Django shell..."
	docker-compose exec web python manage.py shell

# 🗄️ Run migrations
migrate:
	@echo "🗄️ Running database migrations..."
	docker-compose exec web python manage.py migrate

# 👤 Create superuser
superuser:
	@echo "👤 Creating Django superuser..."
	docker-compose exec web python manage.py createsuperuser

# 🎨 Collect static files
collectstatic:
	@echo "🎨 Collecting static files..."
	docker-compose exec web python manage.py collectstatic --noinput

# 💾 Database backup
backup:
	@echo "💾 Creating database backup..."
	mkdir -p backups
	docker-compose exec postgres pg_dump -U pravoslavie_user pravoslavie_portal_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

# 🔄 Restore database
restore:
	@echo "🔄 Restoring database from backup..."
	@echo "Available backups:"
	@ls -la backups/
	@echo "Enter backup filename:"
	@read backup_file && docker-compose exec -T postgres psql -U pravoslavie_user -d pravoslavie_portal_db < backups/$$backup_file

# 🧪 Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose exec web python manage.py test

# 🧹 Clean up
clean:
	@echo "🧹 Cleaning up Docker containers and volumes..."
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# 🛑 Stop containers
stop:
	@echo "🛑 Stopping all containers..."
	docker-compose down

# 🔍 Check status
status:
	@echo "🔍 Container status..."
	docker-compose ps

# 🩺 Health check
health:
	@echo "🩺 Checking application health..."
	curl -f http://localhost:8000/health/ || echo "❌ Health check failed"

# 📈 Performance monitoring
stats:
	@echo "📈 Container stats..."
	docker stats --no-stream

# 🔄 Update and restart
update:
	@echo "🔄 Updating and restarting..."
	git pull origin main
	docker-compose build
	docker-compose down
	docker-compose up -d
	@echo "✅ Update completed!"

# 🚀 Quick start for first-time setup
setup:
	@echo "🚀 First-time setup..."
	make build
	make dev
	sleep 15
	make migrate
	make collectstatic
	@echo "🎉 Setup completed! Visit http://localhost:8000"

# 📦 Export data
export:
	@echo "📦 Exporting data..."
	mkdir -p exports
	docker-compose exec web python manage.py dumpdata --natural-foreign --natural-primary > exports/data_$(shell date +%Y%m%d_%H%M%S).json

# 📥 Import data
import:
	@echo "📥 Importing data..."
	@echo "Available exports:"
	@ls -la exports/
	@echo "Enter export filename:"
	@read export_file && docker-compose exec web python manage.py loaddata exports/$$export_file

# 🔐 Generate secrets
secrets:
	@echo "🔐 Generating new secrets..."
	@echo "SECRET_KEY=$(shell openssl rand -hex 32)"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -hex 16)"

# 📋 Show environment info
env:
	@echo "📋 Environment information..."
	@echo "Docker version: $(shell docker --version)"
	@echo "Docker Compose version: $(shell docker-compose --version)"
	@echo "Current directory: $(shell pwd)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
