#!/bin/bash
# 🔍 Православный портал - Docker Infrastructure Validation

echo "🔍 Validating Docker Infrastructure Setup..."
echo "==========================================="

# 🎯 Validation counters
CHECKS_PASSED=0
CHECKS_TOTAL=0

# 🔧 Function to check file existence
check_file() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if [ -f "$1" ]; then
        echo "✅ $1 - Found"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "❌ $1 - Missing"
    fi
}

# 📁 Function to check directory existence
check_directory() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if [ -d "$1" ]; then
        echo "✅ $1/ - Found"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "❌ $1/ - Missing"
    fi
}

# 🏗️ Core Docker Files
echo "🏗️ Checking Core Docker Files..."
check_file "Dockerfile"
check_file "Dockerfile.dev"
check_file "docker-compose.yml"
check_file "docker-compose.dev.yml"
check_file ".dockerignore"
check_file "Makefile"

# ⚙️ Configuration Files
echo ""
echo "⚙️ Checking Configuration Files..."
check_file ".env.production"
check_file ".env.development"
check_file "config/settings_production.py"
check_file "requirements.txt"

# 📁 Docker Directories
echo ""
echo "📁 Checking Docker Directories..."
check_directory "docker"
check_directory "docker/nginx"
check_directory "docker/postgres"
check_directory "docker/redis"
check_directory "docker/ssl"
check_directory "scripts"

# 🔧 Configuration Files in Docker dirs
echo ""
echo "🔧 Checking Docker Configuration Files..."
check_file "docker/nginx/nginx.conf"
check_file "docker/nginx/sites-enabled/pravoslavie-portal.conf"
check_file "docker/postgres/init.sql"
check_file "docker/redis/redis.conf"

# 📋 Scripts and Utilities
echo ""
echo "📋 Checking Scripts and Utilities..."
check_file "scripts/setup-dev.sh"
check_file "scripts/setup-dev.bat"
check_file "scripts/deploy-production.sh"
check_file "core/health_views.py"
check_file "DOCKER_README.md"

# 🔍 Check Docker and Docker Compose
echo ""
echo "🔍 Checking Docker Installation..."
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
if command -v docker &> /dev/null; then
    echo "✅ Docker - Installed ($(docker --version))"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ Docker - Not installed"
fi

CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose - Installed ($(docker-compose --version))"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ Docker Compose - Not installed"
fi

# 📊 Final Results
echo ""
echo "📊 Validation Results:"
echo "======================"
echo "✅ Checks passed: $CHECKS_PASSED"
echo "❌ Checks failed: $((CHECKS_TOTAL - CHECKS_PASSED))"
echo "📈 Total checks: $CHECKS_TOTAL"

# 🎯 Success percentage
PERCENTAGE=$((CHECKS_PASSED * 100 / CHECKS_TOTAL))
echo "🎯 Success rate: $PERCENTAGE%"

if [ $PERCENTAGE -eq 100 ]; then
    echo ""
    echo "🎉 DOCKER INFRASTRUCTURE SETUP COMPLETE! 🎉"
    echo "✅ All components are in place"
    echo "🚀 Ready to start ЭТАП 2.1 - Локальная сборка Docker-стека"
    echo ""
    echo "🛠️ Next steps:"
    echo "   1. Run: make setup (or scripts/setup-dev.bat on Windows)"
    echo "   2. Test development environment"
    echo "   3. Configure production settings in .env.production"
    echo "   4. Deploy to server"
elif [ $PERCENTAGE -ge 80 ]; then
    echo ""
    echo "⚠️  ALMOST READY - Minor issues detected"
    echo "🔧 Please fix missing components above"
    echo "📋 Most infrastructure is in place"
else
    echo ""
    echo "❌ SETUP INCOMPLETE"
    echo "🛠️ Please complete missing components above"
    echo "📋 Major infrastructure components are missing"
fi

echo ""
echo "📚 Documentation: See DOCKER_README.md for detailed instructions"
echo "🆘 Support: Check Makefile with 'make help' for available commands"
