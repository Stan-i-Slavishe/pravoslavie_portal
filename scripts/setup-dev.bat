@echo off
REM 🚀 Православный портал - Development Setup Script (Windows)

echo 🐳 Starting Pravoslavie Portal Development Environment...

REM 🔍 Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM 📂 Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "docker\ssl" mkdir docker\ssl

REM 📋 Copy environment file
if not exist ".env" (
    echo 📋 Creating development environment file...
    copy .env.development .env
    echo ✅ Environment file created. Please review and update values in .env
)

REM 🏗️ Build and start development containers
echo 🏗️ Building development containers...
docker-compose -f docker-compose.dev.yml build

echo 🚀 Starting development environment...
docker-compose -f docker-compose.dev.yml up -d

REM ⏳ Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM 🗄️ Run database migrations
echo 🗄️ Running database migrations...
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

REM 👤 Create superuser (interactive)
echo 👤 Creating Django superuser...
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

REM 📊 Load initial data (if exists)
if exist "fixtures\initial_data.json" (
    echo 📊 Loading initial data...
    docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata fixtures/initial_data.json
)

REM 🎨 Collect static files
echo 🎨 Collecting static files...
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

echo ✅ Development environment is ready!
echo.
echo 🌐 Services available at:
echo    - Django App: http://localhost:8000
echo    - pgAdmin: http://localhost:5050
echo    - MailHog: http://localhost:8025
echo.
echo 📊 Database info:
echo    - Host: localhost:5432
echo    - Database: pravoslavie_local_db
echo    - User: pravoslavie_user
echo    - Password: dev_password_123
echo.
echo 🛠️ Useful commands:
echo    - View logs: docker-compose -f docker-compose.dev.yml logs -f
echo    - Stop: docker-compose -f docker-compose.dev.yml down
echo    - Shell: docker-compose -f docker-compose.dev.yml exec web bash

pause
