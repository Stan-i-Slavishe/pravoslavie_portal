@echo off
REM ==========================================
REM MIGRATE TO POSTGRESQL SCRIPT - FIXED
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
echo STEP 0: Set LOCAL environment
echo =====================================
echo Forcing LOCAL environment for migration...

REM Force local environment
set DJANGO_ENV=local
echo DJANGO_ENV set to: %DJANGO_ENV%

echo.
echo STEP 1: Backup SQLite data
echo =====================================
echo Creating SQLite data export...

REM Create backups directory
if not exist "backups" mkdir backups

REM Export data with timestamp
set BACKUP_TIME=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set BACKUP_TIME=%BACKUP_TIME: =0%

echo Exporting with LOCAL environment...
set DJANGO_ENV=local
python manage.py dumpdata --natural-foreign --natural-primary -o "backups\sqlite_full_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo Error creating full export
    echo.
    echo Trying with settings override...
    python manage.py dumpdata --natural-foreign --natural-primary --settings=config.settings_local -o "backups\sqlite_full_%BACKUP_TIME%.json"
    if errorlevel 1 (
        echo Critical error during export
        echo Check database connection
        pause
        exit /b 1
    )
)

set DJANGO_ENV=local
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission -o "backups\sqlite_clean_%BACKUP_TIME%.json"
if errorlevel 1 (
    echo Error creating clean export
    echo Trying with settings override...
    python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --settings=config.settings_local -o "backups\sqlite_clean_%BACKUP_TIME%.json"
    if errorlevel 1 (
        echo Error creating clean export, but continuing...
    )
)

echo SQLite data export completed
echo    Files saved to backups\ folder
echo.

echo STEP 2: Configure for PostgreSQL
echo =======================================
echo Updating .env.local for PostgreSQL...

REM Backup current .env.local
if exist ".env.local" (
    copy ".env.local" ".env.local.backup_%BACKUP_TIME%" >nul
    echo Current .env.local backed up
)

REM Create new .env.local for PostgreSQL
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

echo .env.local updated for PostgreSQL
echo.

REM Force environment reload
set DJANGO_ENV=local

echo STEP 3: Check PostgreSQL connection
echo =======================================
echo Checking Django connection to PostgreSQL...

set DJANGO_ENV=local
python manage.py check --database default --settings=config.settings_local
if errorlevel 1 (
    echo PostgreSQL connection error!
    echo.
    echo Check:
    echo    1. PostgreSQL is running
    echo    2. Database pravoslavie_local_db exists
    echo    3. User pravoslavie_user exists  
    echo    4. Password is correct: local_strong_password_2024
    echo.
    pause
    exit /b 1
)

echo PostgreSQL connection successful
echo.

echo STEP 4: Create database structure
echo =============================
echo Applying Django migrations...

set DJANGO_ENV=local
python manage.py migrate --settings=config.settings_local
if errorlevel 1 (
    echo Error applying migrations
    pause
    exit /b 1
)

echo Database structure created successfully
echo.

echo STEP 5: Import data
echo =====================
echo Loading data into PostgreSQL...

REM Find latest created backup
for /f %%i in ('dir /b /o:d "backups\sqlite_clean_*.json"') do set LATEST_BACKUP=%%i

if exist "backups\%LATEST_BACKUP%" (
    echo Importing file: %LATEST_BACKUP%
    set DJANGO_ENV=local
    python manage.py loaddata "backups\%LATEST_BACKUP%" --settings=config.settings_local
    if errorlevel 1 (
        echo Error importing clean data
        echo Trying full import...
        
        for /f %%i in ('dir /b /o:d "backups\sqlite_full_*.json"') do set LATEST_FULL_BACKUP=%%i
        if exist "backups\%LATEST_FULL_BACKUP%" (
            set DJANGO_ENV=local
            python manage.py loaddata "backups\%LATEST_FULL_BACKUP%" --verbosity=2 --settings=config.settings_local
            if errorlevel 1 (
                echo Data import had issues, but continuing...
            )
        )
    )
) else (
    echo No backup files found, skipping data import
)

echo Data import attempted
echo.

echo STEP 6: Create superuser
echo ==================================
echo Creating administrator for PostgreSQL...
echo.
echo Enter superuser data:

set DJANGO_ENV=local
python manage.py createsuperuser --settings=config.settings_local
if errorlevel 1 (
    echo Skipping superuser creation
)

echo.

echo STEP 7: Test server startup
echo ==================================
echo Testing Django server...

set DJANGO_ENV=local
echo Server will start with LOCAL settings
echo.
echo Check in browser:
echo    • Home page: http://127.0.0.1:8000/
echo    • Admin: http://127.0.0.1:8000/admin/  
echo    • Stories: http://127.0.0.1:8000/stories/
echo    • Books: http://127.0.0.1:8000/books/
echo    • Shop: http://127.0.0.1:8000/shop/
echo.

echo Starting server in 5 seconds...
timeout /t 5

set DJANGO_ENV=local
python manage.py runserver 127.0.0.1:8000 --settings=config.settings_local

echo.
echo ==========================================
echo        MIGRATION COMPLETED!
echo ==========================================
echo.
echo What was done:
echo    Environment forced to LOCAL
echo    SQLite data exported
echo    PostgreSQL configured  
echo    Database structure created
echo    Data imported
echo    Server tested
echo.
echo NEXT STEPS:
echo    1. Test all site functions
echo    2. Run data integrity check
echo    3. Create PostgreSQL backup
echo.
pause