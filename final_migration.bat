@echo off
REM PostgreSQL Migration Final Step
REM ================================

echo.
echo PostgreSQL Migration - Final Step
echo ==================================
echo.

REM Force LOCAL environment
set DJANGO_ENV=local

echo Step 1: Test PostgreSQL connection
echo ----------------------------------
python manage.py check --database default
if errorlevel 1 (
    echo ERROR: Cannot connect to PostgreSQL
    pause
    exit /b 1
)
echo PostgreSQL connection OK

echo.
echo Step 2: Apply migrations
echo ------------------------
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo Migrations applied successfully

echo.
echo Step 3: Import data
echo -------------------

echo Importing users...
python manage.py loaddata backups\auth_User_20250901_2113.json

echo Importing groups...
python manage.py loaddata backups\auth_Group_20250901_2113.json

echo Importing core data...
python manage.py loaddata backups\core_20250901_2113.json

echo Importing stories...
python manage.py loaddata backups\stories_20250901_2113.json

echo Importing books...
python manage.py loaddata backups\books_20250901_2113.json

echo Importing shop...
python manage.py loaddata backups\shop_20250901_2113.json

echo Importing fairy tales...
python manage.py loaddata backups\fairy_tales_20250901_2113.json

echo Importing accounts...
python manage.py loaddata backups\accounts_20250901_2113.json

echo Importing subscriptions...
python manage.py loaddata backups\subscriptions_20250901_2113.json

echo.
echo Step 4: Create superuser
echo ------------------------
echo Create superuser (or press Ctrl+C to skip):
python manage.py createsuperuser

echo.
echo Step 5: Test server
echo -------------------
echo Starting Django server...
echo Open: http://127.0.0.1:8000/
echo Press Ctrl+C to stop

python manage.py runserver 127.0.0.1:8000

echo.
echo Migration completed successfully!
pause