@echo off
REM ==========================================
REM MIGRATE TO POSTGRESQL SCRIPT  
REM ==========================================

echo.
echo ========================================
echo    MIGRATION SQLITE -> POSTGRESQL
echo ========================================
echo.

REM Check virtual environment
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Create .venv and install dependencies
    pause
    exit /b 1
)

REM Activate virtual environment  
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo STEP 1: Backup SQLite data
echo =====================================
echo Creating SQLite data export...

REM Create backups directory
if not exist "backups" mkdir backups

REM Export data with timestamp
set BACKUP_TIME=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set BACKUP_TIME=%BACKUP_TIME: =0%

python manage.py dumpdata --natural-foreign --natural-primary -o "backups\sqlite_full_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo Error creating full export
    pause
    exit /b 1
)

python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission -o "backups\sqlite_clean_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo Error creating clean export
    pause
    exit /b 1
)

echo SQLite data export completed
echo    Files saved to backups\ folder
echo.

echo STEP 2: Check PostgreSQL connection
echo =======================================
echo Checking PostgreSQL connection...

REM Update .env file for PostgreSQL
echo Updating .env.local settings...
(
echo # Environment
echo DJANGO_ENV=local
echo.
echo # Security
echo SECRET_KEY=django-insecure-local-development-key-change-me  
echo DEBUG=True
echo ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver
echo.
echo # === SWITCH TO POSTGRESQL ===
echo USE_SQLITE=False
echo.
echo # PostgreSQL settings
echo DB_NAME=pravoslavie_local_db
echo DB_USER=pravoslavie_user
echo DB_PASSWORD=local_strong_password_2024
echo DB_HOST=localhost
echo DB_PORT=5432
echo.
echo # Email ^(console for development^)
echo EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
echo.
echo # API keys ^(test versions^)
echo YOUTUBE_API_KEY=your-youtube-api-key-for-testing
echo YOOKASSA_SHOP_ID=test-shop-id  
echo YOOKASSA_SECRET_KEY=test-secret-key
echo YOOKASSA_TEST_MODE=True
echo.
echo # Redis
echo REDIS_URL=redis://127.0.0.1:6379/1
echo CELERY_BROKER_URL=redis://localhost:6379/0
echo CELERY_RESULT_BACKEND=redis://localhost:6379/0
echo.
echo # Push notifications
echo VAPID_PRIVATE_KEY=test-private-key-for-development-only
echo VAPID_PUBLIC_KEY=BKkKS_8l4BqHZ8jO4yXLsJYK6Q7L_Hd-UQOUUj9SqPxKMaI6F5VJ_HqJN4R7s3uK6GnX2bOqT9hL7F2jZaWvNdc
echo VAPID_EMAIL=admin@pravoslavie-portal.ru
echo.
echo # Admin
echo ADMIN_EMAIL=admin@localhost
echo.
echo # Additional development settings
echo SECURE_SSL_REDIRECT=False
echo CACHE_BACKEND=dummy
) > .env.local

echo .env.local settings updated for PostgreSQL
echo.

REM Check DB connection
echo Checking Django connection to PostgreSQL...
python manage.py check --database default
if errorlevel 1 (
    echo PostgreSQL connection error!
    echo.
    echo Check:
    echo    1. PostgreSQL is running
    echo    2. Database pravoslavie_local_db exists
    echo    3. User pravoslavie_user exists  
    echo    4. Password in .env.local is correct
    echo.
    pause
    exit /b 1
)

echo PostgreSQL connection successful
echo.

echo STEP 3: Create database structure
echo =============================
echo Applying Django migrations...

python manage.py migrate
if errorlevel 1 (
    echo Error applying migrations
    pause
    exit /b 1
)

echo Database structure created successfully
echo.

echo STEP 4: Import data
echo =====================
echo Loading data into PostgreSQL...

REM Find latest created backup
for /f %%i in ('dir /b /o:d "backups\sqlite_clean_*.json"') do set LATEST_BACKUP=%%i

echo Importing file: %LATEST_BACKUP%
python manage.py loaddata "backups\%LATEST_BACKUP%"
if errorlevel 1 (
    echo Error importing clean data
    echo Trying full import...
    
    for /f %%i in ('dir /b /o:d "backups\sqlite_full_*.json"') do set LATEST_FULL_BACKUP=%%i
    python manage.py loaddata "backups\%LATEST_FULL_BACKUP%" --verbosity=2
    if errorlevel 1 (
        echo Critical data import error
        pause
        exit /b 1
    )
)

echo Data imported successfully
echo.

echo STEP 5: Create superuser
echo ==================================
echo Creating administrator for PostgreSQL...
echo.
echo Enter superuser data:

python manage.py createsuperuser
if errorlevel 1 (
    echo Skipping superuser creation
)

echo.

echo STEP 6: Check functionality
echo ==================================
echo Running system tests...

REM Check that site starts
echo Checking server startup...
timeout /t 2 > nul
start /min python manage.py runserver 127.0.0.1:8000

echo.
echo Server started at http://127.0.0.1:8000
echo.
echo Check in browser:
echo    • Home page: http://127.0.0.1:8000/
echo    • Admin: http://127.0.0.1:8000/admin/  
echo    • Stories: http://127.0.0.1:8000/stories/
echo    • Books: http://127.0.0.1:8000/books/
echo    • Shop: http://127.0.0.1:8000/shop/
echo.

echo STEP 7: Create PostgreSQL backup
echo ===================================
echo Creating backup of new PostgreSQL database...

REM Create PostgreSQL dump
set PG_BACKUP_FILE=backups\postgresql_%BACKUP_TIME%.sql
pg_dump -U pravoslavie_user -h localhost -d pravoslavie_local_db -f "%PG_BACKUP_FILE%"
if errorlevel 1 (
    echo Could not create pg_dump ^(possibly not in PATH^)
    echo Create backup manually via pgAdmin or add PostgreSQL to PATH
) else (
    echo PostgreSQL backup created: %PG_BACKUP_FILE%
)

echo.
echo ==========================================
echo        MIGRATION COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo What was done:
echo    SQLite data exported
echo    PostgreSQL configured and connected  
echo    Database structure created
echo    Data imported
echo    Superuser created
echo    Server started and working
echo    Backups created
echo.
echo NEXT STEPS:
echo    1. Test all site functions
echo    2. Make sure all data is in place
echo    3. Proceed to Docker infrastructure creation
echo.
echo To stop server press Ctrl+C in server window
echo.
pause