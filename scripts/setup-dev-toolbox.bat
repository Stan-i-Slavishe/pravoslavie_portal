@echo off
REM 🐳 Православный портал - Docker Toolbox Setup (Windows LTSC)

echo 🐳 Starting Pravoslavie Portal with Docker Toolbox...

REM 🔍 Check if Docker Toolbox is installed
where docker-machine >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Toolbox is not installed. Please install Docker Toolbox first.
    echo 📥 Download from: https://github.com/docker/toolbox/releases
    pause
    exit /b 1
)

REM 🚀 Start default machine if not running
echo 🚀 Checking Docker Machine status...
docker-machine status default 2>nul
if %errorlevel% neq 0 (
    echo 🏗️ Creating default Docker machine...
    docker-machine create --driver virtualbox default
) else (
    echo ✅ Docker machine exists, starting if needed...
    docker-machine start default 2>nul
)

REM ⚙️ Setup environment
echo ⚙️ Setting up Docker environment...
FOR /f "tokens=*" %%i IN ('docker-machine env default') DO %%i

REM 📋 Get machine IP
FOR /f "tokens=*" %%i IN ('docker-machine ip default') DO set DOCKER_IP=%%i

REM 📂 Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "docker\ssl" mkdir docker\ssl

REM 📋 Copy environment file
if not exist ".env" (
    echo 📋 Creating development environment file...
    copy .env.development .env
    echo ✅ Environment file created.
)

REM 🏗️ Build and start development containers
echo 🏗️ Building development containers...
docker-compose -f docker-compose.dev.yml build

echo 🚀 Starting development environment...
docker-compose -f docker-compose.dev.yml up -d

REM ⏳ Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 15 /nobreak >nul

REM 🗄️ Run database migrations
echo 🗄️ Running database migrations...
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

REM 🎨 Collect static files
echo 🎨 Collecting static files...
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

echo ✅ Development environment is ready!
echo.
echo 🌐 Services available at (Docker Machine IP: %DOCKER_IP%):
echo    - Django App: http://%DOCKER_IP%:8000
echo    - pgAdmin: http://%DOCKER_IP%:5050
echo    - MailHog: http://%DOCKER_IP%:8025
echo.
echo 📊 Database info:
echo    - Host: %DOCKER_IP%:5432
echo    - Database: pravoslavie_local_db
echo    - User: pravoslavie_user
echo    - Password: dev_password_123
echo.
echo 🛠️ Useful commands (in Docker Quickstart Terminal):
echo    - View logs: docker-compose -f docker-compose.dev.yml logs -f
echo    - Stop: docker-compose -f docker-compose.dev.yml down
echo    - Shell: docker-compose -f docker-compose.dev.yml exec web bash

pause
