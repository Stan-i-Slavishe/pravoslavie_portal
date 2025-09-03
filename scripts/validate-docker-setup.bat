@echo off
REM 🔍 Православный портал - Docker Infrastructure Validation (Windows)

echo 🔍 Validating Docker Infrastructure Setup...
echo ===========================================

REM 🎯 Validation counters
set CHECKS_PASSED=0
set CHECKS_TOTAL=0

REM 🏗️ Core Docker Files
echo 🏗️ Checking Core Docker Files...
call :check_file "Dockerfile"
call :check_file "Dockerfile.dev"
call :check_file "docker-compose.yml"
call :check_file "docker-compose.dev.yml"
call :check_file ".dockerignore"
call :check_file "Makefile"

REM ⚙️ Configuration Files
echo.
echo ⚙️ Checking Configuration Files...
call :check_file ".env.production"
call :check_file ".env.development"
call :check_file "config\settings_production.py"
call :check_file "requirements.txt"

REM 📁 Docker Directories
echo.
echo 📁 Checking Docker Directories...
call :check_directory "docker"
call :check_directory "docker\nginx"
call :check_directory "docker\postgres"
call :check_directory "docker\redis"
call :check_directory "docker\ssl"
call :check_directory "scripts"

REM 🔧 Configuration Files in Docker dirs
echo.
echo 🔧 Checking Docker Configuration Files...
call :check_file "docker\nginx\nginx.conf"
call :check_file "docker\nginx\sites-enabled\pravoslavie-portal.conf"
call :check_file "docker\postgres\init.sql"
call :check_file "docker\redis\redis.conf"

REM 📋 Scripts and Utilities
echo.
echo 📋 Checking Scripts and Utilities...
call :check_file "scripts\setup-dev.sh"
call :check_file "scripts\setup-dev.bat"
call :check_file "scripts\deploy-production.sh"
call :check_file "core\health_views.py"
call :check_file "DOCKER_README.md"

REM 🔍 Check Docker and Docker Compose
echo.
echo 🔍 Checking Docker Installation...
set /a CHECKS_TOTAL+=1
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker - Installed
    set /a CHECKS_PASSED+=1
) else (
    echo ❌ Docker - Not installed
)

set /a CHECKS_TOTAL+=1
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Compose - Installed
    set /a CHECKS_PASSED+=1
) else (
    echo ❌ Docker Compose - Not installed
)

REM 📊 Final Results
echo.
echo 📊 Validation Results:
echo ======================
echo ✅ Checks passed: %CHECKS_PASSED%
set /a CHECKS_FAILED=%CHECKS_TOTAL%-%CHECKS_PASSED%
echo ❌ Checks failed: %CHECKS_FAILED%
echo 📈 Total checks: %CHECKS_TOTAL%

REM 🎯 Success percentage
set /a PERCENTAGE=%CHECKS_PASSED%*100/%CHECKS_TOTAL%
echo 🎯 Success rate: %PERCENTAGE%%%

if %PERCENTAGE% equ 100 (
    echo.
    echo 🎉 DOCKER INFRASTRUCTURE SETUP COMPLETE! 🎉
    echo ✅ All components are in place
    echo 🚀 Ready to start ЭТАП 2.1 - Локальная сборка Docker-стека
    echo.
    echo 🛠️ Next steps:
    echo    1. Run: scripts\setup-dev.bat
    echo    2. Test development environment
    echo    3. Configure production settings in .env.production
    echo    4. Deploy to server
) else if %PERCENTAGE% geq 80 (
    echo.
    echo ⚠️  ALMOST READY - Minor issues detected
    echo 🔧 Please fix missing components above
    echo 📋 Most infrastructure is in place
) else (
    echo.
    echo ❌ SETUP INCOMPLETE
    echo 🛠️ Please complete missing components above
    echo 📋 Major infrastructure components are missing
)

echo.
echo 📚 Documentation: See DOCKER_README.md for detailed instructions
echo 🆘 Support: Use provided batch scripts for Windows commands
pause
goto :eof

REM 🔧 Function to check file existence
:check_file
set /a CHECKS_TOTAL+=1
if exist "%~1" (
    echo ✅ %~1 - Found
    set /a CHECKS_PASSED+=1
) else (
    echo ❌ %~1 - Missing
)
goto :eof

REM 📁 Function to check directory existence
:check_directory
set /a CHECKS_TOTAL+=1
if exist "%~1" (
    echo ✅ %~1\ - Found
    set /a CHECKS_PASSED+=1
) else (
    echo ❌ %~1\ - Missing
)
goto :eof
