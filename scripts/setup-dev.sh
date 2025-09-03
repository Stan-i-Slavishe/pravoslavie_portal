#!/bin/bash
# 🚀 Православный портал - Development Setup Script

echo "🐳 Starting Pravoslavie Portal Development Environment..."

# 🔍 Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# 📂 Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p docker/ssl

# 📋 Copy environment file
if [ ! -f .env ]; then
    echo "📋 Creating development environment file..."
    cp .env.development .env
    echo "✅ Environment file created. Please review and update values in .env"
fi

# 🏗️ Build and start development containers
echo "🏗️ Building development containers..."
docker-compose -f docker-compose.dev.yml build

echo "🚀 Starting development environment..."
docker-compose -f docker-compose.dev.yml up -d

# ⏳ Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# 🗄️ Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# 👤 Create superuser (interactive)
echo "👤 Creating Django superuser..."
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# 📊 Load initial data (if exists)
if [ -f "fixtures/initial_data.json" ]; then
    echo "📊 Loading initial data..."
    docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata fixtures/initial_data.json
fi

# 🎨 Collect static files
echo "🎨 Collecting static files..."
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

echo "✅ Development environment is ready!"
echo ""
echo "🌐 Services available at:"
echo "   - Django App: http://localhost:8000"
echo "   - pgAdmin: http://localhost:5050"
echo "   - MailHog: http://localhost:8025"
echo ""
echo "📊 Database info:"
echo "   - Host: localhost:5432"
echo "   - Database: pravoslavie_local_db"
echo "   - User: pravoslavie_user"
echo "   - Password: dev_password_123"
echo ""
echo "🛠️ Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "   - Stop: docker-compose -f docker-compose.dev.yml down"
echo "   - Shell: docker-compose -f docker-compose.dev.yml exec web bash"
