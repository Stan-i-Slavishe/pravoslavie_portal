@echo off
REM ==========================================
REM QUICK POSTGRESQL SETUP FOR PROJECT
REM ==========================================

echo.
echo ========================================
echo    INSTALL AND SETUP POSTGRESQL
echo ========================================
echo.

echo INSTALLATION STEPS:
echo.
echo 1. Download PostgreSQL 15+ from official website:
echo    https://www.postgresql.org/download/windows/
echo.
echo 2. Remember the password for postgres user during installation
echo.
echo 3. Return to this script after installation
echo.
pause

echo.
echo Checking PostgreSQL installation...

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if errorlevel 1 (
    echo PostgreSQL not found in PATH
    echo.
    echo Add PostgreSQL to PATH:
    echo    C:\Program Files\PostgreSQL\15\bin
    echo.
    echo Restart this script after adding to PATH
    pause
    exit /b 1
)

echo PostgreSQL found
psql --version
echo.

echo Creating database and user...
echo.
echo Enter postgres user password:

REM Execute SQL script to create DB
psql -U postgres -h localhost -f setup_postgresql.sql
if errorlevel 1 (
    echo Error creating database
    echo.
    echo Possible causes:
    echo    • Wrong postgres password
    echo    • PostgreSQL not running
    echo    • User pravoslavie_user already exists
    echo.
    pause
    exit /b 1
)

echo.
echo Database pravoslavie_local_db created successfully!
echo.
echo Testing connection to new database...

REM Check connection to created DB
psql -U pravoslavie_user -h localhost -d pravoslavie_local_db -c "\dt"
if errorlevel 1 (
    echo Warning: Connection issues with pravoslavie_user
    echo This is normal - Django will create tables later
)

echo.
echo ==========================================
echo        POSTGRESQL READY TO USE!
echo ==========================================
echo.
echo Created objects:
echo    Database: pravoslavie_local_db
echo    User: pravoslavie_user  
echo    Password: local_strong_password_2024
echo    Host: localhost
echo    Port: 5432
echo.
echo NEXT STEPS:
echo    1. Run migrate_to_postgresql_en.bat
echo    2. This will transfer all data from SQLite to PostgreSQL
echo.
pause