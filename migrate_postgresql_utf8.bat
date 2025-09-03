@echo off
chcp 65001 >nul
REM ==========================================
REM MIGRATE TO POSTGRESQL - UTF-8 VERSION
REM ==========================================

echo.
echo ========================================
echo    MIGRATION SQLITE -^> POSTGRESQL
echo ========================================
echo.

REM Check virtual environment
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    pause
    exit /b 1
)

REM Set UTF-8 environment for Python
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM Activate virtual environment  
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo STEP 0: Configure environment
echo =====================================
echo Setting UTF-8 encoding and LOCAL environment...

REM Force local environment with UTF-8
set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo Environment configured
echo.

echo STEP 1: Configure PostgreSQL settings
echo =====================================
echo Creating PostgreSQL configuration...

REM Create backups directory
if not exist "backups" mkdir backups

REM Backup current .env.local
set BACKUP_TIME=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set BACKUP_TIME=%BACKUP_TIME: =0%

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

echo .env.local configured for PostgreSQL
echo.

echo STEP 2: Test PostgreSQL connection
echo =======================================

set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo Testing Django connection to PostgreSQL...
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

echo STEP 3: Apply migrations to PostgreSQL
echo =============================
echo Creating database structure...

set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8
python manage.py migrate --settings=config.settings_local
if errorlevel 1 (
    echo Error applying migrations
    pause
    exit /b 1
)

echo Database structure created successfully
echo.

echo STEP 4: Backup SQLite data with proper encoding
echo =============================================
echo Creating SQLite export with UTF-8 encoding...

REM Try different export strategies
echo Attempting selective data export...

REM Export by individual apps to avoid encoding issues
set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8

echo Exporting core data...
python manage.py dumpdata core --natural-foreign --natural-primary --settings=config.settings_local -o "backups\core_%BACKUP_TIME%.json"

echo Exporting stories data...
python manage.py dumpdata stories --natural-foreign --natural-primary --settings=config.settings_local -o "backups\stories_%BACKUP_TIME%.json"

echo Exporting books data...
python manage.py dumpdata books --natural-foreign --natural-primary --settings=config.settings_local -o "backups\books_%BACKUP_TIME%.json"

echo Exporting shop data...
python manage.py dumpdata shop --natural-foreign --natural-primary --settings=config.settings_local -o "backups\shop_%BACKUP_TIME%.json"

echo Exporting fairy_tales data...
python manage.py dumpdata fairy_tales --natural-foreign --natural-primary --settings=config.settings_local -o "backups\fairy_tales_%BACKUP_TIME%.json"

echo Exporting accounts data...
python manage.py dumpdata accounts --natural-foreign --natural-primary --settings=config.settings_local -o "backups\accounts_%BACKUP_TIME%.json"

echo Exporting auth data...
python manage.py dumpdata auth.User auth.Group --natural-foreign --natural-primary --settings=config.settings_local -o "backups\auth_%BACKUP_TIME%.json"

echo Selective export completed
echo.

echo STEP 5: Import data to PostgreSQL  
echo ================================
echo Loading data into PostgreSQL...

set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8

REM Import data in correct order
echo Importing auth data...
if exist "backups\auth_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\auth_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing core data...
if exist "backups\core_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\core_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing stories data...
if exist "backups\stories_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\stories_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing books data...
if exist "backups\books_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\books_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing fairy_tales data...
if exist "backups\fairy_tales_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\fairy_tales_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing shop data...
if exist "backups\shop_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\shop_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Importing accounts data...
if exist "backups\accounts_%BACKUP_TIME%.json" (
    python manage.py loaddata "backups\accounts_%BACKUP_TIME%.json" --settings=config.settings_local
)

echo Data import completed
echo.

echo STEP 6: Create superuser
echo ==================================
echo Creating administrator for PostgreSQL...

set DJANGO_ENV=local
echo.
echo Enter superuser data ^(or press Ctrl+C to skip^):
python manage.py createsuperuser --settings=config.settings_local
if errorlevel 1 (
    echo Superuser creation skipped
)

echo.

echo STEP 7: Test server
echo ==================================
echo Starting Django development server...

set DJANGO_ENV=local
set PYTHONIOENCODING=utf-8

echo.
echo Server starting with PostgreSQL database...
echo.
echo Check these URLs:
echo    • Home: http://127.0.0.1:8000/
echo    • Admin: http://127.0.0.1:8000/admin/  
echo    • Stories: http://127.0.0.1:8000/stories/
echo    • Books: http://127.0.0.1:8000/books/
echo    • Shop: http://127.0.0.1:8000/shop/
echo.

echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 127.0.0.1:8000 --settings=config.settings_local

echo.
echo ==========================================
echo        MIGRATION PROCESS COMPLETED!
echo ==========================================
echo.
echo What was done:
echo    Environment set to LOCAL with UTF-8
echo    PostgreSQL connection established  
echo    Database structure created
echo    Data exported by apps ^(avoiding encoding issues^)
echo    Data imported to PostgreSQL
echo    Development server tested
echo.
echo NEXT STEPS:
echo    1. Check data integrity: python check_migration.py
echo    2. Create PostgreSQL backup
echo    3. Test all website functions
echo.
pause