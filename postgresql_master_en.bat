@echo off
REM ==========================================
REM POSTGRESQL MIGRATION MASTER SCRIPT
REM ==========================================

title PostgreSQL Migration - Pravoslavie Portal

:MENU
cls
echo.
echo ================================================
echo    POSTGRESQL MIGRATION - PRAVOSLAVIE PORTAL
echo ================================================
echo.
echo Choose action:
echo.
echo    1. Install and setup PostgreSQL
echo    2. Migrate data from SQLite to PostgreSQL  
echo    3. Check data integrity after migration
echo    4. Create PostgreSQL backup
echo    5. Run site on PostgreSQL
echo    6. Show system status
echo.
echo    0. Exit
echo.
set /p choice=Enter action number: 

if "%choice%"=="1" goto INSTALL_POSTGRESQL
if "%choice%"=="2" goto MIGRATE_DATA  
if "%choice%"=="3" goto CHECK_DATA
if "%choice%"=="4" goto CREATE_BACKUP
if "%choice%"=="5" goto RUN_SITE
if "%choice%"=="6" goto SHOW_STATUS
if "%choice%"=="0" goto EXIT
goto MENU

:INSTALL_POSTGRESQL
cls
echo.
echo ================================================
echo        INSTALL AND SETUP POSTGRESQL
echo ================================================
echo.
call setup_postgresql_en.bat
pause
goto MENU

:MIGRATE_DATA
cls  
echo.
echo ================================================
echo          MIGRATE DATA SQLite -^> PostgreSQL
echo ================================================
echo.
call migrate_to_postgresql_en.bat
pause
goto MENU

:CHECK_DATA
cls
echo.
echo ================================================
echo        CHECK DATA INTEGRITY
echo ================================================
echo.
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    pause
    goto MENU
)
call .venv\Scripts\activate.bat
python check_migration.py
pause
goto MENU

:CREATE_BACKUP
cls
echo.
echo ================================================
echo         CREATE POSTGRESQL BACKUP
echo ================================================
echo.
call create_postgresql_backup_en.bat
pause
goto MENU

:RUN_SITE
cls
echo.
echo ================================================
echo           RUN SITE ON POSTGRESQL
echo ================================================
echo.
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    pause
    goto MENU
)

call .venv\Scripts\activate.bat

echo Checking PostgreSQL connection...
python manage.py check --database default
if errorlevel 1 (
    echo Problems with PostgreSQL connection
    echo Execute steps 1 and 2 first
    pause
    goto MENU
)

echo PostgreSQL connection successful
echo.
echo Starting development server...
echo Press Ctrl+C to stop
echo.
python manage.py runserver 127.0.0.1:8000
pause
goto MENU

:SHOW_STATUS
cls
echo.
echo ================================================
echo              SYSTEM STATUS
echo ================================================
echo.

REM Check PostgreSQL
echo PostgreSQL:
pg_dump --version >nul 2>&1
if errorlevel 1 (
    echo    PostgreSQL not installed or not in PATH
) else (
    echo    PostgreSQL installed
    pg_dump --version
)

echo.

REM Check virtual environment
echo Python environment:
if exist ".venv\Scripts\activate.bat" (
    echo    Virtual environment found
) else (
    echo    Virtual environment not found
)

echo.

REM Check configuration
echo Configuration:
if exist ".env.local" (
    echo    .env.local file found
    findstr "USE_SQLITE" .env.local >nul 2>&1
    if errorlevel 1 (
        echo    DB settings not defined
    ) else (
        findstr "USE_SQLITE=False" .env.local >nul 2>&1
        if errorlevel 1 (
            echo    Configured for SQLite
        ) else (
            echo    Configured for PostgreSQL
        )
    )
) else (
    echo    .env.local file not found
)

echo.

REM Check data  
echo Data:
if exist "db.sqlite3" (
    echo    SQLite DB found ^(size: 
    for %%A in ("db.sqlite3") do echo %%~zA bytes^)
) else (
    echo    SQLite DB not found
)

if exist "backups" (
    echo    Backups folder found
    for /f %%i in ('dir /b backups\*.json 2^>nul ^| find /c /v ""') do echo        SQLite exports: %%i
    for /f %%i in ('dir /b backups\*.sql 2^>nul ^| find /c /v ""') do echo        PostgreSQL backups: %%i
) else (
    echo    Backups folder not found
)

echo.

REM PostgreSQL connection status
if exist ".venv\Scripts\activate.bat" (
    echo PostgreSQL connection test:
    call .venv\Scripts\activate.bat >nul 2>&1
    python manage.py check --database default >nul 2>&1
    if errorlevel 1 (
        echo    Could not connect to PostgreSQL
    ) else (
        echo    PostgreSQL connected and working
    )
)

echo.
echo ================================================
pause
goto MENU

:EXIT
cls
echo.
echo ============================================
echo    Thanks for using the script!
echo ============================================
echo.
echo WORK RESULTS:
echo    Ready scripts for PostgreSQL migration
echo    Automated data migration
echo    Integrity check after transfer
echo    Backup system
echo.
echo NEXT STEPS:
echo    1. Docker containerization
echo    2. Production server deployment
echo    3. CI/CD pipeline setup
echo.
echo All scripts saved in project root
echo.
pause
exit